import { useEffect, useState } from "react";
import { Link } from "react-router";
import { isAxiosError } from "axios";
import Stack from "@mui/material/Stack";
import CircularProgress from "@mui/material/CircularProgress";
import AccessTimeOutlinedIcon from "@mui/icons-material/AccessTimeOutlined";

import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";

export type ProjectResponse = {
  created_at: string;
  deadline: string;
  description: string;
  project_id: string;
  project_name: string;
  project_name_slug: string;
  template?: string; // the template this project was made from
  organization: string; // the primary key of the organization
  // this project belongs to
};

export type Project = Omit<
  ProjectResponse,
  "created_at" | "project_id" | "project_name" | "project_name_slug"
> & {
  createdAt: string;
  projectName: string;
  projectId: string;
  projectNameSlug: string;
};

const UserProjectsDisplay = () => {
  const [userProjects, setUserProjects] = useState<Project[]>([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIslLoading] = useState(true);

  useEffect(() => {
    const getUserProjects = async () => {
      setErrorMessage("");
      try {
        const res = await api.get<ProjectResponse[]>("user/projects/");
        const projects = res.data.map((project) =>
          camelize(project)
        ) as Project[];
        setUserProjects(projects);
        setIslLoading(false);
      } catch (error) {
        if (isAxiosError(error)) {
          const statuscode = error.status;

          if (!statuscode) {
            setErrorMessage(
              "The server is temporarily unavailabe. Please try again in a while."
            );
            setIslLoading(false);
            return;
          }

          setErrorMessage("An unexpected error occured ");
          setIslLoading(false);
        } else {
          setErrorMessage("An unexpected error occured");
          setIslLoading(false);
        }
      }
    };
    void getUserProjects();
  }, []);

  const getDate = (deadline: string) => {
    const dateObj = new Date(deadline);
    const dateStr = `${dateObj.getFullYear()}/${(dateObj.getMonth() + 1)
      .toString()
      .padStart(2, "0")}/${dateObj.getDate().toString().padStart(2, "0")}`;
    return dateStr;
  };

  if (errorMessage) {
    return <p className="text-red-500">{errorMessage}</p>;
  }

  return (
    <div>
      {isLoading ? (
        <div className="w-full h-full mt-10 text-center">
          <CircularProgress sx={{ color: "gray" }} />
        </div>
      ) : (
        <>
          {userProjects.length > 0 ? (
            <Stack spacing={0.5}>
              {userProjects.map((project) => (
                <Link
                  key={project.projectId}
                  to={`../${project.projectId}/${project.projectNameSlug}`}
                  className="block hover:bg-stone-100 rounded-md p-2 transition-colors duration-300 ease-in-out sm:max-h-24
                         md:max-h-48 overflow-y-hidden"
                >
                  <p className="text-lg font-bold">{project.projectName}</p>
                  <p className="flex items-center">
                    <AccessTimeOutlinedIcon
                      sx={{ color: "grey" }}
                      fontSize="small"
                    />
                    <span className="ml-3 text-gray-600">
                      {getDate(project.deadline)}
                    </span>
                  </p>
                  <p className="text-gray-600">{project.description}</p>
                </Link>
              ))}
            </Stack>
          ) : (
            <p>You are not a member of any project</p>
          )}
        </>
      )}
    </div>
  );
};

export default UserProjectsDisplay;
