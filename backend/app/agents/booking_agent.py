def handle_flight_booking(trip_memory, selected_option=1):

    flights = trip_memory.get("flight_options", [])

    if not flights:

        return {"type": "booking", "message": "No flight search found."}

    index = selected_option - 1

    if index >= len(flights):

        return {
            "type": "booking",
            "message": f"Option {selected_option} not available.",
        }

    selected_flight = flights[index]

    trip_memory["selected_flight"] = selected_flight

    return {
        "type": "booking_summary",
        "airline": selected_flight.get("airline"),
        "outbound_route": selected_flight.get("outbound_route"),
        "return_route": selected_flight.get("return_route"),
        "departure": selected_flight.get("departure"),
        "arrival": selected_flight.get("arrival"),
        "duration": selected_flight.get("duration"),
        "stops": selected_flight.get("stops"),
        "cabin_class": selected_flight.get("cabin_class"),
        "passengers": selected_flight.get("passengers"),
        "price": selected_flight.get("price"),
        "currency": selected_flight.get("currency"),
        "price_inr": round(float(selected_flight.get("price", 0)) * 105),
    }


def confirm_booking(trip_memory):

    booking = trip_memory.get("selected_flight")

    if not booking:

        return {"type": "booking", "message": "No pending booking found."}

    return {
        "type": "booking_confirmed",
        "flight": booking,
        "message": "Flight booked successfully!",
    }
