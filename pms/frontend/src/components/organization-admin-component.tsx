import { useEffect, useState } from "react";
import Container from "@mui/material/Container";
import CircularProgress from "@mui/material/CircularProgress";
import Avatar from "@mui/material/Avatar";

import {
  OrganizationMember,
  OrganizationMemberResponse,
} from "../types/organization";

import handleGenericApiErrors, { ErrorMessageConfig } from "../utils/errors";
import camelize from "../utils/snakecase-to-camelcase";
import api from "../api";

type OrganizationAdminListProps = {
  organizationId: string;
};

const OrganizationAdminList = ({
  organizationId,
}: OrganizationAdminListProps) => {
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [admins, setAdmins] = useState<OrganizationMember[]>([]);
  const [isLoading, setIsLoading] = useState(true);

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
                <Avatar
                  src={admin.profilePicture}
                  alt="profile-picture"
                  sx={{ width: 24, height: 24, marginRight: 1 }}
                />
                <span>{admin.username}</span>
              </div>
            </li>
          ))}
        </ol>
      )}
    </Container>
  );
};

export default OrganizationAdminList;
