import React from "react";

const BookingSummaryCard = ({
    flight,
    passenger,
    onConfirm,
    onCancel,
}) => {

    const generatePrice = () => {
        if (flight.currency === "GBP") {
            return `₹${Math.round(
                parseFloat(flight.price) * 105
            )}`;
        }

        return `${flight.price} ${flight.currency}`;
    };
    const formatDate = (dateString) => {

        return new Date(dateString).toLocaleString(
            "en-IN",
            {
                day: "2-digit",
                month: "short",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit",
                hour12: true,
            }
        );

    };
    return (
        <div className="bg-white/5 border border-white/10 rounded-3xl p-8 mt-6 text-white">

            <h2 className="text-3xl font-bold mb-6">
                ✈ Booking Confirmation
            </h2>

            {/* Flight Details */}
            <div className="mb-6">

                <h3 className="text-xl font-semibold mb-3">
                    Flight Details
                </h3>

                <p>
                    <strong>Airline:</strong> {flight.airline}
                </p>

                <p>
                    <strong>Route:</strong> {flight.outbound_route}
                </p>

                <p>
                    <strong>Departure:</strong> {formatDate(flight.departure)}
                </p>

                <p>
                    <strong>Arrival:</strong> {formatDate(flight.arrival)}
                </p>

                <p>
                    <strong>Cabin:</strong> {flight.cabin_class}
                </p>

                <p>
                    <strong>Passengers:</strong> {flight.passengers}
                </p>

            </div>

            {/* Passenger Details */}
            <div className="mb-6">

                <h3 className="text-xl font-semibold mb-3">
                    Passenger Details
                </h3>

                <p>
                    <strong>Name:</strong> {passenger.name}
                </p>

                <p>
                    <strong>Age:</strong> {passenger.age}
                </p>

                <p>
                    <strong>Gender:</strong> {passenger.gender}
                </p>

                <p>
                    <strong>Email:</strong> {passenger.email}
                </p>

                <p>
                    <strong>Phone:</strong> {passenger.phone}
                </p>

            </div>

            {/* Price */}
            <div className="mb-8">

                <p className="text-3xl font-bold">
                    {generatePrice()}
                </p>

            </div>

            {/* Buttons */}
            <div className="flex gap-4">

                <button
                    onClick={onConfirm}
                    className="bg-white text-black px-6 py-3 rounded-2xl font-semibold hover:bg-gray-200 transition"
                >
                    Confirm Booking
                </button>

                <button
                    onClick={onCancel}
                    className="bg-red-500 px-6 py-3 rounded-2xl font-semibold hover:bg-red-600 transition"
                >
                    Cancel
                </button>

            </div>

        </div>
    );
};

export default BookingSummaryCard;