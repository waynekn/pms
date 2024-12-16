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

/**
 * Retrieves the CSRF token from the document's cookies.
 *
 * This function looks for a cookie named 'csrftoken' and returns its value.
 * If the 'csrftoken' cookie is not found, it returns an empty string.
 *
 * @returns {string} The value of the 'csrftoken' cookie, or an empty string if the cookie is not found.
 */
export const getCSRFToken = () => {
  const name = "csrftoken";
  let cookieValue = "";

  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
};
