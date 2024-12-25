import { useState } from "react";
import { isAxiosError, AxiosError } from "axios";
import api from "../api";

type OrgAuthFormProps = {
  organizationName: string;
};

const OrgAuthForm = ({ organizationName }: OrgAuthFormProps) => {
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post<{ organizationName: string; password: string }>(
        "organizations/auth/",
        {
          organizationName,
          password,
        }
      );
      // reload the page to display organization detail if auth attempt was successful
      location.reload();
    } catch (error) {
      if (isAxiosError(error)) {
        const axiosError = error as AxiosError<{ error: string }>;
        setErrorMessage(
          axiosError.response?.data.error || " An unexpected error occurred."
        );
      } else {
        setErrorMessage("An unexpected error occurred.");
      }
    }
  };

  return (
    <div className="h-screen grid place-items-center ">
      <form className="max-w-sm mx-auto border-2 p-3" onSubmit={handleSubmit}>
        <p className="mb-2">
          You are not authorized to view
          <span className="font-bold mx-1">{organizationName}</span>
          Enter the passkey to gain access.
        </p>
        <div>
          <input
            type="password"
            id="password"
            name="password"
            className="bg-gray-50 border border-gray-300  text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 "
            required
            onChange={handleChange}
            value={password}
          />
        </div>
        {errorMessage && <p className="text-red-600 text-sm">{errorMessage}</p>}

        <button
          type="submit"
          className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
        >
          Submit
        </button>
      </form>
    </div>
  );
};
export default OrgAuthForm;
