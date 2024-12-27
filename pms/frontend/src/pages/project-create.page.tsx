import { useState } from "react";
import { isAxiosError } from "axios";
import { useLocation } from "react-router";
import ProjectCreateSideBar from "../components/project-create.sidebar";
import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";

export type ProjectCreationFormState = {
  organizationId: string;
  organizationName: string;
};

type FormErrors = {
  organization?: string[];
  projectName?: string[];
  template?: string[];
  description?: string[];
  deadline?: string[];
  nonFieldErrors?: string[];
};

type ErrorResponse = Omit<FormErrors, "projectName" | "nonFieldErrors"> & {
  project_name?: string[];
  non_field_errors?: string[];
};

type FormValues = {
  organization: string;
  projectName: string;
  template: string;
  description: string;
  deadline: string;
};

const ProjectCreationForm = () => {
  const location = useLocation();
  const state = location.state as ProjectCreationFormState;
  const initialState: FormValues = {
    organization: state.organizationId,
    projectName: "",
    template: "",
    description: "",
    deadline: "",
  };
  const [formValues, setFormValues] = useState<FormValues>(initialState);

  const initialErrorsState: FormErrors = {
    organization: [],
    projectName: [],
    template: [],
    description: [],
    deadline: [],
    nonFieldErrors: [],
  };
  const [formErrors, setFormErrors] = useState<FormErrors>(initialErrorsState);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormValues({ ...formValues, [name]: value });
  };

  const getMinDeadlineDate = () => {
    const tomorrow = Date.now() + 24 * 60 * 60 * 1000;
    const tomorrowDate = new Date(tomorrow);
    return `${tomorrowDate.getFullYear()}-${(tomorrowDate.getMonth() + 1)
      .toString()
      .padStart(2, "0")}-${tomorrowDate.getDate().toString().padStart(2, "0")}`;
  };

  const handleTemplateSelection = (
    templateId: string,
    templateName: string
  ) => {
    setFormValues((formValues) => ({
      ...formValues,
      template: templateId,
    }));
    //update text of template field
    const templateInput = document.getElementById(
      "template"
    ) as HTMLInputElement;
    templateInput.value = templateName;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("project/create/", formValues);
    } catch (error) {
      if (isAxiosError(error)) {
        const errorResponse = error.response?.data as ErrorResponse;
        const formErrors = camelize(errorResponse) as FormErrors;
        setFormErrors(formErrors);
      } else {
        setFormErrors({ nonFieldErrors: ["An unexpected error occurred"] });
      }
    }
  };

  return (
    <div className="h-screen w-screen flex flex-col md:flex-row bg-gray-100">
      {/* Sidebar */}
      <ProjectCreateSideBar handleTemplateSelection={handleTemplateSelection} />

      {/* Main Form */}
      <main className="flex-1 p-4 md:p-8">
        <button
          className="md:hidden p-2 bg-blue-500 text-white rounded-md mb-4"
          onClick={() => {
            document
              .getElementById("sidebar")!
              .classList.toggle("translate-x-0");
          }}
        >
          ☰ Open Sidebar
        </button>
        <form
          className="w-full max-w-3xl mx-auto border-2 border-gray-300 rounded-lg bg-white shadow-lg p-8 space-y-6"
          onSubmit={handleSubmit}
        >
          {/* Organization field */}
          <div className="flex flex-col">
            <label
              htmlFor="organization"
              className="text-gray-700 font-medium mb-2"
            >
              Organization:
            </label>
            <input
              type="text"
              name="organization"
              id="organization"
              className="cursor-not-allowed opacity-50 w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none sm:text-sm"
              value={state.organizationName}
              readOnly
              required
            />
            {formErrors.organization && formErrors.organization.length > 0 && (
              <ul>
                {formErrors.organization.map((error) => (
                  <li key={error} className="text-red-600 text-sm">
                    {error}
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Project name field */}
          <div className="flex flex-col">
            <label
              htmlFor="projectName"
              className="text-gray-700 font-medium mb-2"
            >
              Project name:
            </label>
            <input
              type="text"
              name="projectName"
              id="projectName"
              className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="Enter the name of your project"
              value={formValues.projectName}
              onChange={handleChange}
              required
            />
            {formErrors.projectName && formErrors.projectName.length > 0 && (
              <ul>
                {formErrors.projectName.map((error) => (
                  <li key={error} className="text-red-600 text-sm">
                    {error}
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Template field */}
          <div className="flex flex-col">
            <label
              htmlFor="template"
              className="text-gray-700 font-medium mb-2"
            >
              Template:
            </label>
            <input
              type="text"
              name="template"
              id="template"
              className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="This project currently doesn't have a template."
            />
            {formErrors.template && formErrors.template.length > 0 && (
              <ul>
                {formErrors.template.map((error) => (
                  <li key={error} className="text-red-600 text-sm">
                    {error}
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Description field */}
          <div className="flex flex-col">
            <label
              htmlFor="description"
              className="text-gray-700 font-medium mb-2"
            >
              Description:
            </label>
            <textarea
              name="description"
              id="description"
              className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="Enter a description for the project (optional)"
              value={formValues.description}
              onChange={handleChange}
            />
            {formErrors.description && formErrors.description.length > 0 && (
              <ul>
                {formErrors.description.map((error) => (
                  <li key={error} className="text-red-600 text-sm">
                    {error}
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Deadline field */}
          <div className="flex flex-col">
            <label
              htmlFor="deadline"
              className="text-gray-700 font-medium mb-2"
            >
              Deadline:
            </label>
            <input
              type="date"
              name="deadline"
              id="deadline"
              min={getMinDeadlineDate()}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
            {formErrors.deadline && formErrors.deadline.length > 0 && (
              <ul>
                {formErrors.deadline.map((error) => (
                  <li key={error} className="text-red-600 text-sm">
                    {error}
                  </li>
                ))}
              </ul>
            )}
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

          {/* Submit Button */}
          <div className="flex justify-end">
            <button
              type="submit"
              className="px-6 py-3 bg-blue-500 text-white font-medium rounded-md shadow hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
              Submit
            </button>
          </div>
        </form>
      </main>
    </div>
  );
};
export default ProjectCreationForm;
