import { Routes, Route } from "react-router";

import HomePage from "./pages/home-page";
import GoogleCallback from "./components/google-callback.component";

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route
        path="/accounts/google/login/callback/"
        element={<GoogleCallback />}
      />
    </Routes>
  );
};

export default Router;
