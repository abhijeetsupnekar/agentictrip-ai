from sqlalchemy import Column, Integer, String
from database import Base


class Booking(Base):

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    passenger_name = Column(String)
    email = Column(String)

    airline = Column(String)

    route = Column(String)

    departure = Column(String)
    arrival = Column(String)

    price = Column(String)

    pnr = Column(String)

    booking_id = Column(String)


class Memory(Base):

    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, index=True)

    memory_key = Column(String)

    memory_value = Column(String)
