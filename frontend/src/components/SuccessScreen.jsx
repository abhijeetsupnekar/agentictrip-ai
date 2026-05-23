import React from "react";
import { motion } from "framer-motion";

const SuccessScreen = ({
    pnr,
    bookingId,
    passenger,
    flight,
    onNewBooking,
}) => {

    return (

        <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="bg-white/5 border border-white/10 rounded-3xl p-8 mt-6 text-white"
        >

            {/* Success Icon */}
            <div className="text-6xl mb-4">
                🎉
            </div>

            {/* Title */}
            <h1 className="text-4xl font-bold mb-2">
                Booking Confirmed!
            </h1>

            <p className="text-gray-400 mb-8">
                Your flight has been booked successfully.
            </p>

            {/* Booking Details */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                <div className="bg-black/30 rounded-2xl p-5">

                    <h2 className="text-2xl font-semibold mb-4">
                        Booking Details
                    </h2>

                    <p>
                        <strong>PNR:</strong> {pnr}
                    </p>

                    <p>
                        <strong>Booking ID:</strong> {bookingId}
                    </p>

                    <p>
                        <strong>Passenger:</strong> {passenger.name}
                    </p>

                </div>

                <div className="bg-black/30 rounded-2xl p-5">

                    <h2 className="text-2xl font-semibold mb-4">
                        Flight Details
                    </h2>

                    <p>
                        <strong>Airline:</strong> {flight.airline}
                    </p>

                    <p>
                        <strong>Route:</strong> {flight.outbound_route}
                    </p>

                    <p>
                        <strong>Cabin:</strong> {flight.cabin_class}
                    </p>

                </div>

            </div>

            <a
                href={`http://127.0.0.1:8000/download-ticket/${bookingId}`}
                target="_blank"
                rel="noreferrer"
                className="inline-block bg-green-500 text-black px-6 py-3 rounded-2xl font-semibold hover:bg-green-400 transition mr-4"
            >
                Download Ticket PDF
            </a>
            {/* Action Button */}
            <button
                onClick={onNewBooking}
                className="mt-8 bg-gradient-to-r from-green-400 to-blue-500 text-black px-6 py-3 rounded-2xl font-semibold hover:scale-105 transition"
            >
                Book Another Trip
            </button>

        </motion.div>

    );

};

export default SuccessScreen;