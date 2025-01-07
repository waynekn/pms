import { useState } from "react";
import { Link } from "react-router";
import { useSelector } from "react-redux";
import { AxiosError, isAxiosError } from "axios";
import classNames from "classnames";

import { selectCurrentUser } from "../store/user/user.selector";
import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";

import CircularProgress from "@mui/material/CircularProgress";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import VisibilityOffOutlinedIcon from "@mui/icons-material/VisibilityOffOutlined";

// Error response from the API
type ErrorResponse = {
  organization_name?: string[];
  organization_password?: string[];
  non_field_errors?: string[];
};

// Camelized ErrorResponse
type FormErrors = {
  organizationName?: string[];
  organizationPassword?: string[];
  nonFieldErrors?: string[];
};

const OrganizationCreationForm = () => {
  const [formValues, setFormValues] = useState({
    organizationName: "",
    description: "",
    organizationPassword: "",
    password2: "",
  });

  const [formErrors, setFormErrors] = useState<FormErrors>({
    organizationName: [],
    organizationPassword: [],
    nonFieldErrors: [],
  });

  const [isLoading, setIsLoading] = useState(false);

  const [showPassword, setShowPassword] = useState(false);

  const currentUser = useSelector(selectCurrentUser);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormValues({ ...formValues, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (isLoading) {
      return;
    }

    setIsLoading(true);
    try {
      await api.post("/organizations/create/", formValues);
    } catch (error) {
      setIsLoading(false);
      if (isAxiosError(error)) {
        const status = error.status;

        if (status == 400) {
          const axiosError = error as AxiosError<ErrorResponse>;
          const errorResponse = axiosError.response?.data as ErrorResponse;
          const errors = camelize(errorResponse) as FormErrors;
          setFormErrors(errors);
        } else {
          setFormErrors({ nonFieldErrors: ["An unexpected error occurred"] });
        }
      } else {
        setFormErrors({ nonFieldErrors: ["An unexpected error occurred"] });
      }
    }
  };

  return (
    <section className="absolute h-auto w-80 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 p-4 bg-white rounded shadow-lg">
      {/* 'X' symbol */}
      <Link
        to={`/user/${currentUser?.username}/`}
        className="flex justify-end font-bold"
      >
        &#x2715;
      </Link>

      <form method="post" onSubmit={handleSubmit}>
        <h1 className="text-xl font-bold text-center">
          Create an Organization
        </h1>

        {/* Organization name field*/}
        <div className="mt-4">
          <label
            htmlFor="name"
            className="block text-sm font-medium text-gray-700"
          >
            Organization name.
          </label>
          <input
            type="text"
            name="organizationName"
            id="organizationName"
            placeholder="Enter name of your organization"
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            value={formValues.organizationName}
            onChange={handleChange}
            required
          />
          {formErrors.organizationName &&
            formErrors.organizationName.length > 0 && (
              <ul>
                {formErrors.organizationName.map((error) => (
                  <li key={error} className="text-red-600 text-sm">
                    {error}
                  </li>
                ))}
              </ul>
            )}
        </div>

        {/* Organization description field*/}
        <div className="mt-4">
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700"
          >
            Description
          </label>
          <textarea
            name="description"
            id="description"
            placeholder="Enter a description of your organization (optional)"
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            value={formValues.description}
            onChange={handleChange}
          ></textarea>
        </div>

        {/* Password field*/}
        <div className="mt-4">
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
              name="organizationPassword"
              className="block w-full px-3 py-2 pr-10 border rounded-md shadow-sm sm:text-sm 
                            focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              value={formValues.organizationPassword}
              placeholder="Password"
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

          {formErrors.organizationPassword &&
            formErrors.organizationPassword.length > 0 && (
              <ul>
                {formErrors.organizationPassword.map((error) => (
                  <li key={error} className="text-red-600 text-sm">
                    {error}
                  </li>
                ))}
              </ul>
            )}
        </div>

        {/* Password confirmation field*/}
        <div className="mt-4">
          <label
            htmlFor="password2"
            className="block text-sm font-medium text-gray-700"
          >
            Confirm password
          </label>
          <div className="relative mt-1">
            <input
              id="password2"
              type={showPassword ? "text" : "password"}
              name="password2"
              className="block w-full px-3 py-2 pr-10 border rounded-md shadow-sm sm:text-sm 
                            focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              value={formValues.password2}
              placeholder="Confirm password"
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

        {formErrors.nonFieldErrors && formErrors.nonFieldErrors.length > 0 && (
          <ul>
            {formErrors.nonFieldErrors.map((error) => (
              <li key={error} className="text-red-600 text-sm">
                {error}
              </li>
            ))}
          </ul>
        )}

        {/* Submit button */}
        <div className="mt-4">
          <button
            type="submit"
            className={classNames(
              "w-full bg-blue-600 text-white p-2 rounded-md",
              isLoading
                ? "cursor-not-allowed"
                : "cursor-pointer hover:bg-blue-700"
            )}
          >
            Create
            {isLoading && (
              <span className="ml-2">
                <CircularProgress size={13} sx={{ color: "white" }} />
              </span>
            )}
          </button>
        </div>
      </form>
    </section>
  );
};
export default OrganizationCreationForm;
