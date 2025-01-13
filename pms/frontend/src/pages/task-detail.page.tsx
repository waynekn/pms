import { useEffect, useState } from "react";
import classNames from "classnames";
import { useParams } from "react-router";
import { AxiosError, isAxiosError } from "axios";
import Container from "@mui/material/Container";

import { Task, TaskResponse } from "../pages/project-tasks.page";
import TaskAssigness from "../components/task-assigness.component";
import TaskAssignmentComponent from "../components/task-assignment.component";
import { ProjectMember } from "../components/project-members-list.component";

import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";

type TaskDetailResponse = TaskResponse & { assignees: ProjectMember[] };

type TaskDetail = Task & { assignees: ProjectMember[] };

type Tabs = "description" | "assignees" | "add members";

const TaskDetailPage = () => {
  const initialState: TaskDetail = {
    taskId: "",
    taskName: "",
    startDate: "",
    deadline: "",
    description: "",
    projectPhase: { phaseId: "", phaseName: "" },
    assignees: [],
  };
  const [taskDetail, setTaskDetail] = useState<TaskDetail>(initialState);
  const [activeTab, setActiveTab] = useState<Tabs>("description");
  const [errorMessage, setErrorMessage] = useState("");
  const { taskId } = useParams();

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
    const getTaskDetail = async () => {
      try {
        const res = await api.get<TaskDetailResponse>(`task/detail/${taskId}/`);
        const data = camelize(res.data) as TaskDetail;
        setTaskDetail(data);
      } catch (error) {
        handleErrors(error);
      }
    };
    void getTaskDetail();
  }, [taskId]);

  const getDate = (date: string) => {
    const dateObj = new Date(date);
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
    <Container className="min-h-screen border-x">
      <header>
        <h1 className="text-lg font-bold">{taskDetail.taskName}</h1>
        <h2 className="italic text-gray-500">
          {taskDetail.projectPhase.phaseName} phase
        </h2>
        <h3 className="text-gray-500">
          Created on {getDate(taskDetail.startDate)}
        </h3>
      </header>
      <div className="flex flex-col w-3/4 mx-auto bg-white shadow-lg rounded-lg p-6 relative top-10">
        <nav className="flex w-full border-b-2 border-blue-500 rounded-t-md">
          {/* Task description button  */}
          <button
            className={classNames(
              "flex-1 py-2 text-center hover:bg-blue-200 focus:bg-blue-300 transition-colors border-b-4",
              {
                "border-blue-500": activeTab === "description",
                "border-transparent": activeTab !== "description",
              }
            )}
            onClick={() => setActiveTab("description")}
          >
            Task Descrption
          </button>
          {/* Assignees button  */}
          <button
            className={classNames(
              "flex-1 py-2 text-center hover:bg-blue-200 focus:bg-blue-300 transition-colors border-b-4",
              {
                "border-blue-500": activeTab === "assignees",
                "border-transparent": activeTab !== "assignees",
              }
            )}
            onClick={() => setActiveTab("assignees")}
          >
            Assignees
          </button>
          {/* Members addition  */}
          <button
            className={classNames(
              "flex-1 py-2 text-center hover:bg-blue-200 focus:bg-blue-300 transition-colors border-b-4",
              {
                "border-blue-500": activeTab === "add members",
                "border-transparent": activeTab !== "add members",
              }
            )}
            onClick={() => setActiveTab("add members")}
          >
            Assign members
          </button>
        </nav>
        <section className="w-full rounded-b-md p-4">
          {activeTab === "description" && <p>{taskDetail.description}</p>}
          {activeTab === "assignees" && (
            <TaskAssigness assignees={taskDetail.assignees} />
          )}
          {activeTab === "add members" && (
            <TaskAssignmentComponent
              taskId={taskDetail.taskId}
              changeTab={() => setActiveTab("assignees")}
            />
          )}
        </section>
      </div>
    </Container>
  );
};
export default TaskDetailPage;