from app.agents.router import detect_intent

from app.agents.flight_agent import handle_flight_query
from app.agents.trip_planner_agent import handle_trip_planning
from app.tools.weather_tool import get_weather
from app.agents.trip_planner_agent import handle_trip_planning
from app.tools.places_tool import (
    get_hotels,
    get_restaurants,
    get_nightlife,
)
from fastapi import FastAPI

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


from database import engine
from models import Base
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas

from typing import Any
import json


from app.tools.weather_tool import get_weather
from app.tools.places_tool import (
    get_hotels,
    get_nightlife,
    get_restaurants,
)


from database import SessionLocal
from models import Booking
from app.services.memory_service import (
    save_memory,
    get_memory,
    get_all_memory,
)
from app.memory.session_memory import (
    get_session,
    update_session,
    clear_session,
)

Base.metadata.create_all(bind=engine)


app = FastAPI(title="AgenticTrip API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):

    role: str
    content: Any


class ChatRequest(BaseModel):

    message: str

    history: list[Message] = []

    session_id: str


class BookingRequest(BaseModel):

    flight: dict

    passenger: dict


class FlightResult(BaseModel):

    airline: str
    origin: str
    destination: str
    departure: str
    arrival: str
    price: str
    currency: str


@app.get("/")
def home():

    return {"message": "Welcome to AgenticTrip"}


@app.post("/chat")
def chat(request: ChatRequest):

    try:

        user_input = request.message
        session_id = request.session_id

        session = get_session(session_id)

        intent = detect_intent(user_input)

        print("FINAL INTENT:", intent)

        result = None

        # FLIGHTS
        if intent == "flight":
            result = handle_flight_query(user_input, session)

        # HOTELS
        elif intent == "hotels":
            result = handle_hotel_query(user_input, session)

        # TRIP PLANNING
        elif intent == "trip_planning":
            result = handle_trip_planning(user_input, session)

        else:
            result = f"Intent '{intent}' is not implemented yet."

        return {"response": result}

    except Exception as e:
        print("CHAT ERROR:", str(e))
        return {"error": str(e)}

    except Exception as e:

        import traceback

        print("CHAT ERROR:")
        print(str(e))

        traceback.print_exc()

        return {"error": str(e)}


@app.post("/confirm-booking")
def confirm_booking(request: BookingRequest):

    db = SessionLocal()

    try:

        flight = request.flight
        passenger = request.passenger

        import random

        pnr = "AGT" + str(random.randint(100000, 999999))

        booking_id = "BK" + str(random.randint(10000, 99999))

        currency = flight.get("currency")

        price = float(flight.get("price", 0))

        # Convert GBP → INR
        if currency == "GBP":

            price = round(price * 105)

        booking = Booking(
            passenger_name=passenger.get("name"),
            email=passenger.get("email"),
            airline=flight.get("airline"),
            route=flight.get("outbound_route"),
            departure=flight.get("departure"),
            arrival=flight.get("arrival"),
            price=str(price),
            pnr=pnr,
            booking_id=booking_id,
        )

        db.add(booking)

        db.commit()

        db.refresh(booking)

        return {
            "success": True,
            "pnr": pnr,
            "booking_id": booking_id,
            "message": "Booking confirmed successfully",
        }

    finally:

        db.close()


@app.get("/bookings")
def get_bookings():

    db = SessionLocal()

    try:

        bookings = db.query(Booking).all()

        results = []

        for booking in bookings:

            results.append(
                {
                    "id": booking.id,
                    "passenger_name": booking.passenger_name,
                    "email": booking.email,
                    "airline": booking.airline,
                    "route": booking.route,
                    "departure": booking.departure,
                    "arrival": booking.arrival,
                    "price": booking.price,
                    "pnr": booking.pnr,
                    "booking_id": booking.booking_id,
                }
            )

        return {
            "success": True,
            "results": results,
        }

    finally:

        db.close()


@app.get("/download-ticket/{booking_id}")
def download_ticket(booking_id: str):

    db = SessionLocal()

    try:

        booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()

        if not booking:

            return {
                "success": False,
                "message": "Booking not found",
            }

        pdf_path = f"ticket_{booking_id}.pdf"

        c = canvas.Canvas(pdf_path)

        # HEADER
        c.setFont("Helvetica-Bold", 24)
        c.drawString(180, 800, "AgenticTrip Ticket")

        # BOOKING INFO
        c.setFont("Helvetica", 14)

        c.drawString(50, 740, f"Passenger: {booking.passenger_name}")

        c.drawString(50, 710, f"Airline: {booking.airline}")

        c.drawString(50, 680, f"Route: {booking.route}")

        c.drawString(50, 650, f"Departure: {booking.departure}")

        c.drawString(50, 620, f"Arrival: {booking.arrival}")

        c.drawString(50, 590, f"PNR: {booking.pnr}")

        c.drawString(50, 560, f"Booking ID: {booking.booking_id}")

        c.drawString(50, 530, f"Price: INR {booking.price}")

        # FOOTER
        c.setFont("Helvetica-Oblique", 12)

        c.drawString(50, 480, "Thank you for booking with AgenticTrip ✈")

        c.save()

        return FileResponse(
            path=pdf_path,
            filename=pdf_path,
            media_type="application/pdf",
        )

    finally:

        db.close()


@app.get("/memory")
def view_memory():

    return get_all_memory()
