import { AxiosError, isAxiosError } from "axios";
import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import api from "../../api";

import {
  SuccessfulAuth,
  UnsuccessfulLogIn,
  UnsuccessfulRegistration,
  LogInCredentials,
  LogInFormErrors,
  SignUpCredentials,
  SignUpFormErrors,
} from "../../types/auth";
import { User, CurrentUser, UserResponse } from "../../types/user";
import camelize from "../../utils/snakecase-to-camelcase";
import handleGenericApiErrors from "../../utils/errors";

const initialState: CurrentUser = {
  pk: "",
  username: "",
  email: "",
  usernameSlug: "",
  profilePicture: "",
  isLoading: false,
  isLoggedIn: false,
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
    return camelize(response.data.user) as User;
  } catch (error) {
    if (isAxiosError(error)) {
      const axiosError = error as AxiosError<UnsuccessfulLogIn>;
      const statusCode = axiosError.status;

      // If there is no status code the server is not available.
      if (!statusCode) {
        return rejectWithValue({
          nonFieldErrors: [
            "Service is temprarily unavailable. Please try again later.",
          ],
        });
      }

      if (statusCode >= 500) {
        return rejectWithValue({
          nonFieldErrors: [
            "An unexpected server error occurred. Please try again later.",
          ],
        });
      }

      const errorData = axiosError.response?.data;
      if (errorData) {
        const rejectValue = camelize(errorData) as LogInFormErrors;
        return rejectWithValue(rejectValue);
      }

      return rejectWithValue({
        nonFieldErrors: ["An unknown error occurred. Please try again later."],
      });
    }

    return rejectWithValue({
      nonFieldErrors: ["An unexpected error occurred"],
    });
  }
});

export const registerUser = createAsyncThunk<
  User,
  SignUpCredentials,
  {
    rejectValue: SignUpFormErrors;
  }
>("user/registerUser", async (credentials, { rejectWithValue }) => {
  try {
    const response = await api.post<UserResponse>(
      "accounts/register/",
      credentials
    );
    return camelize(response.data) as User;
  } catch (error) {
    if (isAxiosError(error)) {
      const axiosError = error as AxiosError<UnsuccessfulRegistration>;

      const statusCode = axiosError.status;

      // If there is no status code the server is not available.
      if (!statusCode) {
        return rejectWithValue({
          nonFieldErrors: [
            "Service is temprarily unavailable. Please try again later.",
          ],
        });
      }

      // Handle unexpected errors (e.g., server issues)
      if (statusCode >= 500) {
        return rejectWithValue({
          nonFieldErrors: [
            "An unexpected server error occurred. Please try again later.",
          ],
        });
      }

      const errorData = axiosError.response?.data;
      if (errorData) {
        const rejectValue = camelize(errorData) as SignUpFormErrors;
        return rejectWithValue(rejectValue);
      }
    }
    return rejectWithValue({
      nonFieldErrors: ["An unexpected error occurred."],
    });
  }
});

/**
 * Sends Google Authorization Code to the api.
 */
export const googleAuth = createAsyncThunk<User, string>(
  "user/googleAuth",
  async (code) => {
    const response = await api.post<SuccessfulAuth>("dj-rest-auth/google/", {
      code,
    });
    return camelize(response.data.user) as User;
  }
);

/**
 * Fetches the user during app initialization.
 */
export const fetchCurrentUser = createAsyncThunk<User>(
  "user/fetchCurrentUser",
  async () => {
    const response = await api.get<User>("dj-rest-auth/user/");
    return response.data;
  }
);

export const deleteCurrentUser = createAsyncThunk(
  "user/deleteCurrentUser",
  async (_, { rejectWithValue }) => {
    try {
      await api.delete("accounts/delete/");
    } catch (error) {
      const errMsg = handleGenericApiErrors(error);
      return rejectWithValue(errMsg);
    }
  }
);

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    clearCurrentUser() {
      return initialState;
    },
    setCurrentUser(_, action: PayloadAction<UserResponse>): CurrentUser {
      const updatedUser = camelize(action.payload) as User;
      const user: CurrentUser = {
        ...updatedUser,
        isLoading: false,
        isLoggedIn: true,
      };
      return user;
    },
  },
  extraReducers: (builder) => {
    builder
      /**
       * logInUser thunk
       */
      .addCase(logInUser.pending, (state: CurrentUser) => {
        state.isLoading = true;
      })
      .addCase(
        logInUser.fulfilled,
        (state: CurrentUser, action: PayloadAction<User>) => {
          const user: CurrentUser = {
            ...state,
            ...action.payload,
            isLoggedIn: true,
            isLoading: false,
          };
          return user;
        }
      )
      .addCase(logInUser.rejected, (state: CurrentUser) => {
        state.isLoading = false;
      })
      /**
       * registerUser thunk
       */
      .addCase(registerUser.pending, (state: CurrentUser) => {
        state.isLoading = true;
      })
      .addCase(
        registerUser.fulfilled,
        (state: CurrentUser, action: PayloadAction<User>) => {
          const user: CurrentUser = {
            ...state,
            ...action.payload,
            isLoggedIn: true,
            isLoading: false,
          };
          return user;
        }
      )
      .addCase(registerUser.rejected, (state: CurrentUser) => {
        state.isLoading = false;
      })
      /**
       * googleAuth thunk
       */
      .addCase(googleAuth.pending, (state: CurrentUser) => {
        state.isLoading = true;
      })
      .addCase(
        googleAuth.fulfilled,
        (state: CurrentUser, action: PayloadAction<User>) => {
          const user: CurrentUser = {
            ...state,
            ...action.payload,
            isLoggedIn: true,
            isLoading: false,
          };
          return user;
        }
      )
      /**
       * fetchCurrentUser thunk
       */
      .addCase(
        fetchCurrentUser.fulfilled,
        (state: CurrentUser, action: PayloadAction<User>) => {
          const user: CurrentUser = {
            ...state,
            ...action.payload,
            isLoggedIn: true,
            isLoading: false,
          };
          return user;
        }
      )
      /**
       * deleteCurrentUser thunk
       */
      .addCase(deleteCurrentUser.pending, (state: CurrentUser) => {
        state.isLoading = true;
      })
      .addCase(deleteCurrentUser.fulfilled, () => {
        return initialState;
      })
      .addCase(deleteCurrentUser.rejected, (state: CurrentUser) => {
        state.isLoading = false;
      });
  },
});

export const { clearCurrentUser, setCurrentUser } = userSlice.actions;

export const userReducer = userSlice.reducer;
