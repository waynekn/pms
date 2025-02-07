import BrokenLinkSvg from "../assets/broken-link.svg";
import { Link } from "react-router";

const InvalidUrlPage = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 p-6">
      <div className="flex justify-center mb-6">
        <img
          src={BrokenLinkSvg}
          alt="broken link"
          className="w-48 h-48 object-contain"
        />
      </div>

      <p className="text-xl font-semibold text-gray-800 mb-4">
        Oops! The URL you’ve entered is invalid.
      </p>

      <Link
        to="/"
        className="text-lg font-medium text-blue-500 hover:text-blue-700 underline"
      >
        Go back home
      </Link>
    </div>
  );
};

export default InvalidUrlPage;
