import { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router";
import Modal from "@mui/material/Modal";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";
import Container from "@mui/material/Container";
import WavingHandOutlinedIcon from "@mui/icons-material/WavingHandOutlined";
import CircularProgress from "@mui/material/CircularProgress";

import ProfilePictureSettings from "../components/settings/profile-pic.component";
import UsernameSettings from "../components/settings/username.component";

import { SnackBarState } from "../types/snackbar";
import { selectCurrentUser } from "../store/user/user.selector";
import { deleteCurrentUser } from "../store/user/user.slice";
import { StoreDispatch } from "../store/store";

const SettingsPage = () => {
  const currentUser = useSelector(selectCurrentUser);
  const [displaySnackbar, setDisplaySnackbar] = useState(false);
  const [displayModal, setDisplayModal] = useState(false);
  const initialSnackBarState: SnackBarState = {
    message: "",
    serverity: "success",
  };
  const [snackBarState, setSnackBarState] =
    useState<SnackBarState>(initialSnackBarState);
  const dispatch = useDispatch<StoreDispatch>();
  const navigate = useNavigate();

  const displaySuccessMessage = (message: string) => {
    setSnackBarState({
      message,
      serverity: "success",
    });
    setDisplaySnackbar(true);
  };
  const displayErrorMessage = (message: string) => {
    setSnackBarState({
      message,
      serverity: "error",
    });
    setDisplaySnackbar(true);
  };

  const handleClose = () => setDisplaySnackbar(false);

  const deleteAccount = async () => {
    try {
      await dispatch(deleteCurrentUser()).unwrap();
      await navigate("/");
    } catch (error) {
      const message: string =
        typeof error === "string" ? error : "An unknown error occurred";
      displayErrorMessage(message);
    }
  };

  return (
    <Container className="border-x min-h-screen">
      <h1 className="font-bold text-lg text-center">Settings</h1>
      <div className="md:px-10 space-y-5">
        {/* Username field */}
        <UsernameSettings
          displayErrorMessage={displayErrorMessage}
          displaySuccessMessage={displaySuccessMessage}
        />
        {/* Email field */}
        <div className="flex items-center">
          <span className="mr-2 w-24">Email:</span>
          <p className="border-b grow ">{currentUser.email}</p>
          <div className="ml-2 w-16"></div>
        </div>

        <ProfilePictureSettings
          displayErrorMessage={displayErrorMessage}
          displaySuccessMessage={displaySuccessMessage}
        />

        <div className="flex justify-end">
          <button
            onClick={() => setDisplayModal(true)}
            className="flex items-center bg-red-600 text-white hover:bg-red-700 focus:outline-none
             focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 py-2 px-4 rounded-lg text-sm
              font-semibold transition duration-300 ease-in-out"
          >
            <span className="mr-2">
              <WavingHandOutlinedIcon />
            </span>
            Delete Account
          </button>
        </div>
      </div>
      <Snackbar
        open={displaySnackbar}
        autoHideDuration={6000}
        onClose={handleClose}
      >
        <Alert
          onClose={handleClose}
          severity={snackBarState.serverity}
          variant="filled"
          sx={{ width: "100%" }}
        >
          {snackBarState.message}
        </Alert>
      </Snackbar>
      <Modal open={displayModal} onClose={() => setDisplayModal(false)}>
        <div className="fixed inset-0 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h1 className="text-xl font-bold">
              Are you sure you want to delete your account?
            </h1>
            <p>
              This action is <span className="font-bold">permanent</span> and
              cannot be reversed
            </p>
            <div className="flex mt-4">
              <button
                onClick={() => setDisplayModal(false)}
                className="mr-4 bg-gray-300 px-4 py-2 rounded"
              >
                Cancel
              </button>
              <button
                onClick={deleteAccount}
                className="bg-red-600 text-white px-4 py-2 rounded"
              >
                Delete My Account
                <span>
                  {currentUser.isLoading && (
                    <CircularProgress size={13} sx={{ color: "white" }} />
                  )}
                </span>
              </button>
            </div>
          </div>
        </div>
      </Modal>
    </Container>
  );
};

export default SettingsPage;
