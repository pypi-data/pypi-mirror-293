from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Optional

import pandas as pd

from forecast_dataprep.data_enrichment.cyclical_features import add_cyclical_features
from forecast_dataprep.data_enrichment.delayed_features import add_delayed_consumption_feature
from forecast_dataprep.data_enrichment.prices import add_prices
from forecast_dataprep.data_enrichment.temperature import get_multilocation_temperature_forecasts_from_metadata
from forecast_dataprep.data_fetching import get_dataframes, get_metadata
from forecast_dataprep.data_fetching.data_models import BigQueryBundle
from forecast_dataprep.data_ingestion.prediction import there_is_enough_historical_data
from forecast_dataprep.data_ingestion.shared import ingest_metadata_dataframe
from forecast_dataprep.data_ingestion.training import ingest_hourly_consumption_data
from forecast_dataprep.data_models import IngestmentOutput, FeatureSelection, ForecastTargetList, Timespan
from forecast_dataprep.data_enrichment.time_constants import TimeConstants
from forecast_dataprep.weather_api.data_models import WeatherApiBundle


def fetch_ingest_and_enrich(
        bq: BigQueryBundle,
        targets: ForecastTargetList,
        timespan: Timespan,
        weather_api: WeatherApiBundle,
        features: FeatureSelection,
        training: bool = False,
        prediction_start: Optional[datetime] = None) -> pd.DataFrame:
    """
    Get data from BQ, then ingest and enrich it, so it can be used for training or prediction

    :param BigQueryBundle bq: Object with the BigQuery client and project details
    :param ForecastTargetList targets: Object containing either meteringpoint or substation identifiers
    :param Timespan timespan: Object with the start and end of the time period of interest
    :param WeatherApiBundle weather_api: Object with Weather API info and credentials
    :param FeatureSelection features: Object that contains which features should be returned
    :param bool training: True if training constraints should be applied on the data. False implies prediction.
    :param datetime prediction_start: Used only if not training. Adjusts the prediction horizon.
    :returns: a DataFrame with enriched data
    :raises ValueError: If no temperature data or no locations
    :raises RuntimeError: If Weather API does not return 200
    """
    # Step 0: Check input types
    _check_types(bq, targets, timespan, weather_api)

    # Step 1: Get metadata
    dfm = get_metadata(bq, targets)

    # Step 2: Branching: Run queries simultaneously to minimise runtime
    # Uses by default the multilocation function to call Weather API
    with ThreadPoolExecutor() as executor:
        path_1_task = executor.submit(main_ingestion_route, dfm, targets, bq,
                                      timespan, training, features,
                                      prediction_start)
        path_2_task = executor.submit(
            get_multilocation_temperature_forecasts_from_metadata, dfm,
            timespan, weather_api)
    df_ingestion: IngestmentOutput = path_1_task.result()
    df_temperature: pd.DataFrame = path_2_task.result()

    # Step 3: Merge routes
    merged_hourly: pd.DataFrame = merge_routes(
        df_ingestion.ingested_hourly_data, df_temperature)

    # Step 4: Enrich
    return enrich_hourly_data(ingestment_output=IngestmentOutput(
        merged_hourly, df_ingestion.ingested_metadata,
        df_ingestion.enrichment_features),
                              timespan=timespan,
                              features=features,
                              prediction=not training)


def _check_types(bq, targets, timespan, weather_api):
    if not isinstance(bq, BigQueryBundle):
        raise TypeError
    if not isinstance(targets, ForecastTargetList):
        raise TypeError
    if not isinstance(timespan, Timespan):
        raise TypeError
    if not isinstance(weather_api, WeatherApiBundle):
        raise TypeError


