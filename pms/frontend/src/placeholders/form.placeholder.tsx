const FormPlaceHolder = () => {
  return (
    <main className="flex-1 p-4 md:p-8 sm:text-sm md:text-base animate-pulse">
      <form className="w-full max-w-3xl mx-auto border-2 border-gray-300 rounded-lg bg-white shadow-lg p-8 space-y-6">
        <div className="flex flex-col">
          <div className="mb-2 sm:w-full md:w-1/4 h-5 bg-stone-500"></div>
          <div className="h-7 bg-stone-500" />
        </div>

        <div className="flex flex-col">
          <div className="mb-2 sm:w-full md:w-1/4 h-5 bg-stone-500"></div>
          <div className="h-7 bg-stone-500" />
        </div>

        <div className="flex flex-col">
          <div className="mb-2 sm:w-full md:w-1/4 h-5 bg-stone-500"></div>
          <div className="h-7 bg-stone-500" />
        </div>

        <div className="flex justify-end">
          <div className="bg-stone-500 h-7 w-16"></div>
        </div>
      </form>
    </main>
  );
};

export default FormPlaceHolder;
