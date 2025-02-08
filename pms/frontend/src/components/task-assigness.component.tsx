import { useState } from "react";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import Tooltip from "@mui/material/Tooltip";
import RemoveIcon from "@mui/icons-material/Remove";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";

import { ProjectMember } from "../types/projects";
import { TaskDetail } from "../types/tasks";
import { SnackBarState } from "../types/snackbar";

import api from "../api";
import handleGenericApiErrors from "../utils/errors";

type TaskAssignessProps = {
  assignees: ProjectMember[];
  role: TaskDetail["role"];
  taskId: TaskDetail["taskId"];
};

const TaskAssigness = ({ assignees, role, taskId }: TaskAssignessProps) => {
  const [assignments, setAssignments] = useState(assignees);
  const initialSnackBarState: SnackBarState = {
    message: "",
    serverity: "success",
  };
  const [displaySnackBar, setDisplaySnackBar] = useState(false);
  const [snackBarState, setSnackBarState] =
    useState<SnackBarState>(initialSnackBarState);

  const deleteTaskAssignment = async (username: string) => {
    try {
      await api.delete(`assignment/${taskId}/delete/`, {
        data: {
          assignee: username,
        },
      });
      setAssignments(
        assignments.filter((assignee) => assignee.username != username)
      );
      setSnackBarState({
        message: "Assignment successfully removed",
        serverity: "success",
      });
      setDisplaySnackBar(true);
    } catch (error) {
      const errMsg = handleGenericApiErrors(error);
      setSnackBarState({
        message: errMsg,
        serverity: "error",
      });
      setDisplaySnackBar(true);
    }
  };

  return (
    <>
      {assignments.length > 0 ? (
        <Stack>
          {assignments.map((user, index) => (
            <li
              key={index}
              className="font-sans font-semibold md:text-lg h-9 border-b flex items-center"
            >
              <span className="flex items-center grow">
                <Avatar
                  src={user.profilePicture}
                  alt="profile-picture"
                  sx={{ width: 24, height: 24, marginRight: 1 }}
                />
                {user.username}
              </span>
              {role === "Manager" && (
                <Tooltip title="Remove assignment" placement="top">
                  <button
                    className="hover:bg-red-500 hover:text-white rounded-full transition-colors duration-300"
                    onClick={() => deleteTaskAssignment(user.username)}
                  >
                    <RemoveIcon />
                  </button>
                </Tooltip>
              )}
            </li>
          ))}
        </Stack>
      ) : (
        <p className="text-gray-500">No users have been assigned this task</p>
      )}
      <Snackbar
        open={displaySnackBar}
        autoHideDuration={6000}
        onClose={() => setDisplaySnackBar(false)}
      >
        <Alert
          onClose={() => setDisplaySnackBar(false)}
          severity={snackBarState.serverity}
          variant="filled"
          sx={{ width: "100%" }}
        >
          {snackBarState.message}
        </Alert>
      </Snackbar>
    </>
  );
};
export default TaskAssigness;
