"""
This module is an API wrapper for Weather API, tailored to the needs of the load forecast API
"""
from concurrent.futures import ThreadPoolExecutor
from typing import Any, List, Optional, Tuple

from http import HTTPStatus

import numpy as np
import pandas as pd
from pydantic import ValidationError
import requests
from forecast_dataprep.data_models import Timespan
from forecast_dataprep.weather_api.common import decide_which_weather_api_endpoints_to_call, get_past_forecasts_payload

from forecast_dataprep.weather_api.data_models import Location, WeatherApiBundle, WeatherModel


def _parse_weather_api_json_response(json_response: Any) -> pd.DataFrame:
    """
    Returns a dataframe with forecast data for a single location.
    Index: UTC timestamps
    temperature: floats
    """
    try:
        parsed: WeatherModel = WeatherModel.parse_obj(
            json_response).coordinates[0].variables[0].data

        parsed_pandas: pd.DataFrame = pd.DataFrame(
            [(_.time, _.value) for _ in parsed],
            columns=['time', 'temperature'])

        parsed_pandas.set_index('time', inplace=True)
        parsed_pandas.index = pd.to_datetime(parsed_pandas.index)
        parsed_pandas.sort_index(inplace=True)

        return parsed_pandas

    except ValidationError:
        raise ValueError('Something went wrong while parsing temperature data')


def _call_weather_api(weather_url: str, payload: dict,
                      credentials: Tuple[str, str]) -> pd.DataFrame:

    response = requests.post(weather_url, json=payload, auth=credentials)
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(
            f'Status code: {str(response.status_code)}\nResponse:{str(response.text)}'
        )
    json_response = response.json()

    return _parse_weather_api_json_response(json_response)


def _add_coordinates_to_dataframe(temperature: pd.DataFrame,
                                  location: Location) -> pd.DataFrame:
    """
    This function adds 2 extra columns with the location information. 
    We'll need them later in the final stage of data enrichment.
    """
    if temperature.empty:
        raise ValueError('No temperature data')

    latitude = pd.Series(index=temperature.index,
                         data=np.full(temperature.shape[0], location.latitude),
                         name='latitude')
    longitude = pd.Series(index=temperature.index,
                          data=np.full(temperature.shape[0],
                                       location.longitude),
                          name='longitude')
    return temperature.merge(latitude, left_index=True,
                             right_index=True).merge(longitude,
                                                     left_index=True,
                                                     right_index=True)


def _get_future_temperature_forecast(
        location: Location, weather_api: WeatherApiBundle) -> pd.DataFrame:
    """
    Gets the latest temperature forecast from Weather API for a given location.     
    """
    payload = {
        "coordinates": [{
            "latitude": location.latitude,
            "longitude": location.longitude
        }],
        "variables": ["temperature"]
    }

    temperature: pd.DataFrame = _call_weather_api(
        weather_api.domain + '/api/Forecasts/Latest', payload,
        weather_api.credentials)

    return _add_coordinates_to_dataframe(temperature, location)


def _get_past_temperature_forecast(
        timespan: Timespan, location: Location,
        weather_api: WeatherApiBundle) -> pd.DataFrame:
    """
    Gets historical temperature forecast data from Weather API, for a given location. 
    """
    payload: dict = get_past_forecasts_payload(timespan=timespan,
                                               locations=[location])
    temperature: pd.DataFrame = _call_weather_api(
        weather_api.domain + '/api/Forecasts', payload,
        weather_api.credentials)

    return _add_coordinates_to_dataframe(temperature, location)


def _get_past_and_future_temperature_forecast(
        timespan: Timespan, location: Location,
        weather_api: WeatherApiBundle) -> pd.DataFrame:
    """
    Get temperature forecast data from Weather API for a given location, for a period of time 
    that lies in both the past and the future.
    """
    with ThreadPoolExecutor() as executor:
        result_historical = executor.submit(_get_past_temperature_forecast,
                                            timespan, location, weather_api)
        result_latest = executor.submit(_get_future_temperature_forecast,
                                        location, weather_api)

    historical = result_historical.result()
    latest = result_latest.result()

    return pd.concat([historical, latest], sort=True).drop_duplicates()


def _get_temperature_forecast(
        timespan: Timespan, location: Location,
        weather_api: WeatherApiBundle) -> Optional[pd.DataFrame]:
    """
    Call Weather API and fetch historical and/or future temperature forecasts.

    :param Timespan timespan: Object with the start and end time
    :param Location location: contains latitude and longitude
    :param WeatherApiBundle weather_api: Weather API info and credentials
    :returns: A dataframe with time, temperature and location, if success
    """

    call_api_historical, call_api_latest = decide_which_weather_api_endpoints_to_call(
        timespan)

    _df: pd.DataFrame

    if call_api_historical and call_api_latest:
        _df = _get_past_and_future_temperature_forecast(
            timespan, location, weather_api)
    elif call_api_historical:
        _df = _get_past_temperature_forecast(timespan, location, weather_api)
    elif call_api_latest:
        _df = _get_future_temperature_forecast(location, weather_api)
    else:
        return None

    return _df[(_df.index.to_pydatetime() >= timespan.start)
               & (_df.index.to_pydatetime() < timespan.end)]


def get_temperature_forecasts(timespan: Timespan, locations: List[Location],
                              weather_api: WeatherApiBundle) -> pd.DataFrame:
    """
    Fetch historical and/or future temperature forecasts for several locations simultaneously.
    Uses a thread pool to run individual requests, one for each location. 
    Consider using the equivalent multilocation method if you have a long list of locations.
    Past and future forecast requests run each in its own thread.

    :param Timespan timespan: Start and end of the prediction/training time interval
    :param list locations: List of objects each containing latitude and longitude
    :param str weather_api: Weather API info and credentials
    :returns: Dataframe with temperature and location, if success
    :raises ValueError: If no temperature data
    :raises RuntimeError: If the Weather API did not return 200    
    """

    with ThreadPoolExecutor() as executor:
        tasks = [
            executor.submit(_get_temperature_forecast, timespan, location,
                            weather_api) for location in locations
        ]

    results = [task.result() for task in tasks]
    dataframes = [
        result for result in results if result is not None and not result.empty
    ]

    if not dataframes:
        raise ValueError('No temperature data')

    return pd.concat(dataframes, sort=True).drop_duplicates()
