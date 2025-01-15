import { useState } from "react";
import { debounce } from "lodash";
import Chip from "@mui/material/Chip";
import camelize from "../utils/snakecase-to-camelcase";
import { Industry, IndustryResponse } from "../pages/template-creation.page";
import api from "../api";

type ProjectCreateSideBarProps = {
  handleTemplateSelection: (templateId: string, templateName: string) => void;
};

type TemplateSearchResponse = {
  template_id: string;
  template_name: string;
  industry: IndustryResponse;
};

type ProjectTemplate = {
  templateId: string;
  templateName: string;
  industry: Industry;
};

const ProjectCreateSideBar = ({
  handleTemplateSelection,
}: ProjectCreateSideBarProps) => {
  const [projectTemplates, setProjectTemplates] = useState<ProjectTemplate[]>(
    []
  );

  const handleTemplateSearch = debounce(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      const { value } = e.target;
      try {
        const res = await api.get<TemplateSearchResponse[]>(
          `template/search/?name=${value}`
        );
        const projectTemplates = res.data.map((templateSearchResponse) =>
          camelize(templateSearchResponse)
        ) as ProjectTemplate[];
        setProjectTemplates(projectTemplates);
      } catch {
        setProjectTemplates([]);
      }
    },
    300
  );

  return (
    <aside
      className="md:w-1/4 w-full bg-white border-r-2 border-gray-300 shadow-lg p-4 md:static fixed inset-y-0 left-0 z-10 transform -translate-x-full md:translate-x-0 transition-transform duration-300"
      id="sidebar"
    >
      <div className="relative">
        {/* Close Button (visible only on small screens) */}
        <button
          className="absolute top-2 right-2 p-2 bg-gray-200 rounded-md hover:bg-gray-300 focus:outline-none md:hidden"
          onClick={() => {
            document
              .getElementById("sidebar")!
              .classList.toggle("translate-x-0");
          }}
        >
          ✖ Close
        </button>
      </div>

      {/* Template Search */}
      <label
        htmlFor="template-search"
        className="block text-gray-700 font-medium text-sm mt-6"
      >
        Pick a template for your project (Optional)
      </label>
      <input
        type="search"
        name="template-search"
        id="template-search"
        className="w-full px-4 py-2 mt-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        placeholder="Search for a template"
        onChange={handleTemplateSearch}
      />
      {projectTemplates.length > 0 && (
        <ul className="mt-4 space-y-2">
          {projectTemplates.map((projectTemplate) => (
            <li
              key={projectTemplate.templateId}
              className="flex justify-between items-center bg-gray-50 p-2 border border-gray-300 rounded-md cursor-pointer hover:bg-gray-100"
              onClick={() =>
                handleTemplateSelection(
                  projectTemplate.templateId,
                  projectTemplate.templateName
                )
              }
            >
              <span className="text-gray-700">
                {projectTemplate.templateName}
              </span>
              <Chip
                label={projectTemplate.industry.industryName}
                color="success"
              />
            </li>
          ))}
        </ul>
      )}
    </aside>
  );
};
export default ProjectCreateSideBar;
