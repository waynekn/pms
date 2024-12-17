import { useState } from "react";
import LogInForm from "../components/login.component";
import SignUpForm from "../components/signup.component";

export type FormType = "login" | "signup";

const HomePage = () => {
  const [displayLoginForm, setDisplayLoginForm] = useState(false);
  const [displaySignUpForm, setDisplaySignUpForm] = useState(false);

  const handleFormDisplay = (form: FormType) => {
    if (form === "login") {
      setDisplaySignUpForm(false);
      setDisplayLoginForm(true);
    } else {
      setDisplayLoginForm(false);
      setDisplaySignUpForm(true);
    }
  };

  const hideForm = (form: FormType) => {
    if (form === "login") {
      setDisplayLoginForm(false);
    } else {
      setDisplaySignUpForm(false);
    }
  };

  return (
    <div className="h-screen overflow-hidden">
      <nav className="flex justify-end my-3">
        <button
          onClick={() => handleFormDisplay("login")}
          className="py-3 px-6 mx-1  text-lg text-white font-semibold leading-6 bg-blue-500 transition ease-in-out delay-150 hover:bg-blue-600"
        >
          Login
        </button>

        <button
          onClick={() => handleFormDisplay("signup")}
          className="py-3 px-6 mx-1  text-lg text-white font-semibold leading-6 bg-blue-500 transition ease-in-out delay-150 hover:bg-blue-600"
        >
          Sign up
        </button>
      </nav>

      <img
        src="https://media.licdn.com/dms/image/D4D12AQHAzpZZDBIkfA/article-cover_image-shrink_720_1280/0/1710486640359?e=2147483647&v=beta&t=_kP7RyfolRjZCXpwZO3GJqC4Trnozc_G8gP1uCmzilc"
        alt="project management image"
        className="w-lvw h-3/6"
      />

      {displayLoginForm && <LogInForm hideForm={hideForm} />}
      {displaySignUpForm && <SignUpForm hideForm={hideForm} />}
      <article className="mx-2 transform translate-y-1/2 text-4xl font-bold">
        <p>All in one project management software</p>
        <p>Customizable, easy to use project management system.</p>
      </article>
    </div>
  );
};

export default HomePage;
