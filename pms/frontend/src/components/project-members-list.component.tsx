import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { isAxiosError } from "axios";
import { Container } from "@mui/material";

import api from "../api";

type ProjectMember = {
  username: string;
};

const ProjectMembersList = () => {
  const [projectMembers, setProjectMembers] = useState<ProjectMember[]>([]);
  const [errorMessage, setErrorMessage] = useState("");
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
      } catch (error) {
        if (isAxiosError(error)) {
          const statusCode = error.status;

          if (statusCode === 404) {
            setErrorMessage("Could not get project members.");
            return;
          }

          setErrorMessage("An unknown error occured.");
        } else {
          setErrorMessage("An unkown error occured.");
        }
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
    </Container>
  );
};
export default ProjectMembersList;
