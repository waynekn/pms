import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { BrowserRouter } from "react-router";

import { StoreDispatch } from "./store/store";
import { clearCurrentUser, fetchCurrentUser } from "./store/user/user.slice";
import { isStateRefreshed } from "./utils/cookies";

import Router from "./router";

function App() {
  const dispatch = useDispatch<StoreDispatch>();
  useEffect(() => {
    const refreshState = async () => {
      if (isStateRefreshed()) {
        return;
      }
      try {
        await dispatch(fetchCurrentUser());
      } catch {
        dispatch(clearCurrentUser());
      }
      document.cookie = "state-refreshed=true";
    };
    void refreshState();
  }, [dispatch]);

  return (
    <BrowserRouter>
      <Router />
    </BrowserRouter>
  );
}

export default App;
