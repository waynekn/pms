import { useState } from "react";
import classNames from "classnames";
import { useSelector, useDispatch } from "react-redux";

import api from "../../api";
import { selectCurrentUser } from "../../store/user/user.selector";
import { setCurrentUser } from "../../store/user/user.slice";

import { StoreDispatch } from "../../store/store";
import handleGenericApiErrors from "../../utils/errors";
import { User, UserResponse } from "../../types/user";
import camelize from "../../utils/snakecase-to-camelcase";

type UsernameSettingsParams = {
  displaySuccessMessage: (message: string) => void;
  displayErrorMessage: (message: string) => void;
};
const UsernameSettings = ({
  displayErrorMessage,
  displaySuccessMessage,
}: UsernameSettingsParams) => {
  const currentUser = useSelector(selectCurrentUser);
  const [username, setUsername] = useState(currentUser.username);
  const dispatch = useDispatch<StoreDispatch>();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
  };

  const updateUsername = async () => {
    try {
      const response = await api.put<UserResponse>("username/update/", {
        username,
      });
      const user = camelize(response.data) as User;
      const newUrl = `/${user.usernameSlug}/settings/`;
      window.history.pushState({}, "", newUrl);
      dispatch(setCurrentUser(response.data));
      displaySuccessMessage("Username successfuly updated");
    } catch (error) {
      const errMsg = handleGenericApiErrors(error);
      displayErrorMessage(errMsg);
    }
  };

  return (
    <div className="flex items-center">
      <span className="mr-2 w-24">Username:</span>
      <input
        type="text"
        name="username"
        value={username}
        className="border-b grow focus:outline-none"
        onChange={handleChange}
      />

      <button
        className={classNames(
          "ml-2 w-16 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-100",
          currentUser.username === username || !username
            ? "cursor-not-allowed"
            : "cursor-pointer"
        )}
        disabled={currentUser.username === username || !username}
        onClick={updateUsername}
      >
        Update
      </button>
    </div>
  );
};

export default UsernameSettings;
