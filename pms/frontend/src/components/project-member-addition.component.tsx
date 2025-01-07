import { useEffect, useState } from "react";
import classNames from "classnames";
import { AxiosError, isAxiosError } from "axios";
import { useParams, useNavigate } from "react-router";
import Checkbox from "@mui/material/Checkbox";
import CloseIcon from "@mui/icons-material/Close";
import CircularProgress from "@mui/material/CircularProgress";

import api from "../api";

type NonProjectMember = {
  username: string;
};

const NonProjectMembersList = () => {
  const [nonProjectMembers, setNonProjectMembers] = useState<
    NonProjectMember[]
  >([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [addedMembers, setAddedMembers] = useState<string[]>([]);
  const [askForConfirmation, setAskForConfirmation] = useState(false);
  const [displayCircularProgress, setdisplayCircularProgress] = useState(false);

  const { projectId } = useParams();
  const navigate = useNavigate();

  const handleErrors = (error: unknown) => {
    if (isAxiosError(error)) {
      const statusCode = error.status;

      if (!statusCode) {
        setErrorMessage("An unexpected error occurred");
        return;
      }

      if (statusCode === 400) {
        const axiosError = error as AxiosError<{ error: string }>;
        setErrorMessage(
          axiosError.response?.data.error || "An unexpected error occurred"
        );
        return;
      }

      if (statusCode === 404) {
        const axiosError = error as AxiosError<{ detail: string }>;
        setErrorMessage(
          axiosError.response?.data.detail || "An unexpected error occurred"
        );
        return;
      }

      setErrorMessage("An unexpected error occurred");
    } else {
      setErrorMessage("An unexpected error occurred");
    }
  };

  useEffect(() => {
    const getNonProjectMembers = async () => {
      if (!projectId) {
        return setErrorMessage("Invalid url");
      }

      try {
        const res = await api.get<NonProjectMember[]>(
          `project/${projectId}/non-members/`
        );
        setNonProjectMembers(res.data);
      } catch (error) {
        handleErrors(error);
      }
    };
    void getNonProjectMembers();
  }, [projectId]);

  const addMembers = async () => {
    setdisplayCircularProgress(true);
    setErrorMessage("");

    try {
      await api.post(`project/${projectId}/members/add/`, {
        members: addedMembers,
      });

      await navigate("../members/");
    } catch (error) {
      handleErrors(error);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    checked: boolean
  ) => {
    const username = e.target.name;

    if (checked) {
      setAddedMembers((prevMembers) => [...prevMembers, username]);
    } else {
      setAddedMembers((prevMembers) =>
        prevMembers.filter((addedMember) => addedMember !== username)
      );
    }
  };

  if (errorMessage) {
    return (
      <div className="bg-red-600 text-white rounded-lg py-4 px-2 flex">
        <p className="font-bold grow">{errorMessage}</p>
        <span
          onClick={() => (
            setErrorMessage(""),
            setAskForConfirmation(false),
            setdisplayCircularProgress(false),
            setAddedMembers([])
          )}
        >
          <CloseIcon />
        </span>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <div className="text-right">
        <button
          className={classNames(
            "px-4 py-2  text-white font-semibold rounded-md ",
            addedMembers.length === 0
              ? "cursor-not-allowed bg-gray-500 "
              : "bg-blue-500 hover:bg-blue-600 transition duration-300"
          )}
          disabled={addedMembers.length === 0}
          onClick={() => setAskForConfirmation(true)}
        >
          Add members
        </button>
      </div>

      <ul className="space-y-2">
        {nonProjectMembers.map((nonProjectMember, index) => (
          <li
            key={index}
            className="flex items-center space-x-2 bg-gray-100 p-2 rounded-lg hover:bg-gray-200 transition duration-200"
          >
            <span className="mr-2">
              <Checkbox
                name={nonProjectMember.username}
                onChange={handleChange}
              />
            </span>
            <span className="text-gray-800">{nonProjectMember.username}</span>
          </li>
        ))}
      </ul>

      {askForConfirmation && (
        <div className="fixed top-2 left-1/2 transform -translate-x-1/2 bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
          <p className="font-bold mb-4">
            Are you sure you want to add {addedMembers.length} member(s) to your
            project?
          </p>
          <div className="w-full flex justify-evenly space-x-4">
            <button
              className="bg-blue-500 border border-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition duration-200"
              onClick={addMembers}
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
    </div>
  );
};
export default NonProjectMembersList;