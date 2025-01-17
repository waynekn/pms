import { ProjectMember, ProjectPhase, ProjectPhaseResponse } from "./projects";

export type TaskResponse = {
  task_id: string;
  task_name: string;
  start_date: string;
  deadline: string;
  status: "IN_PROGRESS" | "ON_HOLD" | "DONE";
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

export type TaskDetailResponse = TaskResponse & { assignees: ProjectMember[] };

export type TaskDetail = Task & {
  assignees: ProjectMember[];
  role: "Manager" | "Member";
};
