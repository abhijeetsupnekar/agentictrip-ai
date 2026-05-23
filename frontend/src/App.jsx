import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Home from "./pages/Home";
import MyTrips from "./pages/MyTrips";

function App() {

  return (

    <BrowserRouter>

      <MainLayout>

        <Routes>

          <Route
            path="/"
            element={<Home />}
          />

          <Route
            path="/my-trips"
            element={<MyTrips />}
          />

        </Routes>

      </MainLayout>

    </BrowserRouter>

  );

}

export default App;