from pydantic import BaseModel
from typing import Optional, NamedTuple, List
from typing import Final as Constant
from datetime import time, datetime, date
from enum import Enum
from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path

class GpsTrackerEvent(str,Enum):
    STAY: Constant[str] = "Stay"

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
    FAST: Constant[str] = "FAST"
    SLOW: Constant[str] = "SLOW"

class PlaybackButtons(NamedTuple):
    Play: WebElement
    Pause: WebElement
    Continue: WebElement

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

class DocketType(str, Enum):
    APP_BOOKING: Constant[str]  = "App booking"
    ACCOUNT: Constant[str] = "BWC Account"
    DVA: Constant[str] = "DVA"
    NDIS: Constant[str] = "NDIS"
    PRE_PAID: Constant[str] = "Pre Paid"
    GROUPS: Constant[str] = "Groups"
    INTERNAL: Constant[str] = "Internal"

class DocketStatus(str, Enum):
    COMPLETED: Constant[str] = "Completed"
    LODGED: Constant[str] = "Lodged"
    LOGGED: Constant[str] = "Logged"
    PAID: Constant[str] = "Paid"
    DISPUTED: Constant[str] = "Disputed"
    FINALISED: Constant[str] = "Finalised"

class Docket(BaseModel):
    docket_date: date
    docket_type: DocketType
    job_number: int
    account_number: str
    order_number: str
    group_number: str 
    start_time: time
    finish_time: time
    passenger_name: str
    pickup_area: str
    destination_area: str
    meter_total: float
    eft_surcharge: float
    extras: float
    paid_by_passenger_tss: float
    amount_owing: float
    car_number: int
    status: DocketStatus
    lodgment_date: date
    statement_date: date

class VoucherType(str, Enum):
    PRE_PAID: Constant[str] = "pre-paid"
    INTERSTATE_TSS: Constant[str] = "Interstate TSS"
    MANUAL_EFT: Constant[str] = "manual EFT"
    MANUAL_TSS: Constant[str] = "manual TSS"

class Voucher(BaseModel):
    voucher_date: date
    car: int
    amount: float
    voucher_number: int
    voucher_type: VoucherType
    status: DocketStatus
    lodgment_date: date | str
    statement_date: date

class CabCharge(BaseModel):
    docket_date: date
    car: int
    amount: float
    reference: int
    status: DocketStatus
    statement: date

class EftStatement(BaseModel):
    statement_ref: 	int
    statement_url: str
    statement_date: date	
    statement_amount: float	
    amount_allocated: float

class StatementType(str, Enum):
    VOUCHER: Constant[str] = "VOU"
    GROUP: Constant[str] = "GRP"
    DVA: Constant[str] = "DV2"
    ACCOUNT: Constant[str] = "AC"
    NDIS: Constant[str] = "NDI"

class DocketStatement(BaseModel):
    statement_date: date
    statement_url: str
    type: StatementType
    statement_amount: float	
    amount_allocated: float
    statement_ref: str

class PaperDocketStatus(str, Enum):
    PENDING: Constant[str] = "Pending"
    POSTED: Constant[str] = "Posted"

class GroupStatement(BaseModel):
    statement_date: date
    amount: float
    status: PaperDocketStatus