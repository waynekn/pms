import { useState, useEffect } from "react";
import { AxiosResponse } from "axios";
import { Link } from "react-router";
import { debounce } from "lodash";
import camelize from "../utils/snakecase-to-camelcase";
import api from "../api";

export type OrganizationResponse = {
  organization_id: string;
  organization_name: string;
  organization_name_slug: string;
};

export type Organization = {
  organizationId: string;
  organizationName: string;
  organizationNameSlug: string;
};

type OrganizationQuery = {
  organization_name_query: string;
};

// Text to display when no user organizations are found or
// an error occured during fetching.
type FallBackText =
  | "You are currently not a member of any organization."
  | "An error occured while fetching organizations. Please try again in a while.";

const OrganizationComponent = () => {
  const [userOrganizations, setUserOrganizations] = useState<Organization[]>(
    []
  );
  const [searchedOrganizations, setSearchedOrganizations] = useState<
    Organization[]
  >([]);
  const [fallBackText, setFallBackText] = useState<FallBackText>(
    "You are currently not a member of any organization."
  );

  useEffect(() => {
    const fetchUserOrganizations = async () => {
      try {
        const response = await api.get<OrganizationResponse[]>(
          "organizations/"
        );

        const organizations = response.data.map((organization) =>
          camelize(organization)
        ) as Organization[];

        setUserOrganizations(organizations);
      } catch {
        setFallBackText(
          "An error occured while fetching organizations. Please try again in a while."
        );
      }
    };
    void fetchUserOrganizations();
  }, []);

  /**
   * Fetches organizations that a user searches.
   */
  const searchOrganizations = debounce(async (organizationName: string) => {
    try {
      const response = await api.post<
        OrganizationQuery,
        AxiosResponse<OrganizationResponse[]>
      >("organizations/search/", { organization_name_query: organizationName });

      const organizations = response.data.map((organization) =>
        camelize(organization)
      ) as Organization[];

      setSearchedOrganizations(organizations);
    } catch {
      setSearchedOrganizations([]);
    }
  }, 300);

  return (
    <div>
      <div className="flex">
        <div className="flex flex-col relative grow mr-5">
          <div className="relative">
            {/* search div input tag  */}
            <input
              className="w-full bg-white border border-gray-300 text-gray-700 px-4 py-2 mt-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300"
              id="search-bar"
              type="search"
              onChange={(e) => {
                void searchOrganizations(e.target.value);
              }}
              name="organization_name_query"
              placeholder="Search for an organization"
            />
          </div>

          {/* Display searched organizations. */}

          {searchedOrganizations.length > 0 && (
            <div className="w-full absolute border-2 border-red-600 top-12 z-50 mt-2 border-2">
              <ul className="w-full bg-white shadow-lg rounded-md mt-1 z-50">
                {searchedOrganizations.map((organization) => (
                  <li
                    key={organization.organizationId}
                    className="p-2 hover:bg-gray-200 cursor-pointer z-50"
                  >
                    <Link
                      to={`../organization/${organization.organizationNameSlug}`}
                      className="block"
                    >
                      {organization.organizationName}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* link to create an organization  */}
        <Link
          to={"/organization/create/"}
          className="bg-white border border-gray-300 text-gray-700 px-1 py-2 mt-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300"
        >
          Create an organization.
        </Link>
      </div>
      {/* Display user organizations. */}
      {userOrganizations.length > 0 ? (
        <ul className="space-y-2">
          {userOrganizations.map((userOrganization) => (
            <li
              key={userOrganization.organizationId}
              className="bg-white p-2 rounded-md shadow"
            >
              <Link
                to={`../organization/${userOrganization.organizationNameSlug}`}
                className="block"
              >
                {userOrganization.organizationName}
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-600">{fallBackText}</p>
      )}
    </div>
  );
};

export default OrganizationComponent;
