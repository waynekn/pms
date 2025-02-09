import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { useParams, useNavigate } from "react-router";
import { AxiosError, isAxiosError } from "axios";
import CircularProgress from "@mui/material/CircularProgress";
import ExitToAppOutlinedIcon from "@mui/icons-material/ExitToAppOutlined";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";
import classNames from "classnames";
import OrgAuthForm from "../components/org-auth-form.component";
import OrganizationProjects from "../components/organization-projects.component";
import OrganizationAdminList from "../components/organization-admin-component";
import AssignOrganizationAdmin from "../components/organization-admin-creation.component";
import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";
import { selectCurrentUser } from "../store/user/user.selector";
import { ProjectCreationPageState } from "./project-create.page";
import handleGenericApiErrors, { ErrorMessageConfig } from "../utils/errors";

import {
  OrganizationDetailResponse,
  OrganziationDetail,
} from "../types/organization";
import { SnackBarState } from "../types/snackbar";

type Tabs = "Projects" | "Administrators" | "Add administrators";

const OrganizationDetail = () => {
  const initialState: OrganziationDetail = {
    organizationId: "",
    organizationName: "",
    organizationNameSlug: "",
    role: "Member",
    projects: [],
  };
  const [organization, setOrganization] =
    useState<OrganziationDetail>(initialState);
  const [displayOrgAuthForm, setDisplayOrgAuthForm] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoading, setIslLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<Tabs>("Projects");
  // track whether a request has been sent to exit an organization
  const [exitingOrg, setExitingOrg] = useState(false);
  const { organizationNameSlug } = useParams();
  const navigate = useNavigate();
  const currentUser = useSelector(selectCurrentUser);

  const initialSnackBarState: SnackBarState = {
    message: "",
    serverity: "success",
  };
  const [displaySnackBar, setDisplaySnackBar] = useState(false);
  const [snackBarState, setSnackBarState] =
    useState<SnackBarState>(initialSnackBarState);

  useEffect(() => {
    const getOrganizationDetail = async () => {
      try {
        const response = await api.get<OrganizationDetailResponse>(
          `organizations/${organizationNameSlug}/detail/`
        );
        const organization = camelize(response.data) as OrganziationDetail;

        setOrganization((prevState) => {
          return {
            ...prevState,
            ...organization,
          };
        });
        document.title = organization.organizationName;
        setIslLoading(false);
      } catch (error) {
        if (isAxiosError(error)) {
          const axiosError = error as AxiosError;
          const statusCode = axiosError.status;

          if (statusCode === 403) {
            const forbiddenError = error as AxiosError<{
              error: string;
              organization_name: string;
            }>;
            setOrganization((prevState) => ({
              ...prevState,
              organizationName:
                forbiddenError.response?.data.organization_name || "",
            }));
            setIslLoading(false);
            setDisplayOrgAuthForm(true);
            return;
          }

          const messageConfig: ErrorMessageConfig = {
            500: "The server is temporarily unavailable. Please try again in a while.",
          };
          setErrorMessage(handleGenericApiErrors(error, messageConfig));
          setIslLoading(false);
        } else {
          setErrorMessage("An unexpected error occurred.");
          setIslLoading(false);
        }
      }
    };
    void getOrganizationDetail();
  }, [organizationNameSlug]);

  const projectCreationFormState: ProjectCreationPageState = {
    organizationId: organization.organizationId,
    organizationName: organization.organizationName,
  };

  /**
   * Navigate manually instead of using a link to ensure state is passed properly
   * as a link will lose state if opened in a new tab.
   */
  const navigateToProjectCreationPage = async () => {
    await navigate(`../${organization.organizationNameSlug}/project/create/`, {
      state: projectCreationFormState,
    });
  };

  const exitOrg = async () => {
    try {
      if (exitingOrg) return;
      setExitingOrg(true);
      setDisplaySnackBar(false);
      await api.delete(`organizations/${organization.organizationId}/exit/`);
      setExitingOrg(false);
      await navigate(`../user/${currentUser.usernameSlug}`);
    } catch (error) {
      const errMsg = handleGenericApiErrors(error);
      setSnackBarState({
        message: errMsg,
        serverity: "error",
      });
      setDisplaySnackBar(true);
      setExitingOrg(false);
    }
  };

  if (displayOrgAuthForm) {
    return <OrgAuthForm organizationName={organization.organizationName} />;
  }

  if (errorMessage) {
    return (
      <p className="bg-red-600 text-white rounded-lg py-4 px-2 mt-3 md:mx-10">
        {errorMessage}
      </p>
    );
  }

  return (
    <div className=" flex justify-center h-full w-full">
      <main className="w-3/5 ">
        <header className="pb-3">
          <h1
            className={classNames(
              isLoading
                ? "animate-pulse sm:w-full md:w-64 h-5 mt-3 bg-gray-400"
                : "text-lg font-bold"
            )}
          >
            {organization.organizationName}
          </h1>
          <p className="my-1">
            Membership Role:
            <span className="font-bold">{organization.role}</span>
          </p>
          <button
            className="flex items-center bg-red-600 text-white hover:bg-red-700 focus:outline-none
             focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 py-2 px-4 rounded-lg text-sm
              font-semibold transition duration-300 ease-in-out"
            onClick={exitOrg}
          >
            <span className="mr-2">
              <span className="mr-2">
                <ExitToAppOutlinedIcon />
              </span>
              Exit organization
            </span>
            {exitingOrg && (
              <CircularProgress size={13} sx={{ color: "white" }} />
            )}
          </button>
          {organization.role === "Admin" && (
            <div className="flex justify-end">
              <button
                onClick={navigateToProjectCreationPage}
                className="bg-white border border-gray-300 text-gray-700 px-1 py-2 mt-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300"
              >
                Create Project
              </button>
            </div>
          )}
        </header>
        {isLoading ? (
          <div className="w-full h-full mt-10 text-center">
            <CircularProgress sx={{ color: "gray" }} />
          </div>
        ) : (
          <>
            <nav className="flex w-full border-b-2 border-blue-500 rounded-t-md">
              {/* organizations button  */}
              <button
                className={classNames(
                  "flex-1 py-2 text-center hover:bg-blue-200 focus:bg-blue-300 transition-colors border-b-4",
                  {
                    "border-blue-500": activeTab === "Projects",
                    "border-transparent": activeTab !== "Projects",
                  }
                )}
                onClick={() => setActiveTab("Projects")}
              >
                Projects
              </button>
              {/* projects button  */}
              <button
                className={classNames(
                  "flex-1 py-2 text-center hover:bg-blue-200 focus:bg-blue-300 transition-colors border-b-4",
                  {
                    "border-blue-500": activeTab === "Administrators",
                    "border-transparent": activeTab !== "Administrators",
                  }
                )}
                onClick={() => setActiveTab("Administrators")}
              >
                Administrators
              </button>
              <button
                className={classNames(
                  "flex-1 py-2 text-center hover:bg-blue-200 focus:bg-blue-300 transition-colors border-b-4",
                  {
                    "border-blue-500": activeTab === "Add administrators",
                    "border-transparent": activeTab !== "Add administrators",
                  }
                )}
                onClick={() => setActiveTab("Add administrators")}
              >
                Add administrators
              </button>
            </nav>

            {activeTab === "Projects" && (
              <>
                {organization.projects.length > 0 ? (
                  <OrganizationProjects projects={organization.projects} />
                ) : (
                  <p>
                    {organization.organizationName} does not have any projects
                  </p>
                )}
              </>
            )}
            {activeTab === "Administrators" && (
              <OrganizationAdminList
                organizationId={organization.organizationId}
                role={organization.role}
              />
            )}
            {organization.role === "Admin" &&
              activeTab === "Add administrators" && (
                <AssignOrganizationAdmin
                  organizationId={organization.organizationId}
                />
              )}
          </>
        )}
      </main>
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
    </div>
  );
};
export default OrganizationDetail;
