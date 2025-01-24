import { useState } from "react";
import classNames from "classnames";
import Avatar from "@mui/material/Avatar";
import { useDispatch, useSelector } from "react-redux";

import api from "../../api";
import { setCurrentUser } from "../../store/user/user.slice";
import { selectCurrentUser } from "../../store/user/user.selector";
import handleGenericApiErrors, { ErrorMessageConfig } from "../../utils/errors";

import { UserResponse } from "../../types/user";
import { StoreDispatch } from "../../store/store";

type ProfilePictureSettingsParams = {
  displaySuccessMessage: (message: string) => void;
  displayErrorMessage: (message: string) => void;
};

const ProfilePictureSettings = ({
  displayErrorMessage,
  displaySuccessMessage,
}: ProfilePictureSettingsParams) => {
  const [avatar, setAvatar] = useState<File | null>(null);
  const dispatch = useDispatch<StoreDispatch>();
  const currentUser = useSelector(selectCurrentUser);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setAvatar(e.target.files[0]); // Store the File object
    }
  };

  const ProfilePicture = async () => {
    if (!avatar) {
      return;
    }

    const formData = new FormData();
    formData.append("avatar", avatar);

    try {
      const response = await api.put<UserResponse>("avatar/update/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      dispatch(setCurrentUser(response.data));
      displaySuccessMessage("Profile successfully updated");
    } catch (error) {
      const messageConfig: ErrorMessageConfig = {
        500: "An error occurred while updating your profile",
      };
      const errorMsg = handleGenericApiErrors(error, messageConfig);
      displayErrorMessage(errorMsg);
    }
  };
  return (
    <div className="flex">
      <p>Profile picture :</p>
      <div className="ml-4 flex">
        <input
          type="file"
          name="avatar"
          id="avatar"
          onChange={handleFileChange}
          accept=".png,.jpeg,.jpg"
          className="hidden"
        />
        <label htmlFor="avatar" className="cursor-pointer">
          <Avatar
            alt="profile-picture"
            src={currentUser.profilePicture}
            sx={{ width: 96, height: 96 }}
          />
        </label>

        <button
          onClick={ProfilePicture}
          disabled={avatar === null}
          className={classNames(
            "bg-white border border-gray-300 text-gray-700 px-1 py-2 ml-2 h-10  mt-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300",
            avatar === null ? "cursor-not-allowed" : "cursor-pointer"
          )}
        >
          Update
        </button>
      </div>
    </div>
  );
};

export default ProfilePictureSettings;
