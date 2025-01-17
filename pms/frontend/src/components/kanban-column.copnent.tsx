import Stack from "@mui/material/Stack";
import KanbanTask from "./kanban-task.component";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

import { Task } from "../types/tasks";

type KanbanColumnProps = {
  id: string;
  title: string;
  tasks: Task[];
  color: string;
};

const KanbanColumn = ({ id, title, tasks, color }: KanbanColumnProps) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    zIndex: isDragging ? 10 : 1,
    opacity: isDragging ? 0.8 : 1,
    position: "relative" as const,
    boxShadow: isDragging ? "0px 4px 10px rgba(0,0,0,0.2)" : "none",
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="p-2 border rounded-md h-full"
    >
      <h3 className={`${color} px-2 text-lg font-bold rounded-md cursor-grab`}>
        {title}
      </h3>
      {tasks.length > 0 ? (
        <Stack spacing={0.5}>
          {tasks.map((task) => (
            <KanbanTask key={task.taskId} task={task} />
          ))}
        </Stack>
      ) : (
        <p className="text-gray-500">No tasks {title.toLowerCase()}</p>
      )}
    </div>
  );
};
export default KanbanColumn;
