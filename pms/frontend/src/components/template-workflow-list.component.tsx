import DeleteOutlineOutlinedIcon from "@mui/icons-material/DeleteOutlineOutlined";
type TemplateWorkflowListProps = {
  templateWorkflow: string[];
  removeWorkflow: (workflowName: string) => void;
};

const TemplateWorkflowList = ({
  templateWorkflow,
  removeWorkflow,
}: TemplateWorkflowListProps) => {
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
      <p className="block text-gray-700 font-medium text-sm mt-6">
        Template workflow
      </p>

      <ol>
        {templateWorkflow.map((workflow, index) => (
          <li key={index} className="flex list-decimal">
            <p key={index} className="grow">
              {workflow}
            </p>
            <span
              onClick={() => removeWorkflow(workflow)}
              className="cursor-pointer hover:bg-gray-300 p-1 rounded-lg transition-all duration-300 ease-in-out"
            >
              <DeleteOutlineOutlinedIcon />
            </span>
          </li>
        ))}
      </ol>
    </aside>
  );
};
export default TemplateWorkflowList;
