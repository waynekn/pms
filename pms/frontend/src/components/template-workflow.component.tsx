type DisplayTemplateWorkFlowProps = {
  phases: string[];
};

const DisplayTemplateWorkFlow = ({ phases }: DisplayTemplateWorkFlowProps) => {
  return (
    <aside className="border-1 border-black bg-gray-100 p-4 rounded shadow-lg">
      <h1 className="font-bold underline">Added phases:</h1>
      <ol>
        {phases.map((phase, index) => (
          <li key={index}>{phase}</li>
        ))}
      </ol>
    </aside>
  );
};
export default DisplayTemplateWorkFlow;
