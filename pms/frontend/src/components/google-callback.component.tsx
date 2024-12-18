import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useNavigate, useLocation } from "react-router";

import { StoreDispatch } from "../store/store";
import { googleAuth } from "../store/user/user.slice";

const GoogleCallback = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch<StoreDispatch>();

  history.pushState({}, "", "/");

  useEffect(() => {
    const query = new URLSearchParams(location.search);
    const code = query.get("code");

    if (code) {
      dispatch(googleAuth(code))
        .unwrap()
        .then((result) => {
          console.log("Google Auth successful:", result);
        })
        .catch((error) => {
          console.error("Google Auth failed:", error);
        });
    } else {
      console.error("No code found in the callback URL.");
    }
  }, [dispatch, location, navigate]);

  return (
    <div className="fixed bottom-5 left-1/2 transform -translate-x-1/2 z-10 text-center px-4 py-2 rounded">
      <div>Connecting...</div>
    </div>
  );
};

export default GoogleCallback;
