import { configureStore } from "@reduxjs/toolkit";
import logger from "redux-logger";
import { rootReducer } from "./root-reducer";

const isDev = import.meta.env.MODE === "development";

const store = configureStore({
  reducer: rootReducer,

  middleware: (getDefaultMiddleware) =>
    isDev ? getDefaultMiddleware().concat(logger) : getDefaultMiddleware(),
});

export type StoreDispatch = typeof store.dispatch;

export default store;
