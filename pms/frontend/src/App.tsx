import { useEffect, useState } from "react";
import { BrowserRouter } from "react-router";
import Router from "./router";

import { fetchCSRFtoken } from "./utils/CSRFtoken";

function App() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    /**
     * This effect is used to fetch a CSRF token during the development environment.
     * It ensures that the CSRF token is retrieved before making any POST requests
     * to the API. This call will only be made when the app is running in
     * development mode (`import.meta.env.MODE === 'development'`).
     */
    const initCSRFToken = async () => {
      try {
        if (import.meta.env.MODE === "development") {
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
      <Router />
    </BrowserRouter>
  );
}

export default App;
