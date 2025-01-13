import { useEffect, useState } from "react";
import { useParams, Link } from "react-router";
import { AxiosError, isAxiosError } from "axios";
import Container from "@mui/material/Container";
import Stack from "@mui/material/Stack";
import CircularProgress from "@mui/material/CircularProgress";

import {
  ProjectResponse,
  Project,
} from "../components/user-projects.component";

import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";

export type ProjectPhaseResponse = {
  phase_id: string;
  phase_name: string;
};

export type ProjectPhase = {
  phaseId: string;
  phaseName: string;
};

type ProjectWorkFlowResponse = ProjectResponse & {
  phases: ProjectPhaseResponse[];
};

type ProjectWorkFlow = Project & {
  phases: ProjectPhase[];
};

const ProjectPhasePage = () => {
  const initialState: ProjectWorkFlow = {
    createdAt: "",
    projectId: "",
    projectName: "",
    projectNameSlug: "",
    deadline: "",
    description: "",
    organization: "",
    phases: [],
  };
  const [projectWorkflow, setProjectWorkflow] =
    useState<ProjectWorkFlow>(initialState);

  const [isLoading, setIsLoading] = useState(true);
  const [isaddingProjectWorkflow, setIsAddingProjectWorkflow] = useState(false);
  const [phaseInput, setPhaseInput] = useState("");

  const [errorMessage, setErrorMessage] = useState("");
  const [
    projectPhaseAdditionErrorMessage,
    setProjectPhaseAdditionErrorMessage,
  ] = useState("");
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
    const getProjectWorkflow = async () => {
      setErrorMessage("");
      try {
        const res = await api.get<ProjectWorkFlowResponse>(
          `project/${projectId}/workflow/`
        );
        const workflow = camelize(res.data) as ProjectWorkFlow;
        setProjectWorkflow(workflow);
        setIsLoading(false);
      } catch (error) {
        handleErrors(error);
        setIsLoading(false);
      }
    };

    void getProjectWorkflow();
  }, [projectId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPhaseInput(e.target.value);
  };

  const createProjectPhase = async () => {
    setIsAddingProjectWorkflow(true);
    setProjectPhaseAdditionErrorMessage("");
    try {
      const res = await api.post<ProjectPhaseResponse>(
        `project/${projectId}/phase/create/`,
        {
          name: phaseInput,
        }
      );
      const newWorkflow = camelize(res.data) as ProjectPhase;
      setProjectWorkflow((prevState) => ({
        ...prevState,
        phases: [...prevState.phases, newWorkflow],
      }));
      setIsAddingProjectWorkflow(false);
    } catch (error) {
      setIsAddingProjectWorkflow(false);
      if (isAxiosError(error)) {
        const statusCode = error.status;

        if (statusCode === 400 || statusCode === 404) {
          const axiosError = error as AxiosError<{
            phase_name?: string;
            detail?: string;
          }>;
          setProjectPhaseAdditionErrorMessage(
            axiosError.response?.data.phase_name ||
              axiosError.response?.data.detail ||
              "An unexpected error occurred."
          );
          return;
        }

        if (statusCode && statusCode >= 500) {
          setProjectPhaseAdditionErrorMessage("A server error occurred.");
          return;
        }
        setProjectPhaseAdditionErrorMessage("An unexpected error occurred.");
      } else {
        setProjectPhaseAdditionErrorMessage("An unexpected error occurred.");
      }
    }
  };

  if (errorMessage) {
    <p className="bg-red-600 text-white rounded-lg py-4 px-2 mt-3 md:mx-10">
      {errorMessage}
    </p>;
  }

  return (
    <Container className="border-x min-h-screen">
      {isLoading ? (
        <div className="w-full h-full pt-10 text-center">
          <CircularProgress sx={{ color: "gray" }} />
        </div>
      ) : (
        <>
          {projectWorkflow.phases.length > 0 ? (
            <Stack spacing={0.5} className="pt-2">
              <p className="underline font-bold text-center text-lg">
                <span>{projectWorkflow.projectName}</span> phases:
              </p>

              <div className="md:w-1/2">
                <div className="flex justify-center">
                  <input
                    type="text"
                    className="my-1 mr-3 block grow px-3 py-2 border border-gray-300 rounded-md shadow-sm
                     focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder="Create new project phase"
                    onChange={handleChange}
                  />
                  <button
                    className="bg-blue-600 text-white rounded-md my-1 px-2"
                    onClick={createProjectPhase}
                  >
                    Create
                    {isaddingProjectWorkflow && (
                      <span className="ml-2">
                        <CircularProgress size={13} sx={{ color: "white" }} />
                      </span>
                    )}
                  </button>
                </div>
                <p className="text-red-600 text-sm">
                  {projectPhaseAdditionErrorMessage}
                </p>
              </div>

              {projectWorkflow.phases.map((workflow) => (
                <Link
                  key={workflow.phaseId}
                  to={`../phase/${workflow.phaseId}/detail/`}
                  className="block hover:bg-stone-100 rounded-md p-2 transition-colors duration-300 ease-in-out sm:max-h-24
                             md:max-h-48 overflow-y-hidden"
                >
                  <p>{workflow.phaseName}</p>
                </Link>
              ))}
            </Stack>
          ) : (
            <>
              <p className="font-bold md:text-lg">
                {projectWorkflow.projectName} does not have a workflow.
              </p>
              <p className="text-gray-500">
                Add phases to start creating, assigning and monitoring tasks.
              </p>
            </>
          )}
        </>
      )}
    </Container>
  );
};
export default ProjectPhasePage;
