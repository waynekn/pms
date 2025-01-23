import { useEffect, useState } from "react";
import CircularProgress from "@mui/material/CircularProgress";
import Checkbox from "@mui/material/Checkbox";
import classNames from "classnames";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";

import {
  OrganizationMember,
  OrganizationMemberResponse,
} from "../types/organization";
import { SnackBarState } from "../types/snackbar";

import handleGenericApiErrors, { ErrorMessageConfig } from "../utils/errors";
import camelize from "../utils/snakecase-to-camelcase";
import api from "../api";
import Avatar from "@mui/material/Avatar";

type AssignOrganizationAdminProps = {
  organizationId: string;
};

const AssignOrganizationAdmin = ({
  organizationId,
}: AssignOrganizationAdminProps) => {
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [addedAdmins, setAddedAdmins] = useState<string[]>([]);
  const [nonAdmins, setNonAdmins] = useState<OrganizationMember[]>([]);
  const [displayCircularProgress, setdisplayCircularProgress] = useState(false);
  const [askForConfirmation, setAskForConfirmation] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const initialSnackBarState: SnackBarState = {
    message: "",
    serverity: "success",
  };
  const [displaySnackBar, setDisplaySnackBar] = useState(false);
  const [snackBarState, setSnackBarState] =
    useState<SnackBarState>(initialSnackBarState);

  useEffect(() => {
    const getNonOrganizationAdmins = async () => {
      try {
        const res = await api.get<OrganizationMemberResponse[]>(
          `organizations/${organizationId}/non-admins/`
        );
        const nonAdmins = res.data.map((admin) =>
          camelize(admin)
        ) as OrganizationMember[];
        setNonAdmins(nonAdmins);
        setIsLoading(false);
      } catch (error) {
        const messageConfig: ErrorMessageConfig = {
          404: "Could not get organization administrators",
        };
        setErrorMessage(handleGenericApiErrors(error, messageConfig));
        setIsLoading(false);
      }
    };
    void getNonOrganizationAdmins();
  }, [organizationId]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    checked: boolean
  ) => {
    const username = e.target.name;

    if (checked) {
      setAddedAdmins((prevMembers) => [...prevMembers, username]);
    } else {
      setAddedAdmins((prevMembers) =>
        prevMembers.filter((addedMember) => addedMember !== username)
      );
    }
  };

  const createAdmins = async () => {
    setdisplayCircularProgress(true);
    setErrorMessage("");
    try {
      await api.post(`organizations/${organizationId}/admins/create/`, {
        members: addedAdmins,
      });

      setNonAdmins((prevState) =>
        prevState.filter((nonAdmin) => !addedAdmins.includes(nonAdmin.username))
      );
      setAddedAdmins([]);
      setAskForConfirmation(false);
      setDisplaySnackBar(true);
      setSnackBarState({
        message: `${addedAdmins.length} admin(s) successfully added`,
        serverity: "success",
      });
    } catch (error) {
      const errorMsg = handleGenericApiErrors(error);
      setAskForConfirmation(false);
      setdisplayCircularProgress(false);
      setDisplaySnackBar(true);
      setSnackBarState({
        message: errorMsg,
        serverity: "error",
      });
    }
  };

  const handleClose = () => {
    setDisplaySnackBar(false);
  };

  if (errorMessage) {
    return (
      <p className="bg-red-600 text-white rounded-lg py-4 px-2 mt-3 md:mx-10">
        {errorMessage}
      </p>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <div className="text-right">
        <button
          className={classNames(
            "px-4 py-2  text-white font-semibold rounded-md ",
            addedAdmins.length === 0
              ? "cursor-not-allowed bg-gray-500 "
              : "bg-blue-500 hover:bg-blue-600 transition duration-300"
          )}
          disabled={addedAdmins.length === 0}
          onClick={() => setAskForConfirmation(true)}
        >
          Create Admins
        </button>
      </div>

      {isLoading ? (
        <div className="w-full h-full mt-10 text-center">
          <CircularProgress sx={{ color: "gray" }} />
        </div>
      ) : (
        <ul className="space-y-2">
          {nonAdmins.map((nonAdmin, index) => (
            <li
              key={index}
              className="flex items-center space-x-2 bg-gray-100 p-2 rounded-lg hover:bg-gray-200 transition duration-200"
            >
              <span className="mr-2">
                <Checkbox
                  name={nonAdmin.username}
                  checked={addedAdmins.includes(nonAdmin.username)} // Controlled Checkbox
                  onChange={handleChange}
                />
              </span>
              <p className="text-gray-800 flex">
                <Avatar
                  src={nonAdmin.profilePicture}
                  alt="profile-picture"
                  sx={{ width: 24, height: 24, marginRight: 1 }}
                />
                {nonAdmin.username}
              </p>
            </li>
          ))}
        </ul>
      )}

      {askForConfirmation && (
        <div className="fixed top-2 left-1/2 transform -translate-x-1/2 bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
          <p className="font-bold mb-4">
            Are you sure you want to assing {addedAdmins.length} member(s)
            administrator privilleges?
          </p>
          <div className="w-full flex justify-evenly space-x-4">
            <button
              className="bg-blue-500 border border-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition duration-200"
              onClick={createAdmins}
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
    </div>
  );
};

export default AssignOrganizationAdmin;
