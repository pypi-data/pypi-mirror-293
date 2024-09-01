from pydantic import BaseModel
from typing import Optional, NamedTuple, List
from datetime import time, datetime, date
from enum import Enum
from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path

'''
# class Coordinates(BaseModel):
#     latitude: Optional[float]
#     longitude: Optional[float]
#     timestamp: datetime  # This will be overridden

# class Coordinates_with_timestamps(Coordinates):
#     timestamp: time
#     gap: Optional[bool] = None
'''
class GpsTrackerEvent(str,Enum):
    STAY: str = "Stay"

class ProcessedEvent(BaseModel):
    event_type: GpsTrackerEvent
    from_time: time
    to_time: time
    duration: int

class RawEvent(BaseModel):
    event_type: str
    from_time: str
    to_time: str
    duration: str

class PlaybackSpeed(str,Enum):
    FAST: str = "FAST"
    SLOW: str = "SLOW"

class PlaybackButtons(NamedTuple):
    Play: WebElement
    Pause: WebElement
    Continue: WebElement
'''
# class GpsData(Coordinates_with_timestamps):
#         distance: Optional[float] 
#         direction: Optional[str]
#         speed: Optional[float]
'''
class Taxi(BaseModel):
    number: str
    primary_fleet: str
    rego: str
    rego_expiry: date
    coi_expiry: date
    fleets: str
    conditions: str
    make: str
    model: str
    build_date: str
    pax: int
    validation: Optional[str] = None
    until: Optional[date] = None
    reason: Optional[str] = None

class Driver(BaseModel):
    number: int
    name: str
    greeting: str
    address: str
    suburb: str
    post_code: int
    dob: date
    mobile: str
    city: str
    da_expiry: date
    license_expiry: date
    auth_wheelchair: Optional[bool] = None
    auth_bc: Optional[bool] = None
    auth_redcliffe: Optional[bool] = None
    auth_london: Optional[bool] = None
    auth_mandurah: Optional[bool] = None
    refer_fleet_ops: Optional[bool] = None
    conditions: str
    create_date: date
    first_logon: date
    last_logon: date
    first_operator_logon: date
    logons_for_operator: int
    hours_for_operator: int
    validation_active: Optional[bool] = None
    validation_until: Optional[date] = None
    validation_reason: Optional[str] = None
    
class Shift(BaseModel):
    car_id: Taxi | int
    driver_id: Driver | int
    name: str
    log_on: datetime
    log_off: datetime
    duration: int
    distance: int
    offered: int
    accepted: int
    rejected: int
    recalled: int
    completed: int
    total_fares: float
    total_tolls: float

class Job(BaseModel):
    booking_id: int	
    driver_id: Driver | int
    status: str
    accepted: time
    meter_on: time
    meter_off: time
    pick_up_suburb: str
    destination_suburb: str
    fare: float
    toll: float
    account: Optional[str]
    taxi_id: Taxi | int
    shift_id: Shift | int
'''
# class GpsJob(Job):
#     account: Optional[str] = None
#     meter_on_gps: Optional[Coordinates_with_timestamps] = None
#     meter_off_gps: Optional[Coordinates_with_timestamps] = None

# class Coordinates_with_jobs(Coordinates):
#     job: Job
'''
class TrackerEntry(BaseModel):
    timestamp: time
    distance: float
    latitude: float
    longitude: float
    direction: Optional[str] = None
    speed: Optional[float] = None
    stop_time: Optional[int] = None

class GpsRecord(BaseModel):
    date: date
    kml_file: Optional[Path] = None
    events: Optional[List[ProcessedEvent]] = None
    gps_data: Optional[List[TrackerEntry]] = None