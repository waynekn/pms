import { useState, useRef, useEffect } from "react";
import { Link } from "react-router";
import classNames from "classnames";
import { useSelector } from "react-redux";

import OrganizationComponent from "../components/organization.component";
import UserProjectsDisplay from "../components/user-projects.component";
import { selectCurrentUser } from "../store/user/user.selector";

type Tabs = "organizations" | "projects";

const ProfilePage = () => {
  const [activeTab, setActiveTab] = useState<Tabs>("organizations");
  const [displayDropdown, setDisplayDropDown] = useState(false);

  const dropdownRef = useRef<HTMLDivElement | null>(null);
  const dropdownToggleRef = useRef<HTMLButtonElement | null>(null);

  const currentUser = useSelector(selectCurrentUser);

  document.title = currentUser.username;

  // Close dropdown if clicked outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        dropdownToggleRef.current &&
        !dropdownToggleRef.current.contains(event.target as Node)
      ) {
        setDisplayDropDown(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="h-dvh mx-2 my-2">
      <header className="fixed w-full right-2 space-x-4 text-black font-medium p-4 flex justify-between">
        {/* Dropdown toggle button  */}
        <button
          type="button"
          onClick={() => setDisplayDropDown(!displayDropdown)}
          className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg transition duration-200 ml-auto relative"
          ref={dropdownToggleRef}
        >
          Options
          {/* Dropdown menu  */}
          {displayDropdown && (
            <div
              className="absolute right-0 mt-2 bg-white border rounded-lg shadow-md w-max z-50"
              ref={dropdownRef}
            >
              <ul className="space-y-2 py-2 px-4 text-left">
                <li>
                  <Link
                    to="../templates/create/"
                    className="block text-gray-700 hover:text-blue-500"
                  >
                    Create a template
                  </Link>
                </li>

                <li>
                  <Link
                    to={`../${currentUser.usernameSlug}/settings/`}
                    className="block text-gray-700 hover:text-blue-500"
                  >
                    Settings
                  </Link>
                </li>

                <li>
                  <Link
                    to="../logout"
                    className="block text-gray-700 hover:text-blue-500"
                  >
                    Logout
                  </Link>
                </li>
              </ul>
            </div>
          )}
        </button>
      </header>

      <div className="flex flex-col w-3/4 mx-auto bg-white shadow-lg rounded-lg p-6 relative top-10">
        <nav className="flex w-full border-b-2 border-blue-500 rounded-t-md">
          {/* organizations button  */}
          <button
            className={classNames(
              "flex-1 py-2 text-center hover:bg-blue-200 focus:bg-blue-300 transition-colors border-b-4",
              {
                "border-blue-500": activeTab === "organizations",
                "border-transparent": activeTab !== "organizations",
              }
            )}
            onClick={() => setActiveTab("organizations")}
          >
            Organizations
          </button>
          {/* projects button  */}
          <button
            className={classNames(
              "flex-1 py-2 text-center hover:bg-blue-200 focus:bg-blue-300 transition-colors border-b-4",
              {
                "border-blue-500": activeTab === "projects",
                "border-transparent": activeTab !== "projects",
              }
            )}
            onClick={() => setActiveTab("projects")}
          >
            Projects
          </button>
        </nav>

        <section className="w-full rounded-b-md p-4">
          {activeTab === "organizations" && <OrganizationComponent />}
          {activeTab === "projects" && <UserProjectsDisplay />}
        </section>
      </div>
    </div>
  );
};
export default ProfilePage;
