import { useState, useEffect } from "react";
import { useParams } from "react-router";
import { BarChart } from "@mui/x-charts/BarChart";
import ProjectDashBoardPlaceHolder from "../placeholders/project-dashboard.placeholder";

import handleGenericApiErrors from "../utils/errors";
import camelize from "../utils/snakecase-to-camelcase";
import api from "../api";

import { ProjectStats, ProjectStatsResponse } from "../types/projects";

const ProjectDashBoard = () => {
  const initialState: ProjectStats = {
    tasks: 0,
    members: 0,
    description: "",
    tasksOnHold: 0,
    tasksInProgress: 0,
    tasksCompleted: 0,
    percentageCompletion: 0,
  };
  const [projectStats, setProjectStats] = useState<ProjectStats>(initialState);

  const [isLoading, setIslLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  const barColors = ["#FF5733", "#FFC300", "#28A745"];

  const { projectId } = useParams();

  useEffect(() => {
    const getProjectStats = async () => {
      try {
        const res = await api.get<ProjectStatsResponse>(
          `project/stats/?pk=${projectId}`
        );
        const stats = camelize(res.data) as ProjectStats;
        document.title = "Project detail";
        setProjectStats(stats);
        setIslLoading(false);
      } catch (error) {
        // TODO
        setErrorMessage(handleGenericApiErrors(error));
        setIslLoading(false);
      }
    };
    void getProjectStats();
  }, [projectId]);

  if (isLoading) {
    return <ProjectDashBoardPlaceHolder />;
  }

  if (errorMessage) {
    return (
      <p className="bg-red-600 text-white rounded-lg py-4 px-2 mt-3 md:mx-10">
        {errorMessage}
      </p>
    );
  }

  return (
    <div className="h-full w-full flex flex-col ">
      <article className="w-full h-1/3 md:w-3/5 border-stone-700 bg-stone-300 rounded-t-lg flex flex-col">
        <h2 className="ml-2 flex-none">Project Description</h2>
        <div className="flex-1 min-h-0">
          <p className="bg-stone-100 p-2 h-full overflow-y-auto sm:text-2xl md:text-base">
            {projectStats.description || "This project has no description"}
          </p>
        </div>
      </article>

      <section className="h-2/3 mt-5 border-2 rounded-lg ">
        <div className="flex flex-col gap-5 md:flex-row md:gap-8 p-1 h-full">
          {/* Bar Chart */}
          <div className="w-full md:w-1/2 bg-stone-200 p-4 rounded-lg flex flex-col">
            <h3 className="text-lg font-semibold mb-2">Bar Chart</h3>
            <div className="rounded-md h-[300px] w-full sm:h-[400px] md:h-5/6">
              <BarChart
                xAxis={[
                  {
                    id: "barCategories",
                    data: ["In progress", "On hold", "Completed"],
                    scaleType: "band",
                    label: "Task status",
                    colorMap: {
                      type: "ordinal",
                      colors: barColors,
                    },
                  },
                ]}
                yAxis={[
                  {
                    label: "Number of tasks",
                  },
                ]}
                series={[
                  {
                    data: [
                      projectStats.tasksInProgress,
                      projectStats.tasksOnHold,
                      projectStats.tasksCompleted,
                    ],
                  },
                ]}
              />
            </div>
          </div>

          <div className="flex flex-col gap-5 md:flex-row md:w-1/2">
            {/* Number of Project Members */}
            <div className="w-full md:w-1/2 p-6 bg-gradient-to-r from-blue-500 to-blue-600 text-white border-2 border-blue-700 rounded-lg shadow-lg flex flex-col items-center">
              <p className="text-5xl font-extrabold text-yellow-400 mb-2">
                {projectStats.members}
              </p>
              <h3 className="text-xl font-semibold text-white">
                Project Member(s)
              </h3>
            </div>

            {/* Percentage of Tasks Completed */}
            <div className="w-full md:w-1/2 p-6 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-lg shadow-lg">
              <h3 className="text-xl font-semibold mb-3 text-gray-200">
                Completion percentage
              </h3>

              <div className="relative">
                <p className="text-4xl font-extrabold text-yellow-400 ml-2 text-shadow-md">
                  {Math.round(projectStats.percentageCompletion)} %
                </p>

                {/* Progress Bar */}
                <div className="w-full h-2 bg-gray-200 rounded-full mt-4">
                  <div
                    className="h-2 rounded-full bg-yellow-400"
                    style={{ width: `${projectStats.percentageCompletion}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ProjectDashBoard;
