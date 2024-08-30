from datetime import datetime, timedelta, timezone
from typing import List, Tuple

from forecast_dataprep.data_models import Timespan

from forecast_dataprep.weather_api.data_models import Location


def get_past_forecasts_payload(timespan: Timespan, locations: List[Location]):
    payload = {
        "startTime":
        timespan.start.isoformat(),
        "endTime":
        timespan.end.isoformat(),
        "coordinates": [{
            "latitude": location.latitude,
            "longitude": location.longitude
        } for location in locations],
        "variables": ["temperature"]
    }

    return payload


def decide_which_weather_api_endpoints_to_call(
    timespan: Timespan,
    max_horizon_into_future: timedelta = timedelta(days=10),
    max_leeway_from_present: timedelta = timedelta(days=1)
) -> Tuple[bool, bool]:
    """
    Decide which Weather API endpoints should be called, based on an input timespan and the current
    time.
    """
    call_api_historical: bool = True
    call_api_latest: bool = True

    tz_aware_now = datetime.now(timezone.utc)

    # If the time span of interest lies in the future, skip irrelevant calls
    if timespan.start - max_leeway_from_present > tz_aware_now:
        call_api_historical = False
        # Far into the future?
        if timespan.start - max_leeway_from_present > tz_aware_now + max_horizon_into_future:
            call_api_latest = False
    # If the time span of interest lies exclusively in the past, skip the call for future forecast
    if timespan.end + max_leeway_from_present < tz_aware_now:
        call_api_latest = False

    return call_api_historical, call_api_latest
