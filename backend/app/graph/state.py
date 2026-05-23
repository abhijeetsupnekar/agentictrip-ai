from typing import TypedDict, Optional, List
from typing_extensions import Annotated

from operator import add


class AgentState(TypedDict):

    user_input: str

    intent: Optional[str]

    source: Optional[str]

    destination: Optional[str]

    departure_date: Optional[str]

    passengers: Optional[int]

    cabin: Optional[str]

    flights: Optional[List]

    hotel_results: Optional[list]

    selected_flight: Optional[dict]

    booking_status: Optional[str]

    messages: Annotated[List[str], add]

    selected_option: Optional[int]

    booking_details: Optional[dict]

    ticket_generated: Optional[bool]

    workflow_stage: Optional[str]

    recommended_hotels: Optional[list]

    weather_info: Optional[dict]

    nightlife_info: Optional[dict]

    trip_plan: Optional[str]
