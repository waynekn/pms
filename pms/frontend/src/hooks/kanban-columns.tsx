import { useState, useEffect } from "react";
import { useParams } from "react-router";

import { ColumnId } from "../pages/project-phase-detail.page";

const useKanbanColumns = () => {
  const { projectPhaseId } = useParams();

  const LOCAL_STORAGE_KEY = projectPhaseId ? `kanban_${projectPhaseId}` : null;

  const [columnsId, setColumnsId] = useState<ColumnId[]>(() => {
    if (!LOCAL_STORAGE_KEY) return ["onHold", "inProgress", "completed"]; // Default order

    const storedColumns = localStorage.getItem(LOCAL_STORAGE_KEY);
    return storedColumns
      ? (JSON.parse(storedColumns) as ColumnId[])
      : ["onHold", "inProgress", "completed"];
  });

  // Save to localStorage whenever columnsId changes & projectPhaseId exists
  useEffect(() => {
    if (LOCAL_STORAGE_KEY) {
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(columnsId));
    }
  }, [columnsId, LOCAL_STORAGE_KEY]);

  return { columnsId, setColumnsId };
};

export default useKanbanColumns;
