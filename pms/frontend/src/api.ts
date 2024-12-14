import axios from "axios";

// Create an Axios instance with pre-configured settings
const api = axios.create({
  baseURL: "http://localhost:8000/",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
