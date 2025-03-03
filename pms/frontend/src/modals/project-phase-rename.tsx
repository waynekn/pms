import { useState } from "react";
import classNames from "classnames";

import Modal from "@mui/material/Modal";
import Input from "@mui/material/Input";
import CircularProgress from "@mui/material/CircularProgress";

import { ProjectPhase } from "../types/projects";

import api from "../api";
import handleGenericApiErrors from "../utils/errors";

type PhaseDeletionProps = {
  projectPhase: ProjectPhase;
  hideModal: () => void;
};

const PhaseRenameModal = ({ projectPhase, hideModal }: PhaseDeletionProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [errMsg, setErrMsg] = useState("");
  const [newName, setNewName] = useState("");

  const deleteProjectPhase = async () => {
    try {
      setIsLoading(true);
      setErrMsg("");
      await api.put(`project/phase/${projectPhase.phaseId}/rename/`, {
        name: newName.trim(),
      });
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
          <h1 className="text-lg">
            Are you sure you want to rename{" "}
            <span className="font-bold">{projectPhase.phaseName}</span> phase of
            your project?
          </h1>
          <Input
            type="text"
            value={newName}
            placeholder="Enter the new name"
            onChange={(e) => setNewName(e.target.value)}
          />

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
              className="bg-blue-600 text-white px-4 py-2 rounded"
            >
              Rename
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

export default PhaseRenameModal;
