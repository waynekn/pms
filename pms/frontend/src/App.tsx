import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router";

import HomePage from "./pages/home-page";
import { fetchCSRFtoken } from "./utils/CSRFtoken";

function App() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    /**
     * This effect is used to fetch a CSRF token during the development environment.
     * It ensures that the CSRF token is retrieved before making any POST requests
     * to the API. This call will only be made when the app is running in
     * development mode (`process.env.NODE_ENV === 'development'`).
     */
    const initCSRFToken = async () => {
      try {
        if (process.env.NODE_ENV === "development") {
          await fetchCSRFtoken();
        }
        setIsLoading(false);
      } catch {
        window.location.href = "#";
        setIsLoading(false);
      }
    };
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    initCSRFToken();
  }, []);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
