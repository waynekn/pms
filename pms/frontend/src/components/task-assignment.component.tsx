import { useEffect, useState } from "react";
import classNames from "classnames";

import Avatar from "@mui/material/Avatar";
import CircularProgress from "@mui/material/CircularProgress";

import { ProjectMember, ProjectMemberResponse } from "../types/projects";
import api from "../api";
import Checkbox from "@mui/material/Checkbox";
import handleGenericApiErrors, { ErrorMessageConfig } from "../utils/errors";
import camelize from "../utils/snakecase-to-camelcase";

type TaskAssignmentComponentProps = {
  taskId: string;
  changeTab: () => void;
};

const TaskAssignmentComponent = ({
  taskId,
  changeTab,
}: TaskAssignmentComponentProps) => {
  const [nonAssignees, setNonAssignees] = useState<ProjectMember[]>([]);
  const [assignees, setAssignees] = useState<string[]>([]);
  const [displayCircularProgress, setdisplayCircularProgress] = useState(false);
  const [askForConfirmation, setAskForConfirmation] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const getNonAssignees = async () => {
      try {
        const res = await api.get<ProjectMemberResponse[]>(
          `task/${taskId}/non-assignees/`
        );
        const members = res.data.map((member) =>
          camelize(member)
        ) as ProjectMember[];
        setNonAssignees(members);
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
    void getNonAssignees();
  }, [taskId]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    checked: boolean
  ) => {
    const username = e.target.name;

    if (checked) {
      setAssignees((prevMembers) => [...prevMembers, username]);
    } else {
      setAssignees((prevMembers) =>
        prevMembers.filter((addedMember) => addedMember !== username)
      );
    }
  };

  const assignTask = async () => {
    if (isLoading) return;
    setdisplayCircularProgress(true);
    try {
      await api.post(`task/${taskId}/assign/`, { assignees });
      setIsLoading(false);
      setdisplayCircularProgress(false);
      setAskForConfirmation(false);
      changeTab();
    } catch (error) {
      const messageConfig: ErrorMessageConfig = {
        400: "An unexpected error occurred.",
        404: "An unexpected error occurred.",
        500: "A server error occurred.",
      };
      setErrorMessage(handleGenericApiErrors(error, messageConfig));
      setdisplayCircularProgress(false);
      setAskForConfirmation(false);
    }
  };

  if (isLoading) {
    return (
      <section className="text-center mt-5">
        <CircularProgress size={50} sx={{ color: "grey" }} />
      </section>
    );
  }

  if (errorMessage) {
    return (
      <p className="bg-red-600 text-white rounded-lg py-4 px-2 mt-3 md:mx-10">
        {errorMessage}
      </p>
    );
  }

  return (
    <>
      <div className="text-right mb-3">
        <button
          className={classNames(
            "px-4 py-2  text-white font-semibold rounded-md ",
            assignees.length === 0
              ? "cursor-not-allowed bg-gray-500 "
              : "bg-blue-500 hover:bg-blue-600 transition duration-300"
          )}
          disabled={assignees.length === 0}
          onClick={() => setAskForConfirmation(true)}
        >
          Assign task
        </button>
      </div>
      <ul className="space-y-2">
        {nonAssignees.map((nonAssignee, index) => (
          <li
            key={index}
            className="flex items-center space-x-2 bg-gray-100 p-2 rounded-lg hover:bg-gray-200 transition duration-200"
          >
            <span className="mr-2">
              <Checkbox name={nonAssignee.username} onChange={handleChange} />
            </span>
            <p className="text-gray-800 flex">
              <Avatar
                src={nonAssignee.profilePicture}
                alt="profile-picture"
                sx={{ width: 24, height: 24, marginRight: 1 }}
              />
              {nonAssignee.username}
            </p>
          </li>
        ))}
      </ul>
      {askForConfirmation && (
        <div className="fixed top-2 left-1/2 transform -translate-x-1/2 bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
          <p className="font-bold mb-4">
            Are you sure you want to assign {assignees.length} member(s) this
            task?
          </p>
          <div className="w-full flex justify-evenly space-x-4">
            <button
              className="bg-blue-500 border border-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition duration-200"
              onClick={assignTask}
              disabled={isLoading}
            >
              Yes, Proceed
              {displayCircularProgress && (
                <span className="ml-2">
                  <CircularProgress size={15} sx={{ color: "white" }} />
                </span>
              )}
            </button>

            <button
              className="bg-white border border-gray-300 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-100
                   focus:outline-none focus:ring-2 focus:ring-gray-300 transition duration-200"
              onClick={() => (
                setAskForConfirmation(false), setdisplayCircularProgress(false)
              )}
            >
              No, Cancel
            </button>
          </div>
        </div>
      )}
    </>
  );
};
export default TaskAssignmentComponent;
