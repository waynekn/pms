import { useState } from "react";
import Modal from "@mui/material/Modal";
import classNames from "classnames";
import { ProjectPhase } from "../types/projects";

import api from "../api";
import CircularProgress from "@mui/material/CircularProgress";
import handleGenericApiErrors from "../utils/errors";

type PhaseDeletionProps = {
  projectPhase: ProjectPhase;
  hideModal: () => void;
};

const PhaseDeletionConfirmationModal = ({
  projectPhase,
  hideModal,
}: PhaseDeletionProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [errMsg, setErrMsg] = useState("");

  const deleteProjectPhase = async () => {
    try {
      setIsLoading(true);
      setErrMsg("");
      await api.delete(`project/phase/${projectPhase.phaseId}/delete/`);
      location.reload();
    } catch (error) {
      setIsLoading(false);
      setErrMsg(handleGenericApiErrors(error));
    }
  };

  return (
    <Modal open={true} onClose={() => hideModal()}>
      <div className="fixed inset-0 flex justify-center items-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h1 className="text-lg font-bold">
            Are you sure you want to delete {projectPhase.phaseName} phase of
            your project?
          </h1>
          <p>
            All tasks associated with the
            <span className="font-bold mx-1">{projectPhase.phaseName}</span>
            phase of your project will also be deleted
          </p>

          {/** Display error messages */}
          <p className="text-red-600 text-sm">{errMsg}</p>

          <div className="flex mt-4">
            <button
              onClick={() => hideModal()}
              className="mr-4 bg-gray-300 px-4 py-2 rounded"
            >
              Cancel
            </button>
            <button
              onClick={deleteProjectPhase}
              className="bg-red-600 text-white px-4 py-2 rounded"
            >
              Delete
              <span
                className={classNames(
                  "ml-2",
                  isLoading ? "inline" : "invisible"
                )}
              >
                <CircularProgress size={13} sx={{ color: "white" }} />
              </span>
            </button>
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default PhaseDeletionConfirmationModal;
