import { AxiosError } from "axios";
import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import api from "../../api";
import {
  LogInCredentials,
  LogInFormErrors,
} from "../../components/login.component";

export type User = {
  pk: string;
  username: string;
  email: string;
};

export type CurrentUser = User & {
  isLoading: boolean;
  isLoggedIn: boolean;
  notificationMessage: string | null;
};

type SuccessfulAuth = {
  user: User;
  access: string;
  refresh: string;
};

const initialState: CurrentUser = {
  pk: "",
  username: "",
  email: "",
  isLoading: false,
  isLoggedIn: false,
  notificationMessage: null,
};

export type UnsuccessfulLogIn = {
  password?: string[];
  non_field_errors?: string[];
};

/**
 * Sends login credentials (email/username and password) to the API to enable a user to log in.
 *
 * @param {LogInCredentials} credentials - The credentials for logging in, which include email/username and password.
 * @param {Object} thunkAPI - The Thunk API object used to dispatch actions and handle errors.
 * @param {Function} thunkAPI.rejectWithValue - Function to return a rejected promise with a custom error value.
 *
 * @returns {Promise<User>} A promise that resolves to the logged-in user's data if successful.
 *
 * @throws {LogInFormErrors} If the login fails, returns a set of form errors (password errors or non-field errors).
 */
export const logInUser = createAsyncThunk<
  User,
  LogInCredentials,
  {
    rejectValue: LogInFormErrors;
  }
>("user/logInUser", async (credentials, { rejectWithValue }) => {
  try {
    const response = await api.post<SuccessfulAuth>(
      "dj-rest-auth/login/",
      credentials
    );
    return response.data.user;
  } catch (error) {
    if (error instanceof AxiosError) {
      const axiosError = error as AxiosError<UnsuccessfulLogIn>;
      const rejectValue = {
        password: axiosError.response?.data.password,
        nonFieldErrors: axiosError.response?.data.non_field_errors || [
          "An unexpected error occurred",
        ],
      };
      return rejectWithValue(rejectValue);
    }

    return rejectWithValue({
      nonFieldErrors: ["An unexpected error occurred"],
    });
  }
});

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    clearCurrentUser() {
      return initialState;
    },
  },
  extraReducers: (builder) => {
    builder
      /**
       * logInUser thunk
       */
      .addCase(logInUser.pending, (state: CurrentUser) => {
        state.isLoading = true;
        state.notificationMessage = null;
      })
      .addCase(
        logInUser.fulfilled,
        (state: CurrentUser, action: PayloadAction<User>) => {
          const user: CurrentUser = {
            ...state,
            ...action.payload,
            isLoggedIn: true,
            isLoading: false,
            notificationMessage: null,
          };
          return user;
        }
      )
      .addCase(logInUser.rejected, (state: CurrentUser, action) => {
        state.isLoading = false;
        if (typeof action.payload === "string") {
          console.warn(action.payload);
        } else {
          console.warn(action.payload);
        }
      });
  },
});

export const { clearCurrentUser } = userSlice.actions;

export const userReducer = userSlice.reducer;
