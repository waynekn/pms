type TaskTimeRemainingProps = {
  deadline: string;
  overdue: boolean;
};

const TaskTimeRemaining = ({ deadline, overdue }: TaskTimeRemainingProps) => {
  if (overdue) {
    return <p>Time is overdue</p>;
  }

  const deadlineDate = new Date(deadline);
  const now = new Date();

  let years = deadlineDate.getFullYear() - now.getFullYear();
  let months = deadlineDate.getMonth() - now.getMonth();
  let days = deadlineDate.getDate() - now.getDate();

  if (days < 0) {
    const lastMonth = new Date(now.getFullYear(), now.getMonth(), 0);
    days += lastMonth.getDate();
    months -= 1;
  }

  if (months < 0) {
    months += 12;
    years -= 1;
  }

  const showYears = years > 0 ? `${years} year${years > 1 ? "s" : ""}` : null;
  const showMonths =
    months > 0 ? `${months} month${months > 1 ? "s" : ""}` : null;
  const showDays = days > 0 ? `${days} day${days > 1 ? "s" : ""}` : null;

  const remainingTime = [showYears, showMonths, showDays]
    .filter(Boolean)
    .join(" ");

  return <p>{remainingTime} remaining</p>;
};
export default TaskTimeRemaining;
