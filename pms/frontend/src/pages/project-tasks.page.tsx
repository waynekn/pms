import { useState, useEffect } from "react";
import { useParams, Link } from "react-router";
import { AxiosError, isAxiosError } from "axios";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import AccessTimeOutlinedIcon from "@mui/icons-material/AccessTimeOutlined";

import {
  ProjectResponse,
  Project,
} from "../components/user-projects.component";
import { ProjectPhaseResponse, ProjectPhase } from "./project-phases.page";

import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";

export type TaskResponse = {
  task_id: string;
  task_name: string;
  start_date: string;
  deadline: string;
  description: string;
  project_phase: ProjectPhaseResponse;
};

export type Task = Omit<
  TaskResponse,
  "task_id" | "task_name" | "start_date" | "project_phase"
> & {
  taskId: string;
  taskName: string;
  startDate: string;
  projectPhase: ProjectPhase;
};

type ProjectTasksResponse = ProjectResponse & {
  tasks: TaskResponse[];
};

type ProjectTasks = Project & {
  tasks: Task[];
};

const ProjectTasksPage = () => {
  const initialState: ProjectTasks = {
    createdAt: "",
    projectId: "",
    projectName: "",
    projectNameSlug: "",
    deadline: "",
    description: "",
    organization: "",
    tasks: [],
  };
  const [projectTasks, setProjectTasks] = useState<ProjectTasks>(initialState);
  const [errorMessage, setErrorMessage] = useState("");

  const { projectId } = useParams();

  const handleErrors = (error: unknown) => {
    if (isAxiosError(error)) {
      const statusCode = error.status;

      if (statusCode === 400 || statusCode === 404) {
        const axiosError = error as AxiosError<{ detail: string }>;
        setErrorMessage(
          axiosError.response?.data.detail || "An unexpected error occurred."
        );
        return;
      }

      if (statusCode && statusCode >= 500) {
        setErrorMessage("A server error occurred.");
        return;
      }
      setErrorMessage("An unexpected error occurred.");
    } else {
      setErrorMessage("An unexpected error occurred.");
    }
  };

  useEffect(() => {
    const getProjectTasks = async () => {
      if (!projectId) {
        setErrorMessage("Invalid url");
        return;
      }

      try {
        const res = await api.get<ProjectTasksResponse>(
          `project/${projectId}/tasks/`
        );
        const projectTasks = camelize(res.data) as ProjectTasks;
        setProjectTasks(projectTasks);
      } catch (error) {
        handleErrors(error);
      }
    };
    void getProjectTasks();
  }, [projectId]);

  const getDate = (deadline: string) => {
    const dateObj = new Date(deadline);
    const dateStr = `${dateObj.getFullYear()}/${(dateObj.getMonth() + 1)
      .toString()
      .padStart(2, "0")}/${dateObj.getDate().toString().padStart(2, "0")}`;
    return dateStr;
  };

  if (errorMessage) {
    return (
      <p className="bg-red-600 text-white rounded-lg py-4 px-2 mt-3 md:mx-10">
        {errorMessage}
      </p>
    );
  }

  return (
    <Container className="border-x min-h-screen">
      {projectTasks.tasks.length > 0 ? (
        <Stack spacing={0.5}>
          {projectTasks.tasks.map((task) => (
            <Link
              key={task.taskId}
              to={`../task/${task.taskId}/detail/`}
              className="block hover:bg-stone-100 rounded-md p-2 transition-colors duration-300 ease-in-out sm:max-h-24
                         md:max-h-48 overflow-y-hidden"
            >
              <p className="text-lg font-bold">{task.taskName}</p>
              <p className="flex items-center">
                <AccessTimeOutlinedIcon
                  sx={{ color: "grey" }}
                  fontSize="small"
                />
                <span className="ml-3 text-gray-600">
                  {getDate(task.deadline)}
                </span>
              </p>
              <p className="text-gray-600">{task.description}</p>
            </Link>
          ))}
        </Stack>
      ) : (
        <>
          <p className="font-bold md:text-lg">
            {projectTasks.projectName} does not have any tasks currently.
          </p>
          <p className="text-gray-500">Tasks created will appear here.</p>
        </>
      )}
    </Container>
  );
};
export default ProjectTasksPage;
