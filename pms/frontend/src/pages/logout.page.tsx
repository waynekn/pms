import { useState } from "react";
import { useNavigate, Link } from "react-router";
import { useSelector, useDispatch } from "react-redux";
import { StoreDispatch } from "../store/store";
import { clearCurrentUser } from "../store/user/user.slice";
import { selectCurrentUser } from "../store/user/user.selector";
import api from "../api";

const LogoutPage = () => {
  const [logoutError, setLogoutError] = useState<string | null>(null);
  const currentUser = useSelector(selectCurrentUser);
  const dispatch = useDispatch<StoreDispatch>();
  const navigate = useNavigate();

  document.title = "Logout";

  const logOutUser = async () => {
    try {
      setLogoutError(null);
      await api.post("dj-rest-auth/logout/");
      dispatch(clearCurrentUser());
      await navigate("/");
    } catch {
      setLogoutError("An error occurred during logout. Please try again.");
    }
  };

  return (
    <div className="h-screen w-full flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-auto">
        <h2 className="text-2xl font-semibold text-center text-gray-800 mb-4">
          Are you sure you want to log out?
        </h2>
        <p className="text-center text-gray-600 mb-6">
          You will be signed out of your account.
        </p>

        <div className="space-y-4">
          <button
            className="w-full cursor-pointer bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            onClick={logOutUser}
          >
            Yes, log me out
          </button>

          <Link
            to={`../user/${currentUser.username}`}
            className="w-full block text-center cursor-pointer bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Cancel
          </Link>
        </div>
        {logoutError && <p className="text-red-600">{logoutError}</p>}
      </div>
    </div>
  );
};
export default LogoutPage;
