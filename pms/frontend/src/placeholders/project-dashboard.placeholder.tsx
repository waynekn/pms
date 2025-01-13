const ProjectDashBoardPlaceHolder = () => {
  return (
    <div className="h-full w-full flex flex-col animate-pulse ">
      <article className="w-full h-1/3 md:w-3/5 border-stone-700 bg-stone-300 rounded-t-lg flex flex-col">
        <h2 className="ml-2 flex-none h-7 w-15"></h2>
        <div className="flex-1 min-h-0">
          <p className="bg-stone-100 p-2 h-full overflow-y-auto sm:text-2xl md:text-base  w-15"></p>
        </div>
      </article>

      <section className="h-2/3 mt-5 border-2 rounded-lg ">
        <div className="flex flex-col gap-5 md:flex-row md:gap-8 p-1 h-full">
          {/* Bar Chart */}
          <div className="w-full md:w-1/2 bg-stone-200 p-4 rounded-lg flex flex-col">
            <div className="rounded-md h-[300px] w-full sm:h-[400px] md:h-5/6" />
          </div>

          <div className="flex flex-col gap-5 md:flex-row md:w-1/2">
            {/* Number of Project Members */}
            <div className="w-full md:w-1/2 p-6 bg-stone-300 border-2  rounded-lg shadow-lg flex flex-col items-center" />

            {/* Percentage of Tasks Completed */}
            <div className="w-full md:w-1/2 p-6 bg-stone-300 rounded-lg shadow-lg" />
          </div>
        </div>
      </section>
    </div>
  );
};

export default ProjectDashBoardPlaceHolder;
