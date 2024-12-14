import axios from "axios";
import { getCSRFToken } from "./utils/CSRFtoken";

// Create an Axios instance with pre-configured settings
const api = axios.create({
  baseURL: "http://localhost:8000/",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

//Add CSRF token for POST requests
api.interceptors.request.use(
  (config) => {
    if (config.method === "post") {
      config.headers["X-CSRFToken"] = getCSRFToken();
    }
    return config;
  },
  function (error) {
    // eslint-disable-next-line @typescript-eslint/prefer-promise-reject-errors
    return Promise.reject(error);
  }
);

export default api;
