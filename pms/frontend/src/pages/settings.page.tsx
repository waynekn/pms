import { useState } from "react";
import { useSelector } from "react-redux";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";
import Container from "@mui/material/Container";

import ProfilePictureSettings from "../components/settings/profile-pic.component";
import UsernameSettings from "../components/settings/username.component";

import { SnackBarState } from "../types/snackbar";
import { selectCurrentUser } from "../store/user/user.selector";

const SettingsPage = () => {
  const currentUser = useSelector(selectCurrentUser);
  const [displaySnackbar, setDisplaySnackbar] = useState(false);
  const initialSnackBarState: SnackBarState = {
    message: "",
    serverity: "success",
  };
  const [snackBarState, setSnackBarState] =
    useState<SnackBarState>(initialSnackBarState);

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
    </Container>
  );
};

export default SettingsPage;
