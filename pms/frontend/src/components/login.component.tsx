import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router";
import { StoreDispatch } from "../store/store";
import { logInUser } from "../store/user/user.slice";
import { selectCurrentUser } from "../store/user/user.selector";

import GoogleSVG from "../assets/google.svg";

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

  const dispatch = useDispatch<StoreDispatch>();
  const currentUser = useSelector(selectCurrentUser);
  const navigate = useNavigate();

  const googleCallbackUrl = import.meta.env.VITE_GOOGLE_CALLBACK_URL;
  const googleClientId = import.meta.env.VITE_CLIENT_ID;

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
        <header className="flex justify-center text-lg font-bold tracking-wide mb-2">
          Login
        </header>
        <form method="post" onSubmit={handleSubmit}>
          <div className="space-y-4">
            {/**
             * Email or username field.
             */}
            <div className="form-group">
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
                placeholder="Enter email or username"
                onChange={handleChange}
              />
            </div>
            {/**
             * Password field.
             */}
            <div className="form-group">
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                name="password"
                value={formValues.password}
                placeholder="Password"
                onChange={handleChange}
              />
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

            <input
              type="submit"
              className="w-full cursor-pointer bg-blue-600 text-white mb-5 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value="Log in"
              disabled={currentUser.isLoading}
            />
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

          <Link to="#" className="text-sky-500 underline block mt-2">
            Forgot password?
          </Link>

          <p className="mt-4">
            Don’t have an account?
            <Link to="../signup" className="text-sky-500 underline">
              Sign up
            </Link>
          </p>
        </form>
      </div>
    </section>
  );
};
export default LogInForm;
