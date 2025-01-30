import { Link, Outlet } from "react-router";
import { useSelector } from "react-redux";
import Avatar from "@mui/material/Avatar";
import LandingPageImage from "../assets/landing-page.png";

import { selectCurrentUser } from "../store/user/user.selector";

export type FormType = "login" | "signup";

const HomePage = () => {
  const currentUser = useSelector(selectCurrentUser);
  return (
    <div className="h-screen overflow-hidden">
      <nav className="flex justify-end my-3">
        {currentUser.isLoggedIn ? (
          <Link to={`user/${currentUser.usernameSlug}`} className="mx-1">
            <Avatar src={currentUser.profilePicture} alt="profile-picture" />
          </Link>
        ) : (
          <>
            <Link
              to="login"
              className="py-3 px-6 mx-1 text-lg text-white font-semibold leading-6 bg-blue-500 rounded-md
               transition-all transform duration-300 ease-in-out hover:bg-blue-600 hover:scale-105 hover:shadow-lg"
            >
              Login
            </Link>

            <Link
              to="signup"
              className="py-3 px-6 mx-1 text-lg text-white font-semibold leading-6 bg-blue-500 rounded-md
               transition-all transform duration-300 ease-in-out hover:bg-blue-600 hover:scale-105 hover:shadow-lg"
            >
              Sign up
            </Link>
          </>
        )}
      </nav>

      <img
        src={LandingPageImage}
        alt="project management image"
        className="w-lvw h-3/6"
      />
      <Outlet />

      <article className="mx-2 text-center">
        <p className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-blue-500 animate-fadeIn mb-4">
          All-in-one Project Management Software
        </p>
        <p className="text-xl text-gray-700 animate-slideIn">
          Customizable, easy-to-use project management system.
        </p>
      </article>
    </div>
  );
};

export default HomePage;
