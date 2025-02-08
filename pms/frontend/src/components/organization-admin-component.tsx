import { useEffect, useState } from "react";
import Container from "@mui/material/Container";
import CircularProgress from "@mui/material/CircularProgress";
import Avatar from "@mui/material/Avatar";
import Snackbar from "@mui/material/Snackbar";
import RemoveIcon from "@mui/icons-material/Remove";
import Alert from "@mui/material/Alert";

import {
  OrganziationDetail,
  OrganizationMember,
  OrganizationMemberResponse,
} from "../types/organization";
import { SnackBarState } from "../types/snackbar";

import handleGenericApiErrors, { ErrorMessageConfig } from "../utils/errors";
import camelize from "../utils/snakecase-to-camelcase";
import api from "../api";
import Tooltip from "@mui/material/Tooltip";

type OrganizationAdminListProps = {
  organizationId: string;
  role: OrganziationDetail["role"];
};

const OrganizationAdminList = ({
  organizationId,
  role,
}: OrganizationAdminListProps) => {
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [admins, setAdmins] = useState<OrganizationMember[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const initialSnackBarState: SnackBarState = {
    message: "",
    serverity: "success",
  };
  const [displaySnackBar, setDisplaySnackBar] = useState(false);
  const [snackBarState, setSnackBarState] =
    useState<SnackBarState>(initialSnackBarState);

  useEffect(() => {
    const getOrganizationAdmins = async () => {
      try {
        const res = await api.get<OrganizationMemberResponse[]>(
          `organizations/${organizationId}/admins/`
        );
        const admins = res.data.map((admin) =>
          camelize(admin)
        ) as OrganizationMember[];

        setAdmins(admins);
        setIsLoading(false);
      } catch (error) {
        const messageConfig: ErrorMessageConfig = {
          404: "Could not get organization administrators",
        };
        setErrorMessage(handleGenericApiErrors(error, messageConfig));
        setIsLoading(false);
      }
    };
    void getOrganizationAdmins();
  }, [organizationId]);

  const deleteOrgAdmin = async (username: string) => {
    try {
      await api.put(`organizations/${organizationId}/admin/revoke/`, {
        admin: username,
      });
      setAdmins(admins.filter((admin) => admin.username != username));
      setSnackBarState({
        message: "Admin successfully removed",
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

  if (errorMessage) {
    return (
      <p className="bg-red-600 text-white rounded-lg py-4 px-2 mt-3 md:mx-10">
        {errorMessage}
      </p>
    );
  }

  return (
    <Container>
      {isLoading ? (
        <div className="w-full h-full mt-10 text-center">
          <CircularProgress sx={{ color: "gray" }} />
        </div>
      ) : (
        <ol className="space-y-2 w-full list-decimal mt-1">
          {admins.map((admin, index) => (
            <li
              key={index}
              className="font-sans w-full font-semibold md:text-lg border-b"
            >
              <div className="flex content-center">
                <div className="flex content-center grow">
                  <Avatar
                    src={admin.profilePicture}
                    alt="profile-picture"
                    sx={{ width: 24, height: 24, marginRight: 1 }}
                  />
                  <span>{admin.username}</span>
                </div>

                {role === "Admin" && (
                  <Tooltip title="Remove admin privelledges" placement="top">
                    <button
                      className="hover:bg-red-500 hover:text-white rounded-full transition-colors duration-300"
                      onClick={() => deleteOrgAdmin(admin.username)}
                    >
                      <RemoveIcon />
                    </button>
                  </Tooltip>
                )}
              </div>
            </li>
          ))}
        </ol>
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
    </Container>
  );
};

export default OrganizationAdminList;
