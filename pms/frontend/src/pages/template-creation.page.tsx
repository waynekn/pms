import { useState, useEffect } from "react";
import { Link } from "react-router";
import { useSelector } from "react-redux";
import { isAxiosError, AxiosError } from "axios";
import classNames from "classnames";

import { selectCurrentUser } from "../store/user/user.selector";
import camelize from "../utils/snakecase-to-camelcase";
import DisplayTemplateWorkFlow from "../components/template-workflow.component";

import api from "../api";

type IndustryResponse = {
  industry_name: string;
  industry_id: string;
};

type Industry = {
  industryName: string;
  industryId: string;
};

// Error response from the API
type ErrorResponse = {
  industry_name?: string[];
  template_name?: string[];
  template_phases?: string[];
  non_field_errors?: string[];
};

// Camelized ErrorResponse
type FormErrors = {
  industryName?: string[];
  templateName?: string[];
  templatePhases?: string[];
  nonFieldErrors?: string[];
};

type FormValues = {
  industry: string;
  templateName: string;
  templatePhases: string[];
};

const TemplateCreationForm = () => {
  const [formValues, setFormValues] = useState<FormValues>({
    industry: "",
    templateName: "",
    templatePhases: [],
  });
  const [formErrors, setFormErrors] = useState<FormErrors>({
    industryName: [],
    templateName: [],
    templatePhases: [],
    nonFieldErrors: [],
  });
  const [phase, setPhase] = useState("");
  const [isLoading, setIslLoading] = useState(true);
  const [initializationError, setInitializationError] = useState(false);
  const [askForVerification, setAskForVerification] = useState(false);
  const [industries, setIndustries] = useState<Industry[]>([]);
  const currentUser = useSelector(selectCurrentUser);

  useEffect(() => {
    const fetchIndustries = async () => {
      try {
        const response = await api.get<IndustryResponse[]>("industry/list/");
        const industryResponse = response.data;
        const industries = industryResponse.map((industry) =>
          camelize(industry)
        ) as Industry[];
        setIslLoading(false);
        setIndustries(industries);
      } catch {
        setInitializationError(true);
      }
    };
    void fetchIndustries();
  }, []);

  const handleIndustryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFormValues({
      ...formValues,
      industry: e.target.value,
    });
  };

  const handlePhaseInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setPhase(value);
  };

  const handlePhaseAddition = () => {
    if (phase && phase.trim()) {
      const trimmedPhase = phase.trim();
      setFormValues({
        ...formValues,
        templatePhases: [
          ...new Set([...formValues.templatePhases, trimmedPhase]),
        ],
      });
    }
    setPhase("");
  };

  const askForConfirmation = (e: React.FormEvent) => {
    e.preventDefault();
    setAskForVerification(true);
  };

  const handleSubmit = async () => {
    try {
      await api.post("template/create/", formValues);
    } catch (error) {
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

  if (initializationError) {
    return (
      <p className="text-red-500 font-bold">
        Could not initialize form. Please try again later.
      </p>
    );
  }

  return (
    <div className="flex w-full h-dvh items-center justify-center space-even">
      <main className="flex mr-5 w-80 p-4 bg-white rounded shadow-lg">
        <form
          onSubmit={askForConfirmation}
          className={classNames(
            "max-w-md mx-auto bg-white p-6 rounded-lg shadow-md",
            { "animate-pulse": isLoading }
          )}
        >
          <div className="space-y-5">
            {/* Close button */}
            <div className="flex justify-end">
              <Link
                to={`../user/${currentUser.username}`}
                className="text-blue-600 font-bold text-xl hover:text-blue-800"
              >
                &#x2715;
              </Link>
            </div>

            {/* Industry Choice Field */}
            <div className="form-group">
              <label
                htmlFor="industry"
                className="block text-sm font-medium text-gray-700"
              >
                Industry
              </label>
              <select
                name="industries"
                id="industry"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                disabled={isLoading || initializationError}
                required
                onChange={handleIndustryChange}
              >
                <option value="">--Please choose an option--</option>
                {industries.map((industry) => (
                  <option
                    key={industry.industryId}
                    value={industry.industryId}
                    onChange={() =>
                      setFormValues({
                        ...formValues,
                        industry: industry.industryId,
                      })
                    }
                  >
                    {industry.industryName}
                  </option>
                ))}
              </select>
              {/* industry errors */}
              {formErrors.industryName &&
                formErrors.industryName.length > 0 && (
                  <ul>
                    {formErrors.industryName.map((error) => (
                      <li key={error} className="text-red-600 text-sm">
                        {error}
                      </li>
                    ))}
                  </ul>
                )}
            </div>

            {/* Template Name Field */}
            <div className="form-group">
              <label
                htmlFor="templateName"
                className="block text-sm font-medium text-gray-700"
              >
                Template Name
              </label>
              <input
                type="text"
                name="templateName"
                id="templateName"
                placeholder="Enter name of your template"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                disabled={isLoading || initializationError}
                required
                value={formValues.templateName}
                onChange={(e) =>
                  setFormValues({
                    ...formValues,
                    templateName: e.target.value,
                  })
                }
              />
              {/* Template name errors. */}
              {formErrors.templateName &&
                formErrors.templateName.length > 0 && (
                  <ul>
                    {formErrors.templateName.map((error) => (
                      <li key={error} className="text-red-600 text-sm">
                        {error}
                      </li>
                    ))}
                  </ul>
                )}
            </div>

            {/* Template Workflow Section. */}
            <div className="form-group space-y-2">
              <label
                htmlFor="phase"
                className="block text-sm font-medium text-gray-700"
              >
                Enter Template Workflow
              </label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  name="phase"
                  id="phase"
                  placeholder="Enter template phase"
                  value={phase}
                  onChange={handlePhaseInput}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  disabled={isLoading || initializationError}
                />
                <button
                  type="button"
                  onClick={handlePhaseAddition}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={isLoading || initializationError}
                >
                  Add
                </button>
              </div>
              {/* Template phase errors. */}
              {formErrors.templatePhases &&
                formErrors.templatePhases.length > 0 && (
                  <ul>
                    {formErrors.templatePhases.map((error) => (
                      <li key={error} className="text-red-600 text-sm">
                        {error}
                      </li>
                    ))}
                  </ul>
                )}
            </div>

            {/* Submit Button */}
            <div>
              <input
                type="submit"
                value="Create"
                className="w-full cursor-pointer bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading || initializationError}
              />
            </div>
          </div>
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
        </form>
      </main>

      {/* Display template workflow. */}
      {formValues.templatePhases.length > 0 && (
        <DisplayTemplateWorkFlow phases={formValues.templatePhases} />
      )}

      {/* Ask for verification before submitting form.  */}
      {askForVerification && (
        <div className="fixed top-2 bg-white p-8 rounded-lg shadow-lg w-100">
          <p className="font-bold">
            Are you sure you want to proceed with this action?
          </p>
          <div className="w-full flex justify-evenly">
            <button
              className="bg-white border border-gray-300 text-gray-700 px-1 py-2 mt-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300"
              onClick={handleSubmit}
            >
              Yes, Proceed
            </button>
            <button
              className="bg-white border border-gray-300 text-gray-700 px-1 py-2 mt-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300"
              onClick={() => setAskForVerification(false)}
            >
              No, Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
export default TemplateCreationForm;
