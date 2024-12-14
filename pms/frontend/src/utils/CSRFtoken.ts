import api from "../api";

/**
 * Utility function to fetch and set a CSRF token.
 *
 * This function makes an API call to retrieve the CSRF token from the server and
 * stores it in a cookie. It will only be called in the `development` environment
 * to allow the frontend to make secure POST requests to the backend.
 *
 * @throws Error if the request fails; errors are handled in the calling function.
 */
export const fetchCSRFtoken = async () => {
  try {
    const response = await api.get<{ csrftoken: string }>("csrftoken/");
    const token = response.data.csrftoken;
    document.cookie = `$csrftoken=${token}; max-age=3600; SameSite=Lax;`;
  } catch (error) {
    console.error("CSRF token fetch failed:", error);
    throw new Error("Failed to fetch CSRF token");
  }
};