def enrich_hourly_data(ingestment_output: IngestmentOutput, timespan: Timespan,
                       features: FeatureSelection,
                       prediction: bool) -> pd.DataFrame:
    """
    Adds features (cyclical, holidays, hour-of-the-week average consumption, shifted/delayed consumption, 
    price) to the ingested hourly data. The metadata dataframe needs to be enriched with fylke, 
    as this is needed to add the school holidays.

    :param IngestmentOutput ingestment_output: Output from :py:func:`~forecast_dataprep.functions.main_ingestion_route`
    :param Timespan timespan: Object with the start and end of the time period of interest
    :param FeatureSelection features: Which features to include
    :param bool prediction: If both use_prices and prediction are true, prices will be interpolated/extrapolated
    """

    ingested_hourly_data = add_cyclical_features(
        ingestment_output.ingested_hourly_data)

    if features.prices:
        ingested_hourly_data = add_prices(
            ingested_hourly_data, ingestment_output.enrichment_features.prices,
            prediction)

    if features.delayed_features:
        for delay in TimeConstants.DELAYED_FEATURES:
            ingested_hourly_data = add_delayed_consumption_feature(
                ingested_hourly_data, delay)

    return ingested_hourly_data.sort_index()


def main_ingestion_route(
        raw_metadata: pd.DataFrame,
        model_targets: ForecastTargetList,
        bq: BigQueryBundle,
        timespan: Timespan,
        training: bool,
        features: FeatureSelection,
        prediction_start: Optional[datetime] = None) -> IngestmentOutput:
    """
    This enrichment route is meant to run in parallel with :py:func:`~forecast_dataprep.data_enrichment.temperature.get_multilocation_temperature_forecasts_from_metadata`

    :param pd.DataFrame raw_metadata: Result from :py:func:`~forecast_dataprep.data_fetching.__init__.get_metadata` 
    :param ForecastTargetList model_targets: Object representing desired substations or meteringpoints
    :param BigQueryBundle bq: Object containing the BQ client and the BQ project name
    :param Timespan timespan: Object with the start and end of the time period of interest
    :param bool training: If true, the hourly consumption data will be filtered using certain conditions
    :param FeatureSelection features: Which features to include
    :param datetime prediction_start: Point in time when one wants the prediction to start. Ignored if training
    :returns: IngestmentOutput 
    :raises ValueError: If no (or not enough) consumption data
    """
    dfm_ingested = ingest_metadata_dataframe(raw_metadata)

    dfs = get_dataframes(bq, model_targets, timespan, features)

    if dfs.hourly_consumption is None or dfs.hourly_consumption.empty:
        raise ValueError('No hourly consumption data')

    if training:
        dfs.hourly_consumption = ingest_hourly_consumption_data(
            timespan, dfs.hourly_consumption)
        if dfs.hourly_consumption is None or dfs.hourly_consumption.empty:
            raise ValueError('No hourly consumption data')
    elif not there_is_enough_historical_data(
            dfs.hourly_consumption, TimeConstants.DELAYED_FEATURES,
            TimeConstants.FORECAST_HORIZON, prediction_start):
        raise ValueError('Not enough hourly consumption data')

    return IngestmentOutput(dfs.hourly_consumption, dfm_ingested, dfs.ingested)


def merge_routes(ingested_hourly_data: Optional[pd.DataFrame],
                 temperature_data: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Intermediate stage following data ingestion. 
    
    :param pd.DataFrame ingested_hourly_data: Result from :py:func:`~forecast_dataprep.methods.main_ingestion_route` 
    :param pd.DataFrame temperature_data: Result from :py:func:`~forecast_dataprep.data_enrichment.temperature.get_temperature_forecasts_from_metadata` 
    :returns: pd.DataFrame or None if any of the input dataframes is either empty or None
    """
    if ingested_hourly_data is not None \
        and not ingested_hourly_data.empty and not temperature_data.empty:
        return ingested_hourly_data.reset_index().merge(
            temperature_data.rename(columns={'time': 'measurementTime'}),
            on=['measurementTime', 'modelTargetId'],
            how='outer').set_index('measurementTime')
    return None
