import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from "axios";
import { getCSRFToken } from "./utils/cookies";

type TokenRefreshResponse = {
  access: string;
};

// Create an Axios instance with pre-configured settings
const api = axios.create({
  baseURL:
    import.meta.env.MODE === "production"
      ? // TODO: Replace with actual production URL upon deployment
        "http://localhost/"
      : "http://localhost:8000/",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

// Flag to prevent infinite loops
let madeAttemptToGetAccessToken = false;

/**
 * Interceptor for unauthorized errors.
 */
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig;

    if (error.response?.status === 401) {
      /**
       * The "/dj-rest-auth/user/" endpoint is called during the initial loading
       * of the app to refresh the `User` state. Do not redirect to the login page
       * if a 401 error occurs for this specific endpoint, so as not to redirect to
       * the login page during app initialization.
       */
      if (error.response.config.url === "dj-rest-auth/user/") {
        return Promise.reject(error);
      }

      if (!madeAttemptToGetAccessToken) {
        madeAttemptToGetAccessToken = true;

        try {
          const refreshResponse = await api.post<TokenRefreshResponse>(
            "dj-rest-auth/token/refresh/"
          );
          const newAccessToken = refreshResponse.data.access;

          // Reset the flag
          madeAttemptToGetAccessToken = false;

          // Update the Authorization header with the new token
          originalRequest.headers = {
            ...originalRequest.headers,
            Authorization: `Bearer ${newAccessToken}`,
          };

          // Retry the original request with the new token
          return api(originalRequest);
        } catch {
          // Redirect the user to the login page if unauthorized error persists.
          const path = window.location.pathname;
          window.location.href = `/login?next=${path}`;
        }
      } else {
        // Reset flag.
        madeAttemptToGetAccessToken = false;
        const path = window.location.pathname;
        window.location.href = `/login?next=${path}`;
      }
    }

    return Promise.reject(error);
  }
);

//Add CSRF token for POST requests
api.interceptors.request.use(
  (config) => {
    if (config.method === "post") {
      config.headers["X-CSRFToken"] = getCSRFToken();
    }
    return config;
  },
  function (error) {
    return Promise.reject(
      error instanceof Error ? error : new Error(String(error))
    );
  }
);

export default api;
