import { useEffect, useState } from "react";
import classNames from "classnames";
import { useParams } from "react-router";
import Container from "@mui/material/Container";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";
import DoneAllIcon from "@mui/icons-material/DoneAll";

import TaskAssigness from "../components/task-assigness.component";
import TaskAssignmentComponent from "../components/task-assignment.component";
import { TaskDetail, TaskDetailResponse } from "../types/tasks";
import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";
import handleGenericApiErrors, { ErrorMessageConfig } from "../utils/errors";

import { SnackBarState } from "../types/snackbar";

type Tabs = "description" | "assignees" | "add members";

const TaskDetailPage = () => {
  const initialState: TaskDetail = {
    taskId: "",
    taskName: "",
    startDate: "",
    deadline: "",
    status: "IN_PROGRESS",
    role: "Member",
    description: "",
    projectPhase: { phaseId: "", phaseName: "" },
    assignees: [],
  };
  const [taskDetail, setTaskDetail] = useState<TaskDetail>(initialState);
  const [activeTab, setActiveTab] = useState<Tabs>("description");
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const { taskId } = useParams();

  const initialSnackBarState: SnackBarState = {
    message: "",
    serverity: "success",
  };
  const [displaySnackBar, setDisplaySnackBar] = useState(false);
  const [snackBarState, setSnackBarState] =
    useState<SnackBarState>(initialSnackBarState);

  useEffect(() => {
    const getTaskDetail = async () => {
      try {
        const res = await api.get<TaskDetailResponse>(`task/detail/${taskId}/`);
        const data = camelize(res.data) as TaskDetail;
        document.title = data.taskName;
        setTaskDetail(data);
        setIsLoading(false);
      } catch (error) {
        const messageConfig: ErrorMessageConfig = {
          400: "An unexpected error occurred.",
          404: "An unexpected error occurred.",
          500: "A server error occurred.",
        };
        setErrorMessage(handleGenericApiErrors(error, messageConfig));
        setIsLoading(false);
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

  const handleClose = () => {
    setDisplaySnackBar(false);
  };

  const changeTaskStatus = async (status: TaskDetail["status"]) => {
    setDisplaySnackBar(false);
    setSnackBarState(initialSnackBarState);
    try {
      await api.put(`task/${taskDetail.taskId}/status/update/`, {
        status,
      });
      setTaskDetail((detail) => ({
        ...detail,
        status: status,
      }));
      setDisplaySnackBar(true);
      setSnackBarState({
        message: `Task status successfully updated`,
        serverity: "success",
      });
    } catch (error) {
      const errorMsg = handleGenericApiErrors(error);
      setSnackBarState({ message: errorMsg, serverity: "error" });
      setDisplaySnackBar(true);
    }
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
      {isLoading ? (
        <div className="w-full h-full pt-10 text-center">
          <CircularProgress sx={{ color: "gray" }} />
        </div>
      ) : (
        <>
          <header>
            <h1 className="text-lg font-bold">{taskDetail.taskName}</h1>
            <h2 className="italic text-gray-500">
              {taskDetail.projectPhase.phaseName} phase
            </h2>
            <h3 className="text-gray-500">
              Created on {getDate(taskDetail.startDate)}
            </h3>
            {/* Section to change task status */}

            {taskDetail.status === "DONE" ? (
              <DoneAllIcon sx={{ color: "green" }} />
            ) : (
              <div className="flex justify-center mt-1">
                <div className="flex justify-evenly w-full md:w-3/4 ">
                  <button
                    disabled={taskDetail.status === "ON_HOLD"}
                    className={classNames(
                      "bg-bold-yellow px-2 font-bold rounded-md",
                      taskDetail.status === "ON_HOLD"
                        ? "cursor-not-allowed"
                        : "cursor-pointer"
                    )}
                    onClick={() => changeTaskStatus("ON_HOLD")}
                  >
                    Pause task
                  </button>
                  <button
                    disabled={taskDetail.status === "IN_PROGRESS"}
                    className={classNames(
                      "bg-red-orange px-2 font-bold rounded-md",
                      taskDetail.status === "IN_PROGRESS"
                        ? "cursor-not-allowed"
                        : "cursor-pointer"
                    )}
                    onClick={() => changeTaskStatus("IN_PROGRESS")}
                  >
                    Resume
                  </button>
                  <button
                    className={classNames(
                      "bg-rich-green px-2 font-bold rounded-md"
                    )}
                    onClick={() => changeTaskStatus("DONE")}
                  >
                    Complete
                  </button>
                </div>
              </div>
            )}
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
              {/* Only display option to assign task to project managers*/}
              {taskDetail.role === "Manager" && (
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
              )}
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

          <Snackbar
            open={displaySnackBar}
            autoHideDuration={6000}
            onClose={handleClose}
          >
            <Alert
              onClose={handleClose}
              severity={snackBarState.serverity}
              variant="filled"
              sx={{ width: "100%" }}
            >
              {snackBarState.message}
            </Alert>
          </Snackbar>
        </>
      )}
    </Container>
  );
};
export default TaskDetailPage;
