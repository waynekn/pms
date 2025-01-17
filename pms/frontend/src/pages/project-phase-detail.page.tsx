import { useState, useEffect } from "react";
import { useParams } from "react-router";
import Container from "@mui/material/Container";
import { DndContext, DragEndEvent } from "@dnd-kit/core";
import { SortableContext } from "@dnd-kit/sortable";

import TaskCreateForm from "../components/task-creation-form";
import ProjectPhaseDetailPlaceholder from "../placeholders/project-phase-detail.placeholder";

import api from "../api";
import camelize from "../utils/snakecase-to-camelcase";
import handleGenericApiErrors, { ErrorMessageConfig } from "../utils/errors";

import { PhaseDetail, PhaseDetailResponse } from "../types/projects";

import KanbanColumn from "../components/kanban-column.copnent";
import useKanbanColumns from "../hooks/kanban-columns";

export type ColumnId = "onHold" | "inProgress" | "completed";

const ProjectPhaseDetail = () => {
  const initialState: PhaseDetail = {
    project: {
      createdAt: "",
      projectId: "",
      projectName: "",
      projectNameSlug: "",
      deadline: "",
      description: "",
      organization: {
        organizationId: "",
        organizationName: "",
        organizationNameSlug: "",
      },
    },
    phase: { phaseId: "", phaseName: "" },
    role: "Member",
    onHold: [],
    inProgress: [],
    completed: [],
  };
  const [detail, setDetail] = useState(initialState);

  const columnTitles: Record<ColumnId, string> = {
    onHold: "On Hold",
    inProgress: "In Progress",
    completed: "Completed",
  };

  const columnColors: Record<ColumnId, string> = {
    onHold: "bg-bold-yellow",
    inProgress: "bg-red-orange",
    completed: "bg-rich-green",
  };

  const [displayTaskCreateForm, setDisplayTaskCreateForm] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const { projectPhaseId } = useParams();

  const { columnsId, setColumnsId } = useKanbanColumns();

  useEffect(() => {
    const getProjectPhaseDetail = async () => {
      try {
        const res = await api.get<PhaseDetailResponse>(
          `project/phase/${projectPhaseId}/detail/`
        );
        const detail: PhaseDetail = camelize(res.data) as PhaseDetail;
        setDetail(detail);
        setIsLoading(false);
      } catch (error) {
        const messageConfig: ErrorMessageConfig = {
          400: "An unexpected error occurred.",
          404: "Could not find project phase.",
          500: "A server error occurred.",
        };
        setErrorMessage(handleGenericApiErrors(error, messageConfig));
        setIsLoading(false);
      }
    };
    void getProjectPhaseDetail();
  }, [projectPhaseId]);

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over || active.id === over.id) return;

    // Reorder columnsId array based on drag
    const oldIndex = columnsId.indexOf(active.id as ColumnId);
    const newIndex = columnsId.indexOf(over.id as ColumnId);

    const newColumnsOrder = [...columnsId];
    newColumnsOrder.splice(oldIndex, 1);
    newColumnsOrder.splice(newIndex, 0, active.id as ColumnId);

    setColumnsId(newColumnsOrder); // Update state
  };

  if (isLoading) {
    return <ProjectPhaseDetailPlaceholder />;
  }

  if (errorMessage) {
    return (
      <p className="bg-red-600 text-white rounded-lg py-4 px-2 mt-3 md:mx-10">
        {errorMessage}
      </p>
    );
  }

  return (
    <Container className="min-h-screen border-x">
      {/* Nav bar */}
      <nav className="flex border-b py-3 justify-center">
        <span
          className="bg-white border border-gray-300 text-gray-700 px-1 py-2
         rounded-md min-w-40 mx-2"
        >
          {detail.project.projectName}
        </span>

        <span
          className="bg-white border border-gray-300 text-gray-700 px-1 py-2
         rounded-md min-w-40 mx-2"
        >
          {detail.phase.phaseName}
        </span>
        {detail.role === "Manager" && (
          <button
            onClick={() => setDisplayTaskCreateForm(true)}
            className="bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700"
          >
            Create Task
          </button>
        )}
      </nav>
      {/* Kanban board */}
      <main className="grid md:grid-cols-3 gap-y-3 gap-2 mt-1 h-full">
        <DndContext onDragEnd={handleDragEnd}>
          <SortableContext items={columnsId}>
            {columnsId.map((columnId) => (
              <KanbanColumn
                key={columnId}
                id={columnId}
                title={columnTitles[columnId]}
                tasks={detail[columnId]}
                color={columnColors[columnId]}
              />
            ))}
          </SortableContext>
        </DndContext>
      </main>

      {/* Task creation form */}
      {displayTaskCreateForm && (
        <TaskCreateForm
          projectPhase={projectPhaseId as string}
          projectName={detail.project.projectName}
          phaseName={detail.phase.phaseName}
          hideForm={() => setDisplayTaskCreateForm(false)}
        />
      )}
    </Container>
  );
};
export default ProjectPhaseDetail;
