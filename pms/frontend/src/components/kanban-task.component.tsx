import { useState, useEffect } from "react";
import { Link } from "react-router";
import { Task } from "../types/tasks";
import classNames from "classnames";
import Tooltip from "@mui/material/Tooltip";
import AccessTimeOutlinedIcon from "@mui/icons-material/AccessTimeOutlined";
import TaskTimeRemaining from "./task-time-remaining.component";
import DoneAllIcon from "@mui/icons-material/DoneAll";

type KanbanTaskProps = {
  task: Task;
};

const KanbanTask = ({ task }: KanbanTaskProps) => {
  const [isOverDue, setIsOverDue] = useState(false);

  useEffect(() => {
    const deadline = new Date(task.deadline);
    setIsOverDue(Date.now() > deadline.getTime());
  }, [task.deadline, task.startDate]);

  return (
    <div className="sm:max-h-24 px-1 md:max-h-48 overflow-y-hidden !mt-1 !mb-5 border-b ">
      <header className="font-bold cursor-move bg-gray-200 rounded-t-md px-1">
        {task.taskName}
      </header>
      <Link
        className=" block text-gray-600 hover:bg-stone-100 transition-colors duration-300 ease-in-out"
        to={`../task/${task.taskId}/detail/`}
      >
        {task.description}
      </Link>
      <div>
        <span>
          {task.status === "DONE" ? (
            <DoneAllIcon sx={{ color: "green" }} fontSize="small" />
          ) : (
            <Tooltip
              placement="top"
              title={
                <TaskTimeRemaining
                  deadline={task.deadline}
                  overdue={isOverDue}
                />
              }
            >
              <AccessTimeOutlinedIcon
                fontSize="small"
                className={classNames(
                  " cursor-pointer",
                  isOverDue ? "text-red-500" : "text-green-500"
                )}
              />
            </Tooltip>
          )}
        </span>
      </div>
    </div>
  );
};

export default KanbanTask;
