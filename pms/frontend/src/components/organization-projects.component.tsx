import { Link } from "react-router";
import { Project } from "../types/projects";

type OrganizationProjectsProps = {
  projects: Project[];
};

const OrganizationProjects = ({ projects }: OrganizationProjectsProps) => {
  return (
    <ul className="space-y-2">
      {projects.map((project) => (
        <li key={project.projectId} className="border-b mt-1 block">
          <Link
            to={`../p/${project.projectId}/${project.projectNameSlug}/`}
            className="block"
          >
            {project.projectName}
          </Link>
        </li>
      ))}
    </ul>
  );
};

export default OrganizationProjects;
