"""
This module contains functions with queries against Edna BQ
"""
from datetime import datetime
from typing import Optional

from google.cloud import bigquery
from google.cloud.bigquery.job import QueryJob
import pandas as pd

from forecast_dataprep.data_fetching.data_models import BigQueryBundle
from forecast_dataprep.data_models import ForecastTargetLevel, ForecastTargetList, Timespan
from forecast_dataprep.data_fetching.meteringpoints import get_meteringpoint_hourly_data
from forecast_dataprep.data_fetching.substations import get_substation_hourly_data


def get_hourly_data(
        bq: BigQueryBundle,
        targets: ForecastTargetList,
        timespan: Optional[Timespan] = None) -> Optional[pd.DataFrame]:

    if targets.level == ForecastTargetLevel.METERING_POINT:
        return get_meteringpoint_hourly_data(bq, targets.identifiers, timespan)
    elif targets.level == ForecastTargetLevel.SUBSTATION:
        return get_substation_hourly_data(bq, targets.identifiers, timespan)
    return None


def get_prices(bq: BigQueryBundle, timespan: Timespan):
    """
    Fetch prices.

    :param bool extrapolate: If true, fill out future prices with the prices from the last known day
    """
    query = (
        "SELECT t, AVG(_price) AS price "
        "FROM ( "
        "  SELECT TIMESTAMP_TRUNC(EndTime, HOUR) AS t, Value AS _price "
        f" FROM `{bq.project.name}.{bq.project.prices_dataset}.{bq.project.prices_table}` "
        "  WHERE EndTime < @to_time AND EndTime > @from_time "
        ") "
        "GROUP BY t "
        "ORDER BY t ")

    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("from_time", "TIMESTAMP",
                                      timespan.start),
        bigquery.ScalarQueryParameter("to_time", "TIMESTAMP", timespan.end)
    ])
    query_job: QueryJob = bq.client.query(query, job_config=job_config)

    prices: pd.DataFrame = query_job.result().to_dataframe(
        create_bqstorage_client=False)

    prices.set_index('t', inplace=True)
    prices.sort_index(inplace=True)

    result: pd.DataFrame = _add_empty_rows_for_datapoints_in_the_future(
        prices, timespan.start, timespan.end)

    return result


def _add_empty_rows_for_datapoints_in_the_future(prices: pd.DataFrame,
                                                 from_time: datetime,
                                                 to_time: datetime):

    from_time = from_time.replace(minute=0, second=0, microsecond=0)
    to_time = to_time.replace(minute=0, second=0, microsecond=0)

    required_times = pd.DataFrame(
        pd.date_range(from_time, to_time, freq='1H', tz='utc')).set_index(0)
    required_times.index.name = 't'
    required_times.sort_index(inplace=True)
    result = prices.merge(required_times,
                          left_index=True,
                          right_index=True,
                          how='outer')
    result.index.name = 'measurementTime'
    return result
