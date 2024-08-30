"""
This module contains functions with queries against Edna BQ, specific to substations
"""
from typing import List, Optional

from google.cloud import bigquery
from google.cloud.bigquery.job import QueryJob
import pandas as pd

from forecast_dataprep.data_fetching.data_models import BigQueryBundle
from forecast_dataprep.data_models import Timespan


def get_substation_hourly_data(
        bq: BigQueryBundle,
        substations: List[str],
        timespan: Optional[Timespan] = None) -> pd.DataFrame:
    """
    Query and fetch historical hourly consumption for the substations selected.
    :params BigQueryBundle bq: object with a BigQuery client and project info
    """
    query = (
        "SELECT trafoId AS modelTargetId, measurementTime, energyWh "
        f"FROM `{bq.project.name}.{bq.project.dataset}.{bq.project.substation_hourly}` "
        "WHERE trafoId IN UNNEST(@trafo) "
        f"{'AND measurementTime >= @from_time AND measurementTime <= @to_time ' if timespan is not None else ''}"
        "ORDER BY trafoId DESC, measurementTime DESC ")

    query_parameters: list = [
        bigquery.ArrayQueryParameter("trafo", "STRING", substations)
    ]
    if timespan is not None:
        query_parameters.append(
            bigquery.ScalarQueryParameter("from_time", "TIMESTAMP",
                                          timespan.start))
        query_parameters.append(
            bigquery.ScalarQueryParameter("to_time", "TIMESTAMP",
                                          timespan.end))

    job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
    query_job: QueryJob = bq.client.query(query, job_config=job_config)

    result: pd.DataFrame = query_job.result().to_dataframe(
        create_bqstorage_client=False)
    result.set_index('measurementTime', inplace=True)
    return result


def get_substation_metadata(bq: BigQueryBundle,
                            substation: List[str]) -> pd.DataFrame:
    query = (
        "SELECT trafoId AS modelTargetId, latitude, longitude, municipalityNo "
        f"FROM `{bq.project.name}.{bq.project.dataset}.{bq.project.substation_metadata}` "
        "WHERE trafoId IN UNNEST(@trafo) ")

    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ArrayQueryParameter("trafo", "STRING", substation)
    ])
    query_job: QueryJob = bq.client.query(query, job_config=job_config)

    result = query_job.result().to_dataframe(create_bqstorage_client=False)
    return result
