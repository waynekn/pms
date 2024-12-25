import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { AxiosError, isAxiosError, AxiosResponse } from "axios";
import OrgAuthForm from "../components/org-auth-form.component";
import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";

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
type Project = {
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
};

// `OrganizationResponse` but with camel case keys
type Organziation = {
  organizationId: string;
  organizationName: string;
  organizationNameSlug: string;
  projects: Project[];
  isLoading: boolean;
};

const OrganizationDetail = () => {
  const initialState: Organziation = {
    organizationId: "",
    organizationName: "",
    organizationNameSlug: "",
    projects: [],
    isLoading: false,
  };
  const [organization, setOrganization] = useState<Organziation>(initialState);
  const [displayOrgAuthForm, setDisplayOrgAuthForm] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const { organizationNameSlug } = useParams();

  useEffect(() => {
    const getOrganizationDetail = async () => {
      try {
        const response = await api.post<
          { organizationNameSlug: string },
          AxiosResponse<OrganizationResponse>
        >(`organizations/detail/`, {
          organizationNameSlug,
        });
        const organization = camelize(response.data) as Organziation;

        setOrganization((prevState) => {
          return {
            ...prevState,
            ...organization,
            isLoading: false,
          };
        });
      } catch (error) {
        if (isAxiosError(error)) {
          const axiosError = error as AxiosError;

          const statusCode = axiosError.status;
          // If there is then the error is not from the server.
          if (!statusCode) {
            setErrorMessage(
              "The server is temporarily unavailable. Please try again in a while."
            );
            return;
          }

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
            setDisplayOrgAuthForm(true);
            return;
          }

          const unexpectedError = error as AxiosError<{ error: string }>;
          setErrorMessage(
            unexpectedError.response?.data.error ||
              "An unexpected error occurred."
          );
        } else {
          setErrorMessage("An unexpected error occurred.");
        }
      }
    };
    void getOrganizationDetail();
  }, [organizationNameSlug]);

  if (displayOrgAuthForm) {
    return <OrgAuthForm organizationName={organization.organizationName} />;
  }

  return (
    <div className=" flex justify-center h-full w-full">
      <main className="w-3/5 ">
        {errorMessage ? (
          <p>{errorMessage}</p>
        ) : (
          <>
            <header className="border-b-2">
              <h1 className="text-lg font-bold">
                {organization.organizationName}
              </h1>
            </header>
            {organization.projects.length > 0 ? (
              <ul className="space-y-2">
                {organization.projects.map((project) => (
                  <li key={project.projectId}>{project.projectName}</li>
                ))}
              </ul>
            ) : (
              <p>{organization.organizationName} does not have any projects</p>
            )}
          </>
        )}
      </main>
    </div>
  );
};
export default OrganizationDetail;
