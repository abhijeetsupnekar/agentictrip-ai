# backend/app/memory/session_memory.py

session_memory = {}


def get_session(session_id: str):

    if session_id not in session_memory:

        session_memory[session_id] = {
            "source": None,
            "destination": None,
            "departure_date": None,
            "return_date": None,
            "trip_type": "one_way",
            "passengers": 1,
            "cabin": "economy",
            "selected_flight": None,
            "flight_options": [],
            "booking_stage": None,
        }

    return session_memory[session_id]


def update_session(session_id: str, key: str, value):

    session = get_session(session_id)

    session[key] = value


def clear_session(session_id: str):

    if session_id in session_memory:

        del session_memory[session_id]
