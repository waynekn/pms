import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { Avatar, Container } from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";

import api from "../api";
import handleGenericApiErrors, { ErrorMessageConfig } from "../utils/errors";

import { ProjectMember, ProjectMemberResponse } from "../types/projects";
import camelize from "../utils/snakecase-to-camelcase";

const ProjectMembersList = () => {
  const [projectMembers, setProjectMembers] = useState<ProjectMember[]>([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const { projectId } = useParams();

  useEffect(() => {
    const getProjectMembers = async () => {
      if (!projectId) {
        setErrorMessage("nvalid url");
        return;
      }

      document.title = "Project members";

      try {
        const res = await api.get<ProjectMemberResponse[]>(
          `project/${projectId}/members/`
        );
        const members = res.data.map((member) =>
          camelize(member)
        ) as ProjectMember[];
        setProjectMembers(members);
        setIsLoading(false);
      } catch (error) {
        const errorMessageConfig: ErrorMessageConfig = {
          404: "Could not get project members.",
        };
        setErrorMessage(handleGenericApiErrors(error, errorMessageConfig));
        setIsLoading(false);
      }
    };

    void getProjectMembers();
  }, [projectId]);

  if (errorMessage) {
    return (
      <p className="bg-red-600 text-white rounded-lg py-4 px-2">
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
        <ul className="space-y-2">
          {projectMembers.map((member, index) => (
            <li
              key={index}
              className="font-sans font-semibold md:text-lg h-9 border-b flex items-center"
            >
              <Avatar
                src={member.profilePicture}
                alt="profile-picture"
                sx={{ width: 24, height: 24, marginRight: 1 }}
              />
              {member.username}
            </li>
          ))}
        </ul>
      )}
    </Container>
  );
};
export default ProjectMembersList;
