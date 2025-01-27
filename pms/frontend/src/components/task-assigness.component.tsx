import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
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
            <li
              key={index}
              className="font-sans font-semibold md:text-lg h-9 border-b flex items-center"
            >
              <Avatar
                src={user.profilePicture}
                alt="profile-picture"
                sx={{ width: 24, height: 24, marginRight: 1 }}
              />
              {user.username}
            </li>
          ))}
        </Stack>
      ) : (
        <p className="text-gray-500">No users have been assigned this task</p>
      )}
    </>
  );
};
export default TaskAssigness;
