"""
This module has the highest level functions for fetching data from Edna BQ
"""
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import pandas as pd

from forecast_dataprep.data_fetching.data_models import BigQueryBundle
from forecast_dataprep.data_models import Dataframes, EnrichmentFeaturesBundle, FeatureSelection, ForecastTargetList, ForecastTargetLevel, Timespan
from forecast_dataprep.data_fetching.common import get_hourly_data, get_prices
from forecast_dataprep.data_fetching.meteringpoints import get_meteringpoint_metadata
from forecast_dataprep.data_fetching.substations import get_substation_metadata


def get_dataframes(bq: BigQueryBundle, targets: ForecastTargetList,
                   timespan: Timespan,
                   features: FeatureSelection) -> Dataframes:
    """
    Query Edna tables and fetch data, returned as dataframes.
    The substation/meteringpoint metadata is not part of this group of queries, in order to 
    optimise the overall execution order.

    :param FeatureSelection features: Which features to include
    """
    with ThreadPoolExecutor(max_workers=5) as executor:
        dfh = executor.submit(get_hourly_data, bq, targets, timespan)
        dfp = executor.submit(get_prices, bq,
                              timespan) if features.prices else None

        dfh = dfh.result()
        dfp = dfp.result() if dfp is not None else None

        return Dataframes(
            dfh,
            EnrichmentFeaturesBundle(
                dfp if dfp is not None else pd.DataFrame()))


def get_metadata(bq: BigQueryBundle,
                 targets: ForecastTargetList) -> Optional[pd.DataFrame]:
    """
    Get meteringpoint/substation metadata. 
    The result contains columns latitude and longitude that are needed to get the right forecast
    data from Weather API. It also contains column postalCode, which is needed to enrich with the
    location-dependant school holidays feature.
    """
    if targets.level == ForecastTargetLevel.METERING_POINT:
        return get_meteringpoint_metadata(bq, targets.identifiers)
    elif targets.level == ForecastTargetLevel.SUBSTATION:
        return get_substation_metadata(bq, targets.identifiers)
    return None
