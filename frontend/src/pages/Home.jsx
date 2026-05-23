import { useState, useEffect } from "react";
import { useRef } from "react";
import ReactMarkdown from "react-markdown";
import Navbar from "../components/Navbar";
import PassengerForm from "../components/PassengerForm";
import BookingSummaryCard from "../components/BookingSummaryCard";
import SuccessScreen from "../components/SuccessScreen";
import { motion } from "framer-motion";
import TypingIndicator from "../components/TypingIndicator";




function Home() {

  const [selectedFlight, setSelectedFlight] = useState(null);
  const [bookingStage, setBookingStage] = useState("search");
  const [passengerData, setPassengerData] = useState(null);

  const [message, setMessage] = useState("");

  const [loading, setLoading] = useState(false);

  const [pnr, setPnr] = useState("");
  const [bookingId, setBookingId] = useState("");
  const sessionIdRef = useRef(crypto.randomUUID());
  const [messages, setMessages] = useState([]);




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

  const formatCurrency = (value) => {

    if (!value) return "₹0";

    const cleaned = String(value)
      .replace(/[^\d,]/g, "");

    const number = parseInt(
      cleaned.replace(/,/g, "")
    );

    return !isNaN(number)
      ? "₹" + number.toLocaleString()
      : value;

  };

  const formatDuration = (duration) => {

    if (!duration) return "";

    const match = duration.match(
      /P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?/
    );

    if (!match) return duration;

    const days = match[1];
    const hours = match[2];
    const minutes = match[3];

    let result = "";

    if (days) result += `${days}d `;
    if (hours) result += `${hours}h `;
    if (minutes) result += `${minutes}m`;

    return result.trim();

  };


  const getAirlineLogo = (airline) => {

    const logos = {
      "Duffel Airways": "/logos/duffelairways.png",
      "Air India": "/logos/airindia.png",

      "British Airways": "/logos/britishairways.png",

      "Emirates": "/logos/emirates.png",

      "IndiGo": "/logos/indigo.png",

      "Qantas": "/logos/qantas.png",

      "Qatar Airways": "/logos/qatar.png",

    };

    return logos[airline] || "/logos/default.png";

  };

  const handleSubmit = async () => {

    if (!message.trim()) return;

    const currentMessage = message;

    const userMessage = {
      role: "user",
      content: currentMessage,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);

    setMessage("");

    try {

      setLoading(true);

      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/chat`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            message: currentMessage,
            session_id: sessionIdRef.current,
          }),
        }
      );

      const data = await response.json();

      const assistantMessage = {
        role: "assistant",
        content: data.response,
      };

      setMessages((prev) => [
        ...prev,
        assistantMessage,
      ]);

    }

    catch (error) {

      console.log(error);

    }

    finally {

      setLoading(false);

    }

  };

  const handleKeyDown = (e) => {

    if (e.key === "Enter") {
      handleSubmit();
    }

  };

  const renderAssistantResponse = (content) => {

    console.log(typeof content);
    console.log(content);

    console.log("RENDER CONTENT:", content);

    // ERROR
    if (content?.type === "error") {

      return (

        <div>

          <h2 className="text-3xl font-bold mb-6 text-red-400">

            ❌ Error

          </h2>

          <div className="bg-red-500/10 border border-red-500/20 rounded-2xl p-5">

            <p className="text-lg">

              {content.message}

            </p>

          </div>

        </div>

      );

    }

    // WEATHER
    if (content?.type === "weather") {

      return (

        <div>

          <h2 className="text-3xl font-bold capitalize">

            {content.destination}

          </h2>

          <div className="mt-6 bg-white/5 rounded-2xl p-5 border border-white/10">

            <h3 className="text-xl font-semibold mb-4">

              🌤 Live Weather

            </h3>

            <p className="mb-2">

              Temperature:
              {" "}
              {content.weather.temperature}°C

            </p>

            <p className="mb-2">

              Condition:
              {" "}
              {content.weather.condition}

            </p>

            <p>

              Humidity:
              {" "}
              {content.weather.humidity}%

            </p>

          </div>

        </div>

      );

    }

    // HOTELS
    if (content?.type === "hotels") {

      return (

        <div>

          <h2 className="text-3xl font-bold mb-6">

            🏨 Hotels

          </h2>

          <div className="space-y-4">

            {
              content.results.map((hotel, i) => (

                <div
                  key={i}
                  className="bg-white/5 rounded-2xl p-5 border border-white/10"
                >

                  <h3 className="text-2xl font-bold">

                    {hotel.name}

                  </h3>

                  <p className="text-green-400 mt-2">

                    ⭐ {hotel.rating}

                  </p>

                  <p className="text-gray-400 mt-2">

                    {hotel.address}

                  </p>

                </div>

              ))
            }

          </div>

        </div>

      );

    }

    // RESTAURANTS
    if (content?.type === "restaurants") {

      return (

        <div>

          <h2 className="text-3xl font-bold mb-6">

            🍽 Restaurants

          </h2>

          <div className="space-y-4">

            {
              content.results.map((restaurant, i) => (

                <div
                  key={i}
                  className="bg-white/5 rounded-2xl p-5 border border-white/10"
                >

                  <h3 className="text-2xl font-bold">

                    {restaurant.name}

                  </h3>

                  <p className="text-green-400 mt-2">

                    ⭐ {restaurant.rating}

                  </p>

                  <p className="text-gray-400 mt-2">

                    {restaurant.address}

                  </p>

                </div>

              ))
            }

          </div>

        </div>

      );

    }
    // NIGHTLIFE
    if (content?.type === "nightlife") {

      return (

        <div>

          <h2 className="text-3xl font-bold mb-6">

            🌃 Nightlife

          </h2>

          <div className="space-y-4">

            {
              content.results.map((place, i) => (

                <div
                  key={i}
                  className="bg-white/5 rounded-2xl p-5 border border-white/10"
                >

                  <h3 className="text-2xl font-bold">

                    {place.name}

                  </h3>

                  <p className="text-green-400 mt-2">

                    ⭐ {place.rating}

                  </p>

                  <p className="text-gray-400 mt-2">

                    {place.address}

                  </p>

                </div>

              ))
            }

          </div>

        </div>

      );

    }
    if (
      content?.booking_status === "confirmed"
    ) {

      return (

        <div>

          <div
            style={{
              background: "#111",
              borderRadius: "20px",
              padding: "20px",
              marginBottom: "20px",
              border: "1px solid #2a2a2a",
            }}
          >

            <h2
              style={{
                color: "white",
                marginBottom: "16px",
              }}
            >
              ⚡ Agent Activity
            </h2>

            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "10px",
              }}
            >

              {content.messages?.map(
                (activity, index) => (

                  <div
                    key={index}

                    style={{
                      background: "#1a1a1a",
                      padding: "10px 14px",
                      borderRadius: "10px",
                      color: "#00ff88",
                    }}
                  >
                    ✓ {activity}
                  </div>

                )
              )}

            </div>

          </div>

          <div
            className="bg-green-500/10 border border-green-500/20 rounded-2xl p-6"
          >

            <h2 className="text-3xl font-bold text-green-400 mb-4">

              ✅ Booking Confirmed

            </h2>

            <p className="text-lg text-white">

              Your flight booking has been confirmed successfully.

            </p>

          </div>

        </div>

      );

    }
    // LANGGRAPH FLIGHTS

    if (
      Array.isArray(content?.flights) &&
      content.flights.length > 0 &&
      content.workflow_stage === "waiting_for_selection"
    ) {
      console.log("FLIGHT CONTENT:", content);
      return (

        <div>

          {/* AGENT ACTIVITY */}

          {content.messages && (

            <div
              style={{
                background: "#111",
                borderRadius: "20px",
                padding: "20px",
                marginBottom: "20px",
                border: "1px solid #2a2a2a",
              }}
            >

              <h2
                style={{
                  color: "white",
                  marginBottom: "16px",
                }}
              >
                ⚡ Agent Activity
              </h2>

              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "10px",
                }}
              >

                {content.messages.map(
                  (activity, index) => (

                    <div
                      key={index}

                      style={{
                        background: "#1a1a1a",
                        padding: "10px 14px",
                        borderRadius: "10px",
                        color: "#00ff88",
                      }}
                    >
                      ✓ {activity}
                    </div>

                  )
                )}

              </div>

            </div>

          )}

          {/* FLIGHT CARDS */}

          <div className="space-y-4">

            {content.flights.map((flight, i) => (

              <div
                key={i}
                className="bg-white/5 rounded-2xl p-5 border border-white/10"
              >

                <p className="text-sm text-gray-400 mb-2">
                  Option {i + 1}
                </p>

                <h2 className="text-2xl font-bold">
                  {flight.airline}
                </h2>

                <p className="text-gray-400 mt-2">
                  {flight.outbound_route}
                </p>

                <p className="text-gray-400 mt-2">
                  Departure: {formatDate(flight.departure)}
                </p>

                <p className="text-green-400 text-2xl font-bold mt-4">

                  {
                    flight.currency === "GBP"

                      ? `₹${Math.round(
                        parseFloat(flight.price) * 105
                      )} (${flight.price} GBP)`

                      : `${flight.price} ${flight.currency}`
                  }

                </p>

              </div>

            ))}

          </div>

        </div>

      );
    }

    // SIMPLE FLIGHT RESULTS

    if (
      content?.type === "flights" &&
      Array.isArray(content.results)
    ) {

      return (

        <div>

          <h2 className="text-3xl font-bold mb-6">
            ✈ Available Flights
          </h2>

          <div className="space-y-4">

            {content.results.map((flight, i) => (

              <motion.div
                key={i}

                initial={{ opacity: 0, y: 20 }}

                animate={{ opacity: 1, y: 0 }}

                className="bg-white/5 rounded-2xl p-5 border border-white/10"
              >

                <p className="text-sm text-gray-400 mb-2">
                  Option {i + 1}
                </p>
                <div
                  className="
    flex items-center justify-between
    mt-8
    pt-6
    border-t border-white/10
  "
                >

                  <div>

                    <p className="text-sm text-gray-400 mb-1">
                      Total Fare
                    </p>

                    <p
                      className="
        text-5xl
        font-black

        bg-gradient-to-r
        from-green-400
        to-emerald-300

        bg-clip-text
        text-transparent
      "
                    >

                      {
                        flight.currency === "GBP"

                          ? `₹${Math.round(
                            parseFloat(flight.price) * 105
                          )}`

                          : `${flight.price} ${flight.currency}`
                      }

                    </p>

                  </div>

                  <button
                    onClick={() => {

                      setSelectedFlight(flight);

                      setBookingStage("passenger_form");

                      window.scrollTo({
                        top: document.body.scrollHeight,
                        behavior: "smooth",
                      });

                    }}

                    className="
      px-8 py-4

      rounded-2xl

      bg-white
      text-black

      font-bold
      text-lg

      hover:scale-105
      hover:bg-gray-200

      transition-all
      duration-300

      shadow-xl
    "
                  >

                    Book Now

                  </button>

                </div>
                <div className="flex items-center gap-4 mb-4">

                  <img
                    src={getAirlineLogo(flight.airline)}
                    alt={flight.airline}
                    className="max-h-12 object-contain"

                    onError={(e) => {

                      e.target.onerror = null;

                      e.target.src = "/logos/default.png";

                    }}
                  />

                  <div>

                    <h2 className="text-2xl font-bold">
                      {flight.airline}
                    </h2>

                    <p className="text-gray-400">
                      {flight.outbound_route}
                    </p>

                  </div>

                </div>

                <div className="grid grid-cols-2 gap-4 mt-4">

                  <div
                    className="
    bg-black/30
    border border-white/5
    rounded-2xl
    p-4
  "
                  >

                    <p className="text-gray-400 text-sm">
                      Departure
                    </p>

                    <p className="font-semibold">
                      {formatDate(flight.departure)}
                    </p>

                  </div>

                  <div
                    className="
    bg-black/30
    border border-white/5
    rounded-2xl
    p-4
  "
                  >

                    <p className="text-gray-400 text-sm">
                      Arrival
                    </p>

                    <p className="font-semibold">
                      {formatDate(flight.arrival)}
                    </p>

                  </div>

                  <div
                    className="
    bg-black/30
    border border-white/5
    rounded-2xl
    p-4
  "
                  >

                    <p className="text-gray-400 text-sm">
                      Duration
                    </p>

                    <p className="font-semibold">
                      {formatDuration(flight.duration)}
                    </p>

                  </div>

                  <div
                    className="
    bg-black/30
    border border-white/5
    rounded-2xl
    p-4
  "
                  >

                    <p className="text-gray-400 text-sm">
                      Stops
                    </p>

                    <p className="font-semibold">
                      {flight.stops}
                    </p>

                  </div>

                </div>



              </motion.div>

            ))}

          </div>

        </div>

      );

    }
    // BOOKING
    if (content?.type === "booking") {

      return (

        <div>

          <h2 className="text-3xl font-bold mb-6">

            ✅ Booking Assistant

          </h2>

          <div className="bg-white/5 rounded-2xl p-5 border border-white/10">

            <p className="text-xl font-semibold">

              {content.message}

            </p>

          </div>

        </div>

      );

    }

    // CONFIRMATION
    if (content?.type === "confirmation") {

      return (

        <div>

          <h2 className="text-3xl font-bold mb-6">

            🎉 Booking Confirmed

          </h2>

          <div className="bg-white/5 rounded-2xl p-5 border border-white/10">

            <p className="text-xl whitespace-pre-line">

              {content.message}

            </p>

          </div>

        </div>

      );

    }




    // LANGGRAPH TRIP PLAN

    if (content?.type === "trip_plan") {

      const data = content.data;

      return (

        <div className="space-y-6">

          {/* HEADER */}

          <div
            className="
          bg-gradient-to-r
          from-blue-500/10
          to-purple-500/10

          border border-white/10

          rounded-3xl
          p-6
        "
          >

            <h1 className="text-4xl font-black text-white">
              🌍 {data.destination} Trip
            </h1>

          </div>

          {/* STAY + BUDGET */}

          <div className="grid md:grid-cols-2 gap-5">

            <div
              className="
            bg-gradient-to-br from-white/10 to-white/5
            border border-white/10
            rounded-3xl
            p-6
          "
            >

              <h2 className="text-2xl font-bold mb-4">
                🏨 Best Areas To Stay
              </h2>

              <div className="space-y-3">

                {data.best_areas_to_stay.map((area, i) => (

                  <div
                    key={i}
                    className="
                  bg-black/30
                  rounded-2xl
                  p-4
                "
                  >
                    {area}
                  </div>

                ))}

              </div>

            </div>

            <div
              className="
            bg-white/5
            border border-white/10
            rounded-3xl
            p-6
          "
            >

              <h2 className="text-2xl font-bold mb-4">
                💰 Estimated Budget
              </h2>

              <div className="space-y-3">

                <div className="bg-black/30 rounded-2xl p-4">
                  Budget: {data.estimated_budget.budget}
                </div>

                <div className="bg-black/30 rounded-2xl p-4">
                  Mid-range: {data.estimated_budget.mid_range}
                </div>

                <div className="bg-black/30 rounded-2xl p-4">
                  Luxury: {data.estimated_budget.luxury}
                </div>

              </div>

            </div>

          </div>

          {/* DAY CARDS */}

          <div className="space-y-6">

            {data.days.map((day, i) => (

              <motion.div
                key={i}

                initial={{ opacity: 0, y: 20 }}

                animate={{ opacity: 1, y: 0 }}
                whileHover={{
                  y: -4,
                }}
                className="
              bg-white/5
              border border-white/10
              rounded-3xl
              p-6
            "
              >

                <h2 className="text-3xl font-black mb-2">
                  📅 Day {day.day}
                </h2>

                <p className="text-xl text-gray-300 mb-6">
                  {day.title}
                </p>

                <div className="grid md:grid-cols-3 gap-5">

                  {/* MORNING */}

                  <div className="bg-yellow-500/10 rounded-2xl p-5">

                    <h3 className="text-2xl font-black mb-4">
                      🌅 Morning
                    </h3>

                    <div className="space-y-3">

                      {day.morning.map((item, idx) => (

                        <div key={idx}>
                          • {item}
                        </div>

                      ))}

                    </div>

                  </div>

                  {/* AFTERNOON */}

                  <div className="bg-orange-500/10 rounded-2xl p-5">

                    <h3 className="text-xl font-bold mb-4">
                      ☀ Afternoon
                    </h3>

                    <div className="space-y-3">

                      {day.afternoon.map((item, idx) => (

                        <div key={idx}>
                          • {item}
                        </div>

                      ))}

                    </div>

                  </div>

                  {/* EVENING */}

                  <div className="bg-blue-500/10 rounded-2xl p-5">

                    <h3 className="text-xl font-bold mb-4">
                      🌙 Evening
                    </h3>

                    <div className="space-y-3">

                      {day.evening?.length > 0 ? (

                        day.evening.map((item, idx) => (

                          <div key={idx}>
                            • {item}
                          </div>

                        ))

                      ) : (

                        <p className="text-gray-500 italic">
                          No evening activities planned.
                        </p>

                      )}

                    </div>

                  </div>

                </div>

              </motion.div>

            ))}

          </div>

        </div>

      );

    }

    // DEFAULT STRING / ITINERARY
    return (

      <div className="bg-white/5 border border-white/10 rounded-2xl p-5">

        <pre className="whitespace-pre-wrap text-sm overflow-x-auto">
          {JSON.stringify(content, null, 2)}
        </pre>

      </div>

    );

  };

  return (

    <div className="min-h-screen bg-black text-white overflow-x-hidden relative">

      <Navbar />

      <div className="max-w-4xl mx-auto pt-16 pb-40 px-4 sm:px-6">

        <div className="space-y-6">

          {
            messages.map((msg, index) => (

              <div
                key={index}
                className={`flex w-full ${msg.role === "user"
                  ? "justify-end"
                  : "justify-start"
                  }`}
              >

                <div
                  className={`rounded-3xl p-5 sm:p-6 w-full max-w-3xl border overflow-hidden break-words ${msg.role === "user"
                    ? "bg-white text-black"
                    : "bg-white/5 border-white/10 backdrop-blur-xl"
                    }`}
                >

                  {
                    msg.role === "assistant" && (

                      <div className="mb-5">

                        <h3 className="font-semibold">

                          AgenticTrip AI

                        </h3>

                        <p className="text-sm text-gray-400">

                          Travel Planning Assistant

                        </p>

                      </div>

                    )
                  }

                  {
                    msg.role === "assistant"

                      ? renderAssistantResponse(msg.content)

                      : (

                        <div className="prose prose-invert break-words max-w-none">

                          <ReactMarkdown>
                            {msg.content}
                          </ReactMarkdown>

                        </div>

                      )
                  }

                </div>

              </div>

            ))
          }

          {
            loading && (
              <TypingIndicator />
            )
          }

        </div>

      </div>

      {
        bookingStage === "passenger_form" &&
        selectedFlight && (

          <div className="max-w-4xl mx-auto px-4 mb-32">

            <PassengerForm
              onSubmit={(data) => {

                setPassengerData(data);

                setBookingStage("confirmation");

              }}

              onCancel={() => {

                setBookingStage("search");

              }}
            />

          </div>

        )
      }

      {
        bookingStage === "confirmation" &&
        selectedFlight &&
        passengerData && (

          <div className="max-w-4xl mx-auto px-4 mb-32">

            <BookingSummaryCard
              flight={selectedFlight}
              passenger={passengerData}

              onConfirm={async () => {

                try {

                  const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/confirm-booking`,
                    {
                      method: "POST",

                      headers: {
                        "Content-Type": "application/json",
                      },

                      body: JSON.stringify({
                        flight: selectedFlight,
                        passenger: passengerData,
                      }),
                    }
                  );

                  const data = await response.json();

                  console.log("BOOKING RESPONSE:", data);

                  if (data.success) {

                    setPnr(data.pnr);

                    setBookingId(data.booking_id);



                    setBookingStage("success");

                    window.scrollTo({
                      top: 0,
                      behavior: "smooth",
                    });

                  }

                }

                catch (error) {

                  console.log(error);

                  alert("Booking failed");

                }

              }}

              onCancel={() => {

                setBookingStage("search");

              }}
            />

          </div>

        )
      }

      {
        bookingStage === "success" &&
        selectedFlight &&
        passengerData && (

          <div className="max-w-4xl mx-auto px-4 mb-32">

            <SuccessScreen
              pnr={pnr}
              bookingId={bookingId}
              passenger={passengerData}
              flight={selectedFlight}

              onNewBooking={() => {

                setBookingStage("search");

                setSelectedFlight(null);

                setPassengerData(null);

                window.scrollTo({
                  top: 0,
                  behavior: "smooth",
                });

              }}
            />

          </div>

        )
      }

      <div className="fixed bottom-0 left-0 right-0 bg-black border-t border-white/10 p-4 sm:p-6">

        <div className="max-w-4xl mx-auto flex gap-3">

          <input
            value={message}
            onChange={(e) =>
              setMessage(e.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Ask AgenticTrip AI..."
            className="flex-1 p-4 rounded-2xl bg-white/5 border border-white/10 outline-none"
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="bg-white text-black px-6 sm:px-8 rounded-2xl"
          >

            {loading ? "..." : "Send"}

          </button>
          <button
            onClick={() => {

              setMessages([]);

              localStorage.clear();

              window.location.reload();

            }}
            className="bg-red-500 text-white px-5 rounded-2xl hover:bg-red-600 transition"
          >
            Clear Chat
          </button>

        </div>

      </div>

    </div>

  );

}

export default Home;