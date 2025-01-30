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
              className="py-3 px-6 mx-1  text-lg text-white font-semibold leading-6 bg-blue-500 transition ease-in-out delay-150 hover:bg-blue-600"
            >
              Login
            </Link>

            <Link
              to="signup"
              className="py-3 px-6 mx-1  text-lg text-white font-semibold leading-6 bg-blue-500 transition ease-in-out delay-150 hover:bg-blue-600"
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

      <article className="mx-2 text-4xl font-bold">
        <p>All in one project management software</p>
        <p>Customizable, easy to use project management system.</p>
      </article>
    </div>
  );
};

export default HomePage;
