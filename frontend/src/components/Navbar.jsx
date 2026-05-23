import { Link } from "react-router-dom";
function Navbar() {
  return (
    <nav className="w-full flex items-center justify-between px-8 py-5 border-b border-white/10 backdrop-blur-md sticky top-0 z-50">

      <div className="flex items-center gap-3">

        <div className="w-10 h-10 rounded-xl bg-white text-black flex items-center justify-center font-bold">
          AI
        </div>

        <div>
          <h1 className="text-2xl font-bold">
            AgenticTrip
          </h1>

          <p className="text-xs text-gray-400">
            AI Travel Planner
          </p>
        </div>

      </div>

      <div className="flex items-center gap-6">

        <Link
          to="/"
          className="text-white hover:text-gray-300 transition"
        >
          Home
        </Link>

        <Link
          to="/my-trips"
          className="text-white hover:text-gray-300 transition"
        >
          My Trips
        </Link>

      </div>

    </nav>
  )
}

export default Navbar