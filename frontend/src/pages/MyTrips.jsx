import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";

function MyTrips() {

    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        fetchBookings();

    }, []);

    const fetchBookings = async () => {

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/bookings"
            );

            const data = await response.json();

            console.log("BOOKINGS:", data);

            setBookings(data.results || []);

        }

        catch (error) {

            console.log(error);

        }

        finally {

            setLoading(false);

        }

    };

    const formatDate = (dateString) => {

        if (!dateString) return "";

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

        <div className="min-h-screen bg-black text-white">

            <Navbar />

            <div className="max-w-6xl mx-auto px-4 pt-32 pb-12">

                <h1 className="text-4xl font-bold mb-10">

                    ✈ My Trips

                </h1>

                {
                    loading && (

                        <p className="text-gray-400">
                            Loading bookings...
                        </p>

                    )
                }

                {
                    !loading && bookings.length === 0 && (

                        <div className="bg-white/5 border border-white/10 rounded-3xl p-10">

                            <p className="text-xl text-gray-300">

                                No bookings found.

                            </p>

                        </div>

                    )
                }

                <div className="space-y-6">

                    {
                        bookings.map((booking, index) => (

                            <div
                                key={index}
                                className="bg-white/5 border border-white/10 rounded-3xl p-6"
                            >

                                <div className="flex items-center justify-between flex-wrap gap-4">

                                    <div>

                                        <h2 className="text-3xl font-bold">

                                            {booking.airline}

                                        </h2>

                                        <p className="text-gray-400 mt-1">

                                            Passenger: {booking.passenger_name}

                                        </p>

                                    </div>

                                    <div className="text-right">

                                        <p className="text-sm text-gray-400">
                                            Booking ID
                                        </p>

                                        <p className="font-bold">
                                            {booking.booking_id}
                                        </p>

                                    </div>

                                </div>

                                <div className="mt-8 bg-black/30 rounded-2xl p-5">

                                    <div className="flex items-center justify-between">

                                        <div>

                                            <p className="text-4xl font-bold">
                                                {booking.route?.split(" → ")[0]}
                                            </p>

                                            <p className="text-gray-400 mt-2">
                                                {formatDate(booking.departure)}
                                            </p>

                                        </div>

                                        <div className="text-center px-4">

                                            <div className="text-3xl mb-2">
                                                ✈
                                            </div>

                                            <p className="text-green-400">
                                                Confirmed
                                            </p>

                                        </div>

                                        <div className="text-right">

                                            <p className="text-4xl font-bold">
                                                {
                                                    booking.route?.split(" → ")[1]
                                                }
                                            </p>

                                            <p className="text-gray-400 mt-2">
                                                {formatDate(booking.arrival)}
                                            </p>

                                        </div>

                                    </div>

                                </div>

                                <div className="mt-6 flex justify-between flex-wrap gap-4">

                                    <div>

                                        <p className="text-sm text-gray-400">
                                            PNR
                                        </p>

                                        <p className="font-bold text-lg">
                                            {booking.pnr}
                                        </p>

                                    </div>

                                    <div>

                                        <p className="text-sm text-gray-400">
                                            Total Paid
                                        </p>

                                        <p className="font-bold text-2xl text-green-400">

                                            ₹{
                                                Math.round(
                                                    parseFloat(booking.price) * 105
                                                )
                                            }

                                        </p>

                                    </div>

                                </div>

                            </div>

                        ))
                    }

                </div>

            </div>

        </div>

    );

}

export default MyTrips;