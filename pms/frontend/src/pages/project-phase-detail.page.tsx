import { useState, useEffect } from "react";
import { useParams } from "react-router";
import Container from "@mui/material/Container";
import Stack from "@mui/material/Stack";

import KanbanTask from "../components/kanban-task.component";
import TaskCreateForm from "../components/task-creation-form";
import ProjectPhaseDetailPlaceholder from "../placeholders/project-phase-detail.placeholder";

import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";
import handleGenericApiErrors, { ErrorMessageConfig } from "../utils/errors";

import { TaskResponse, Task } from "./project-tasks.page";
import { ProjectPhaseResponse, ProjectPhase } from "./project-phases.page";
import {
  ProjectResponse,
  Project,
} from "../components/user-projects.component";

type PhaseDetailResponse = {
  project: ProjectResponse;
  phase: ProjectPhaseResponse;
  on_hold: TaskResponse[];
  in_progress: TaskResponse[];
  completed: TaskResponse[];
};

type PhaseDetail = {
  project: Project;
  phase: ProjectPhase;
  onHold: Task[];
  inProgress: Task[];
  completed: Task[];
};

const ProjectPhaseDetail = () => {
  const initialState: PhaseDetail = {
    project: {
      createdAt: "",
      projectId: "",
      projectName: "",
      projectNameSlug: "",
      deadline: "",
      description: "",
      organization: "",
    },
    phase: { phaseId: "", phaseName: "" },
    onHold: [],
    inProgress: [],
    completed: [],
  };
  const [detail, setDetail] = useState(initialState);

  const [displayTaskCreateForm, setDisplayTaskCreateForm] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const { projectPhaseId } = useParams();

  useEffect(() => {
    const getProjectPhaseDetail = async () => {
      try {
        const res = await api.get<PhaseDetailResponse>(
          `project/phase/${projectPhaseId}/detail/`
        );
        const detail: PhaseDetail = camelize(res.data) as PhaseDetail;
        setDetail(detail);
        setIsLoading(false);
      } catch (error) {
        const messageConfig: ErrorMessageConfig = {
          400: "An unexpected error occurred.",
          404: "Could not find project phase.",
          500: "A server error occurred.",
        };
        setErrorMessage(handleGenericApiErrors(error, messageConfig));
        setIsLoading(false);
      }
    };
    void getProjectPhaseDetail();
  }, [projectPhaseId]);

  if (isLoading) {
    return <ProjectPhaseDetailPlaceholder />;
  }

  if (errorMessage) {
    return (
      <p className="bg-red-600 text-white rounded-lg py-4 px-2 mt-3 md:mx-10">
        {errorMessage}
      </p>
    );
  }

  return (
    <Container className="min-h-screen border-x">
      {/* Nav bar */}
      <nav className="flex border-b py-3 justify-center">
        <span
          className="bg-white border border-gray-300 text-gray-700 px-1 py-2
         rounded-md min-w-40 mx-2"
        >
          {detail.project.projectName}
        </span>

        <span
          className="bg-white border border-gray-300 text-gray-700 px-1 py-2
         rounded-md min-w-40 mx-2"
        >
          {detail.phase.phaseName}
        </span>

        <button
          onClick={() => setDisplayTaskCreateForm(true)}
          className="bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700"
        >
          Create Task
        </button>
      </nav>

      {/* TODO: Kanban board */}
      <main className="grid md:grid-cols-3 gap-y-3 gap-2 mt-1">
        <div>
          <h3 className="bg-bold-yellow px-2 text-lg font-bold rounded-md">
            On hold
          </h3>
          {detail.onHold.length > 0 ? (
            <Stack spacing={0.5}>
              {detail.onHold.map((task) => (
                <KanbanTask task={task} />
              ))}
            </Stack>
          ) : (
            <p className="text-gray-500">There are tasks on hold</p>
          )}
        </div>
        <div>
          <h3 className="bg-red-orange px-2 text-lg font-bold rounded-md">
            In progress
          </h3>
          {detail.inProgress.length > 0 ? (
            <Stack spacing={0.5}>
              {detail.inProgress.map((task) => (
                <KanbanTask key={task.taskId} task={task} />
              ))}
            </Stack>
          ) : (
            <p className="text-gray-500">There are no tasks in progress</p>
          )}
        </div>
        <div>
          <h3 className="bg-rich-green px-2 text-lg font-bold rounded-md">
            Completed
          </h3>
          {detail.completed.length > 0 ? (
            <Stack spacing={0.5}>
              {detail.completed.map((task) => (
                <KanbanTask task={task} />
              ))}
            </Stack>
          ) : (
            <p className="text-gray-500">There are no tasks completed</p>
          )}
        </div>
      </main>
      {/* Task creation form */}
      {displayTaskCreateForm && (
        <TaskCreateForm
          projectPhase={projectPhaseId as string}
          hideForm={() => setDisplayTaskCreateForm(false)}
        />
      )}
    </Container>
  );
};
export default ProjectPhaseDetail;
