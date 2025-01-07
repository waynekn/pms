import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { useDispatch, useSelector } from "react-redux";
import classNames from "classnames";

import { StoreDispatch } from "../store/store";
import { registerUser } from "../store/user/user.slice";
import { selectCurrentUser } from "../store/user/user.selector";

import GoogleSVG from "../assets/google.svg";
import CircularProgress from "@mui/material/CircularProgress";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import VisibilityOffOutlinedIcon from "@mui/icons-material/VisibilityOffOutlined";

export type SignUpCredentials = {
  username: string;
  email: string;
  password1: string;
  password2: string;
};

export type SignUpFormErrors = {
  username?: string[];
  email?: string[];
  password1?: string[];
  nonFieldErrors?: string[];
};

const SignUpForm = () => {
  const initialFormValues = {
    username: "",
    email: "",
    password1: "",
    password2: "",
  };
  const initialFormErrors: SignUpFormErrors = {
    username: [],
    email: [],
    password1: [],
    nonFieldErrors: [],
  };
  const [formValues, setFormValues] =
    useState<SignUpCredentials>(initialFormValues);
  const [formErrors, setFormErrors] =
    useState<SignUpFormErrors>(initialFormErrors);
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
    setFormErrors(initialFormErrors);
    // Don't make a request if another is pending.
    if (currentUser.isLoading) {
      return;
    }
    try {
      const user = await dispatch(registerUser(formValues)).unwrap();
      await navigate(`../user/${user.username}`);
    } catch (error) {
      const formErrors = error as SignUpFormErrors;
      setFormErrors((prevErrors) => {
        return {
          ...prevErrors,
          ...formErrors,
        };
      });
    }
  };

  return (
    <section className="absolute h-auto w-80 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 p-4 bg-white rounded shadow-lg z-50">
      <div>
        {/**'X' symbol  */}
        <Link to="/" className="flex justify-end font-bold">
          &#x2715;
        </Link>
        <h2 className="flex justify-center text-lg font-bold tracking-wide">
          Sign Up
        </h2>

        <form method="post" onSubmit={handleSubmit}>
          <div className="space-y-4">
            {/* Username Field  */}
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-gray-700"
              >
                Username
              </label>
              <input
                id="username"
                type="text"
                name="username"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                     focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                value={formValues.username}
                placeholder="Enter username"
                onChange={handleChange}
                required
              />
              {/**
               * Username errors.
               */}
              {formErrors.username && formErrors.username.length > 0 && (
                <ul>
                  {formErrors.username.map((error) => (
                    <li key={error} className="text-red-600 text-sm">
                      {error}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {/* Email Field  */}
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                name="email"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                     focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                value={formValues.email}
                placeholder="Enter your email"
                onChange={handleChange}
                required
              />
              {/**
               * Email errors.
               */}
              {formErrors.email && formErrors.email.length > 0 && (
                <ul>
                  {formErrors.email.map((error) => (
                    <li key={error} className="text-red-600 text-sm">
                      {error}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {/* Password Field */}
            <div>
              <label
                htmlFor="password1"
                className="block text-sm font-medium text-gray-700"
              >
                Password
              </label>
              <div className="relative mt-1">
                <input
                  id="password1"
                  type={showPassword ? "text" : "password"}
                  name="password1"
                  className="block w-full px-3 py-2 pr-10 border rounded-md shadow-sm sm:text-sm 
                            focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  value={formValues.password1}
                  placeholder="Enter your password"
                  onChange={handleChange}
                  required
                />
                {showPassword ? (
                  <VisibilityOffOutlinedIcon
                    onClick={togglePasswordVisibility}
                    fontSize="small"
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer text-gray-500 hover:text-gray-700"
                  />
                ) : (
                  <VisibilityOutlinedIcon
                    onClick={togglePasswordVisibility}
                    fontSize="small"
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer text-gray-500 hover:text-gray-700"
                  />
                )}
              </div>
              {/** Password1 errors */}
              {formErrors.password1 && formErrors.password1.length > 0 && (
                <ul className="mt-2">
                  {formErrors.password1.map((error) => (
                    <li key={error} className="text-red-600 text-sm">
                      {error}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {/*  Confirm Password Field */}
            <div>
              <label
                htmlFor="password2"
                className="block text-sm font-medium text-gray-700"
              >
                Confirm Password
              </label>
              <div className="relative mt-1">
                <input
                  id="password2"
                  type={showPassword ? "text" : "password"}
                  name="password2"
                  className="block w-full px-3 py-2 pr-10 border rounded-md shadow-sm sm:text-sm 
                            focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  value={formValues.password2}
                  placeholder="Confirm your password"
                  onChange={handleChange}
                  required
                />
                {showPassword ? (
                  <VisibilityOffOutlinedIcon
                    onClick={togglePasswordVisibility}
                    fontSize="small"
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer text-gray-500 hover:text-gray-700"
                  />
                ) : (
                  <VisibilityOutlinedIcon
                    onClick={togglePasswordVisibility}
                    fontSize="small"
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer text-gray-500 hover:text-gray-700"
                  />
                )}
              </div>
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

            {/*  Submit Button  */}
            <button
              type="submit"
              className={classNames(
                "w-full bg-blue-600 text-white mb-5 py-2 rounded-md  focus:outline-none",
                currentUser.isLoading
                  ? "cursor-not-allowed"
                  : "hover:bg-blue-700 cursor-pointer "
              )}
            >
              Sign up
              {currentUser.isLoading && (
                <span className="ml-2">
                  <CircularProgress size={13} sx={{ color: "white" }} />
                </span>
              )}
            </button>
          </div>
          {/* Login link   */}
          <p>
            Already have an account?
            <Link to="../login" className="text-blue-500 underline mt-1">
              Log in
            </Link>
          </p>
        </form>

        {/*  Google auth */}
        <a
          href={`https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=${googleCallbackUrl}&prompt=consent&response_type=code&client_id=${googleClientId}&scope=openid%20email%20profile&access_type=offline`}
          className="flex w-full bg-white border border-gray-300 text-gray-700 px-1 py-2 mt-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300"
        >
          <img src={GoogleSVG} alt="Google logo" className="h-6 mr-2" />
          Sign Up with Google
        </a>
      </div>
    </section>
  );
};

export default SignUpForm;
