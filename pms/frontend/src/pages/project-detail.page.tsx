import { useState } from "react";
import { Link, Outlet } from "react-router";
import classNames from "classnames";
import Stack from "@mui/material/Stack";
import ClearIcon from "@mui/icons-material/Clear";

const ProjectDetailPage = () => {
  const [isSidebarVisible, setIsSidebarVisible] = useState(false);

  return (
    <div className="flex h-screen w-screen overflow-hidden">
      {/* Button to open sidebar only on small screens */}
      {!isSidebarVisible && (
        <button
          onClick={() => setIsSidebarVisible(true)}
          className="md:hidden p-2 fixed top-1 left-4 z-50"
        >
          ☰
        </button>
      )}

      {/* Sidebar */}
      <nav
        className={classNames(
          "border-r p-4 fixed top-0 left-0 h-full bg-white sm:w-40 md:block md:w-48 transition-transform duration-300 ease-in-out",
          isSidebarVisible
            ? "transform translate-x-0 z-40 opacity-100"
            : "transform -translate-x-full opacity-0 z-30",
          // Always show the sidebar on md and larger screens
          "md:transform-none md:translate-x-0 md:opacity-100 md:z-40"
        )}
      >
        {/* Button to close sidebar only on small screens */}
        <div className="text-right md:hidden">
          <ClearIcon onClick={() => setIsSidebarVisible(false)} />
        </div>

        <Stack spacing={1}>
          <Link
            to={"dashboard/"}
            className="hover:bg-stone-200 rounded-md p-2 transition-colors duration-300 ease-in-out"
          >
            Dashboard
          </Link>
          <Link
            to={"members/"}
            className="hover:bg-stone-200 rounded-md p-2 transition-colors duration-300 ease-in-out"
          >
            Members
          </Link>
          <Link
            to={"members/add/"}
            className="hover:bg-stone-200 rounded-md p-2 transition-colors duration-300 ease-in-out"
          >
            Add Members
          </Link>
        </Stack>
      </nav>

      <main className="grow p-4 pt-10 md:pt-3 md:ml-48 h-full overflow-y-auto md:overflow-hidden">
        <Outlet />
      </main>
    </div>
  );
};

export default ProjectDetailPage;
