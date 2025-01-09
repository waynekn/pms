import { useState } from "react";
import { isAxiosError, AxiosError } from "axios";
import CircularProgress from "@mui/material/CircularProgress";
import classNames from "classnames";

import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";

type ErrorResponse = {
  project_phase?: string[];
  task_name?: string[];
  deadline?: string[];
  description?: string[];
  non_field_errors?: string[];
};

type FormErrors = Omit<
  ErrorResponse,
  "project_phase" | "task_name" | "non_field_errors"
> & {
  projectPhase?: string[];
  taskName?: string[];
  nonFieldErrors?: string[];
};

type TaskCreationPayload = {
  projectPhase: string;
  taskName: string;
  deadline: string;
  description: string;
};

type TaskCreateFormParams = {
  projectPhase: string;
  hideForm: () => void;
};

const TaskCreateForm = ({ projectPhase, hideForm }: TaskCreateFormParams) => {
  const initialState: TaskCreationPayload = {
    projectPhase,
    taskName: "",
    deadline: "",
    description: "",
  };
  const [formValues, setFormValues] =
    useState<TaskCreationPayload>(initialState);

  const initialErrors: FormErrors = {
    projectPhase: [],
    taskName: [],
    deadline: [],
    description: [],
    nonFieldErrors: [],
  };
  const [formErrors, setFormErrors] = useState(initialErrors);
  const [isLoading, setIsLoading] = useState(false);

  const getMinDeadlineDate = () => {
    const tomorrow = Date.now() + 24 * 60 * 60 * 1000;
    const tomorrowDate = new Date(tomorrow);
    return `${tomorrowDate.getFullYear()}-${(tomorrowDate.getMonth() + 1)
      .toString()
      .padStart(2, "0")}-${tomorrowDate.getDate().toString().padStart(2, "0")}`;
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormValues({ ...formValues, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isLoading) return;
    setIsLoading(true);
    try {
      await api.post("task/create/", formValues);
      hideForm();
    } catch (error) {
      setIsLoading(false);
      if (isAxiosError(error)) {
        const statusCode = error.status;

        if (statusCode === 400) {
          const axiosError = error as AxiosError<ErrorResponse>;
          const errorResponse = axiosError.response?.data as ErrorResponse;
          const formErrors = camelize(errorResponse) as FormErrors;
          setFormErrors(formErrors);
          return;
        }

        setFormErrors({ nonFieldErrors: ["An unexpected error occurred."] });
      } else {
        setFormErrors({ nonFieldErrors: ["An unexpected error occurred."] });
      }
    }
  };

  return (
    <section
      className="absolute h-auto w-80 top-1/2 left-1/2 transform bg-gray-50
     -translate-x-1/2 -translate-y-1/2 p-4 border rounded shadow-lg"
    >
      <button onClick={() => hideForm()} className="flex justify-end font-bold">
        &#x2715;
      </button>

      <form method="post" onSubmit={handleSubmit}>
        <h1 className="text-xl font-bold text-center">Create a task.</h1>

        {/* Task name field*/}
        <div className="mt-4">
          <label
            htmlFor="task-name"
            className="block text-sm font-medium text-gray-700"
          >
            Task name.
          </label>
          <input
            type="text"
            name="taskName"
            id="task-name"
            placeholder="Enter task name"
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            value={formValues?.taskName}
            onChange={handleChange}
            maxLength={30}
            required
          />
          {formErrors.taskName && formErrors.taskName.length > 0 && (
            <ul>
              {formErrors.taskName.map((error) => (
                <li key={error} className="text-red-600 text-sm">
                  {error}
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Task description field*/}
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
            placeholder="Enter a description of your task"
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
             focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            maxLength={500}
            value={formValues.description}
            onChange={handleChange}
            required
          ></textarea>
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

        <div className="mt-4">
          <label
            htmlFor="deadline"
            className="block text-sm font-medium text-gray-700"
          >
            Deadline
          </label>
          <input
            type="date"
            name="deadline"
            id="deadline"
            min={getMinDeadlineDate()}
            onChange={handleChange}
            required
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
            disabled={isLoading}
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
export default TaskCreateForm;
