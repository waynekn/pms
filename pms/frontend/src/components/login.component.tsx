import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router";
import classNames from "classnames";

import { StoreDispatch } from "../store/store";
import { logInUser } from "../store/user/user.slice";
import { selectCurrentUser } from "../store/user/user.selector";

import GoogleSVG from "../assets/google.svg";
import CircularProgress from "@mui/material/CircularProgress";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import VisibilityOffOutlinedIcon from "@mui/icons-material/VisibilityOffOutlined";

export type LogInCredentials = {
  username: string;
  password: string;
};

export type LogInFormErrors = {
  password?: string[];
  nonFieldErrors?: string[];
};

const LogInForm = () => {
  const [formValues, setFormValues] = useState<LogInCredentials>({
    username: "",
    password: "",
  });
  const [formErrors, setFormErrors] = useState<LogInFormErrors>({
    password: [],
    nonFieldErrors: [],
  });

  const [showPassword, setShowPassword] = useState(false);

  const dispatch = useDispatch<StoreDispatch>();
  const currentUser = useSelector(selectCurrentUser);
  const navigate = useNavigate();

  const googleCallbackUrl = import.meta.env.VITE_GOOGLE_CALLBACK_URL;
  const googleClientId = import.meta.env.VITE_CLIENT_ID;

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormValues({ ...formValues, [name]: value });
  };

  const handleSubmit = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    setFormErrors({ password: [], nonFieldErrors: [] });
    try {
      const user = await dispatch(logInUser(formValues)).unwrap();
      await navigate(`../user/${user.username}/`);
    } catch (error) {
      const formErrors = error as LogInFormErrors;
      setFormErrors((prevState) => {
        return {
          ...prevState,
          ...formErrors,
        };
      });
    }
  };

  return (
    <section className="absolute h-auto w-80 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 p-4 bg-white rounded shadow-lg z-50">
      <div>
        {/* 'X' symbol */}
        <Link to="/" className="w-full flex justify-end font-bold">
          &#x2715;
        </Link>
        <header className="text-xl font-bold text-center">Login</header>
        <form method="post" onSubmit={handleSubmit}>
          <div className="space-y-4">
            {/**
             * Email or username field.
             */}
            <div>
              <label
                htmlFor="login"
                className="block text-sm font-medium text-gray-700"
              >
                Email or Username
              </label>
              <input
                id="login"
                type="text"
                name="username"
                value={formValues.username}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                     focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Enter email or username"
                onChange={handleChange}
              />
            </div>
            {/**
             * Password field.
             */}
            <div className="relative">
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700"
              >
                Password
              </label>
              <div className="relative mt-1">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  name="password"
                  className="block w-full px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm
                 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  value={formValues.password}
                  placeholder="Password"
                  onChange={handleChange}
                />
                {showPassword ? (
                  <VisibilityOffOutlinedIcon
                    onClick={togglePasswordVisibility}
                    fontSize="small"
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer text-sm text-gray-500 hover:text-gray-700"
                  />
                ) : (
                  <VisibilityOutlinedIcon
                    onClick={togglePasswordVisibility}
                    fontSize="small"
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer text-sm text-gray-500 hover:text-gray-700"
                  />
                )}
              </div>
            </div>

            {/**
             * Password errors errors if any.
             */}
            {formErrors.password && formErrors.password.length > 0 && (
              <ul>
                {formErrors.password.map((error) => (
                  <li key={error} className="text-red-600 text-sm">
                    {error}
                  </li>
                ))}
              </ul>
            )}

            <button
              type="submit"
              className={classNames(
                "w-full bg-blue-600  text-white p-2 rounded-md mt-4 ",
                currentUser.isLoading
                  ? "cursor-not-allowed"
                  : "cursor-pointer hover:bg-blue-700"
              )}
              disabled={currentUser.isLoading}
            >
              Login
              {currentUser.isLoading && (
                <span className="ml-2">
                  <CircularProgress size={13} sx={{ color: "white" }} />
                </span>
              )}
            </button>
          </div>
          {/**
           * Non field errors.
           */}
          {formErrors.nonFieldErrors &&
            formErrors.nonFieldErrors.length > 0 && (
              <ul>
                {formErrors.nonFieldErrors.map((error) => (
                  <li key={error} className="text-red-600 text-sm">
                    {error}
                  </li>
                ))}
              </ul>
            )}

          <a
            href={`https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=${googleCallbackUrl}&prompt=consent&response_type=code&client_id=${googleClientId}&scope=openid%20email%20profile&access_type=offline`}
            className="flex w-full bg-white border border-gray-300 text-gray-700 px-1 py-2 mt-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300"
          >
            <img src={GoogleSVG} alt="Google logo" className="h-6 mr-2" />
            Sign In with Google
          </a>

          <Link to="#" className="text-blue-500 underline block mt-2">
            Forgot password?
          </Link>

          <p className="mt-2">
            Don’t have an account?
            <Link to="../signup" className="text-blue-500 underline">
              Sign up
            </Link>
          </p>
        </form>
      </div>
    </section>
  );
};
export default LogInForm;
