import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { Container } from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";

import api from "../api";
import handleGenericApiErrors, { ErrorMessageConfig } from "../utils/errors";

export type ProjectMember = {
  username: string;
};

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

      try {
        const res = await api.get<ProjectMember[]>(
          `project/${projectId}/members/`
        );
        setProjectMembers(res.data);
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
              className="font-sans font-semibold md:text-lg h-9 border-b"
            >
              {member.username}
            </li>
          ))}
        </ul>
      )}
    </Container>
  );
};
export default ProjectMembersList;
