import { Organization, OrganizationResponse } from "./organization";
import { Task, TaskResponse } from "./tasks";

export type ProjectMember = {
  username: string;
};

export type ProjectResponse = {
  created_at: string;
  deadline: string;
  description: string;
  project_id: string;
  project_name: string;
  project_name_slug: string;
  organization: OrganizationResponse;
};

export type Project = Omit<
  ProjectResponse,
  | "created_at"
  | "project_id"
  | "project_name"
  | "project_name_slug"
  | "organization"
> & {
  createdAt: string;
  projectName: string;
  projectId: string;
  projectNameSlug: string;
  organization: Organization;
};

export type ProjectStatsResponse = {
  tasks: number;
  members: number;
  description: string;
  tasks_in_progress: number;
  tasks_on_hold: number;
  tasks_completed: number;
  percentage_completion: number;
};

export type ProjectStats = Omit<
  ProjectStatsResponse,
  | "tasks_in_progress"
  | "tasks_on_hold"
  | "tasks_completed"
  | "percentage_completion"
> & {
  tasksInProgress: number;
  tasksOnHold: number;
  tasksCompleted: number;
  percentageCompletion: number;
};

export type ProjectPhaseResponse = {
  phase_id: string;
  phase_name: string;
};

export type ProjectPhase = {
  phaseId: string;
  phaseName: string;
};

export type ProjectTasksResponse = ProjectResponse & {
  tasks: TaskResponse[];
};

export type ProjectTasks = Project & {
  tasks: Task[];
};

/**
 * Detail of a phase of a project.
 */
export type PhaseDetailResponse = {
  project: ProjectResponse;
  phase: ProjectPhaseResponse;
  role: "Manager" | "Member";
  on_hold: TaskResponse[];
  in_progress: TaskResponse[];
  completed: TaskResponse[];
};

export type PhaseDetail = {
  project: Project;
  phase: ProjectPhase;
  role: "Manager" | "Member";
  onHold: Task[];
  inProgress: Task[];
  completed: Task[];
};
