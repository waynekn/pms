import Container from "@mui/material/Container";

const ProjectPhaseDetailPlaceholder = () => {
  return (
    <Container className="min-h-screen border-x animate-pulse">
      <nav className="flex border-b py-3 justify-center">
        <span
          className="border border-gray-300 px-1 py-2
             rounded-md min-w-40 mx-2 h-10 bg-stone-300"
        ></span>

        <span
          className="border border-gray-300 px-1 py-2
             rounded-md min-w-40 mx-2 h-10 bg-stone-300"
        ></span>

        <span className="bg-stone-300 h-10 p-2 rounded-md w-48"></span>
      </nav>

      <main className="grid md:grid-cols-3 gap-y-3 gap-2 mt-1">
        <div className="sm:mb-10 md:mb-0">
          <h3 className="bg-stone-300 h-8 rounded-md"></h3>
        </div>
        <div className="sm:mb-10 md:mb-0">
          <h3 className="bg-stone-300 h-8 rounded-md"></h3>
        </div>
        <div className="sm:mb-10 md:mb-0">
          <h3 className="bg-stone-300 h-8 rounded-md"></h3>
        </div>
      </main>
    </Container>
  );
};
export default ProjectPhaseDetailPlaceholder;
