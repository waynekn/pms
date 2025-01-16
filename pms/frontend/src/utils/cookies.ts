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
