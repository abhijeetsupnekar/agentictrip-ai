def confirm_booking(memory):

    booking = memory.get(
        "pending_booking"
    )

    if not booking:

        return {

            "type": "confirmation",

            "message":
                "No pending booking found."

        }

    # SIMULATED BOOKING SUCCESS

    return {

        "type": "confirmation",

        "message": (
            f"✅ Flight booked successfully!\n\n"
            f"{booking['airline']}\n"
            f"{booking['origin']} → "
            f"{booking['destination']}\n"
            f"Price: "
            f"{booking['price']} "
            f"{booking['currency']}"
        )

    }