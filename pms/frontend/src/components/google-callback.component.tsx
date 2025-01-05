import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useLocation } from "react-router";

import { selectCurrentUser } from "../store/user/user.selector";
import { StoreDispatch } from "../store/store";
import { googleAuth } from "../store/user/user.slice";

const GoogleCallback = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch<StoreDispatch>();
  const currentUser = useSelector(selectCurrentUser);

  const query = new URLSearchParams(location.search);
  const code = query.get("code");

  history.pushState({}, "", "/");

  useEffect(() => {
    const sendGoogleAuthRequest = async () => {
      if (code) {
        try {
          await dispatch(googleAuth(code)).unwrap();
          await navigate(`../user/${currentUser.username}`);
        } catch {
          await navigate("/");
        }
      } else {
        await navigate("/");
      }
    };

    void sendGoogleAuthRequest();
  }, [code, currentUser.username, dispatch, location, navigate]);

  return (
    <div className="fixed bottom-5 left-0 w-full z-10 text-center px-4 py-2 shadow-lg">
      <span className="bg-green-600 px-3 py-3 text-white text-lg font-bold rounded-2xl">
        Connecting
        <span className="text-white text-lg font-bold ml-2 animate-ping">
          ...
        </span>
      </span>
    </div>
  );
};

export default GoogleCallback;
