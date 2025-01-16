import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router";
import { AxiosError, isAxiosError } from "axios";
import CircularProgress from "@mui/material/CircularProgress";
import classNames from "classnames";
import OrgAuthForm from "../components/org-auth-form.component";
import OrganizationProjects from "../components/organization-projects.component";
import OrganizationAdminList from "../components/organization-admin-component";
import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";
import { ProjectCreationPageState } from "./project-create.page";
import handleGenericApiErrors, { ErrorMessageConfig } from "../utils/errors";

// Projects response from API.
type ProjectResponse = {
  project_id: string;
  project_name: string;
  project_name_slug: string;
  description: string;
  created_at: string;
  deadline: string;
  status: string;
};

// `ProjectResponse` but with camel case keys
export type Project = {
  projectId: string;
  projectName: string;
  projectNameSlug: string;
  description: string;
  createdAt: string;
  deadline: string;
  status: string;
};

// Organization response from API.
type OrganizationResponse = {
  organization_id: string;
  organization_name: string;
  organization_name_slug: string;
  projects: ProjectResponse[];
  role: "Member" | "Admin";
};

// `OrganizationResponse` but with camel case keys
type Organziation = {
  organizationId: string;
  organizationName: string;
  organizationNameSlug: string;
  role: "Member" | "Admin";
  projects: Project[];
};

export type OrganizationMember = {
  username: string;
};

type Tabs = "Projects" | "Administrators" | "Add administrators";

const OrganizationDetail = () => {
  const initialState: Organziation = {
    organizationId: "",
    organizationName: "",
    organizationNameSlug: "",
    role: "Member",
    projects: [],
  };
  const [organization, setOrganization] = useState<Organziation>(initialState);
  const [displayOrgAuthForm, setDisplayOrgAuthForm] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoading, setIslLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<Tabs>("Projects");
  const { organizationNameSlug } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const getOrganizationDetail = async () => {
      try {
        const response = await api.get<OrganizationResponse>(
          `organizations/${organizationNameSlug}/detail/`
        );
        const organization = camelize(response.data) as Organziation;

        setOrganization((prevState) => {
          return {
            ...prevState,
            ...organization,
          };
        });
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
              />
            )}
          </>
        )}
      </main>
    </div>
  );
};
export default OrganizationDetail;
