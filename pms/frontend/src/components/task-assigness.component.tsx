import Stack from "@mui/material/Stack";
import { ProjectMember } from "../types/projects";

type TaskAssignessProps = {
  assignees: ProjectMember[];
};

const TaskAssigness = ({ assignees }: TaskAssignessProps) => {
  return (
    <>
      {assignees.length > 0 ? (
        <Stack>
          {assignees.map((user, index) => (
            <p
              key={index}
              className="font-sans font-semibold md:text-lg h-9 border-b"
            >
              {user.username}
            </p>
          ))}
        </Stack>
      ) : (
        <p className="text-gray-500">No users have been assigned this task</p>
      )}
    </>
  );
};
export default TaskAssigness;
