from concurrent.futures import ThreadPoolExecutor
from typing import Any, List, Optional, Tuple

from http import HTTPStatus

import pandas as pd
from pydantic import ValidationError
import requests
from forecast_dataprep.data_models import Timespan
from forecast_dataprep.weather_api.common import decide_which_weather_api_endpoints_to_call, get_past_forecasts_payload

from forecast_dataprep.weather_api.data_models import Location, WeatherApiBundle, WeatherModel


def _parse_multilocation_weatherapi_json_response(
        json_response: Any) -> pd.DataFrame:
    """
    Returns a dataframe without a set index (i.e. with a RangeIndex object) and columns: 
    latitude: float
    longitude: float
    time: datetime UTC
    temperature: float
    """
    try:
        parsed: WeatherModel = WeatherModel.parse_obj(json_response)

        multi_location_temp = pd.DataFrame([{
            'latitude': c.latitude,
            'longitude': c.longitude,
            'time': datapoint.time,
            'temperature': datapoint.value
        } for c in parsed.coordinates for datapoint in c.variables[0].data])

        multi_location_temp.time = pd.to_datetime(multi_location_temp.time)

        return multi_location_temp

    except ValidationError:
        raise ValueError('Something went wrong while parsing temperature data')


def _call_multilocation_weather_api(
        weather_url: str, payload: dict,
        credentials: Tuple[str, str]) -> pd.DataFrame:

    response = requests.post(weather_url, json=payload, auth=credentials)
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(
            f'Status code: {str(response.status_code)}\nResponse:{str(response.text)}'
        )
    json_response = response.json()

    return _parse_multilocation_weatherapi_json_response(json_response)


def _get_multilocation_future_temperature_forecast(
        locations: List[Location],
        weather_api: WeatherApiBundle) -> pd.DataFrame:
    """
    Gets the latest temperature forecast from Weather API for multiple locations.     
    """
    payload = {
        "coordinates": [{
            "latitude": location.latitude,
            "longitude": location.longitude
        } for location in locations],
        "variables": ["temperature"]
    }

    temperature: pd.DataFrame = _call_multilocation_weather_api(
        weather_api.domain + '/api/Forecasts/Latest', payload,
        weather_api.credentials)

    return temperature


def _get_multilocation_past_temp_forecasts(
        timespan: Timespan, locations: List[Location],
        weather_api: WeatherApiBundle) -> pd.DataFrame:
    """
    Gets historical temperature forecast data from Weather API, for multiple locations. 
    """
    payload: dict = get_past_forecasts_payload(timespan=timespan,
                                               locations=locations)

    temperature: pd.DataFrame = _call_multilocation_weather_api(
        weather_api.domain + '/api/Forecasts', payload,
        weather_api.credentials)

    return temperature


def _get_multilocation_past_and_future_temperature_forecast(
        timespan: Timespan, locations: List[Location],
        weather_api: WeatherApiBundle) -> pd.DataFrame:
    """
    Get temperature forecast data from Weather API for multiple locations, for a period of time 
    that lies in both the past and the future.
    """
    with ThreadPoolExecutor() as executor:
        result_historical = executor.submit(
            _get_multilocation_past_temp_forecasts, timespan, locations,
            weather_api)
        result_latest = executor.submit(
            _get_multilocation_future_temperature_forecast, locations,
            weather_api)

    historical = result_historical.result()
    latest = result_latest.result()

    return pd.concat([historical, latest], sort=True).drop_duplicates()


def get_multilocation_temperature_forecasts(
        timespan: Timespan, locations: List[Location],
        weather_api: WeatherApiBundle) -> Optional[pd.DataFrame]:
    """
    Call Weather API and fetch historical and/or future temperature forecasts.
    Runs one request for all locations.
    Past and future forecast run each in its own thread.

    :param Timespan timespan: Object with the start and end time
    :param List[Locations] locations: contains latitude & longitude pairs
    :param WeatherApiBundle weather_api: Weather API info and credentials
    :returns: A dataframe with time, temperature and location, if success
    :raises ValueError: If no temperature data
    :raises RuntimeError: If the Weather API did not return 200
    """

    call_api_historical, call_api_latest = decide_which_weather_api_endpoints_to_call(
        timespan)

    _df: pd.DataFrame

    if call_api_historical and call_api_latest:
        _df = _get_multilocation_past_and_future_temperature_forecast(
            timespan, locations, weather_api)
    elif call_api_historical:
        _df = _get_multilocation_past_temp_forecasts(timespan, locations,
                                                     weather_api)
    elif call_api_latest:
        _df = _get_multilocation_future_temperature_forecast(
            locations, weather_api)
    else:
        return None

    # Timespan must be timezone-aware
    result: pd.DataFrame = _df[(_df.time >= timespan.start)
                               & (_df.time < timespan.end)]

    if result.empty:
        raise ValueError('No temperature data')

    return result.drop_duplicates()
