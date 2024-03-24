import {
  Box,
  Button,
  Modal,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import React from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { text } from "@fortawesome/fontawesome-svg-core";

const modalStyle = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

interface PdfUploadComponentProps {
  handleOpen: () => void;
  handleClose: () => void;
  setTextValue: React.Dispatch<React.SetStateAction<string>>;
}

export function PdfUpload(props: PdfUploadComponentProps) {
  const [open, setOpen] = React.useState(false);
  const [textFieldValue, setTextFieldValue] = React.useState("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files ? event.target.files[0] : null;
    if (file) {
      console.log(file);
      const formData = new FormData();
      formData.append("the_file", file);

      fetch("http://127.0.0.1:5000/uploadPDF", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (response.ok) {
            console.log("File uploaded successfully");
          } else {
            console.error("Failed to upload file");
          }
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
        });
    }
  };

  const handleOpen = () => {
    setOpen(true);
    props.handleOpen();
  };

  const handleTextFieldChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setTextFieldValue(event.target.value);
    props.setTextValue(event.target.value);
  };

  return (
    <div>
      <button onClick={handleOpen}>
        <FontAwesomeIcon icon={faPlus} />
      </button>
      <Modal open={open} onClose={props.handleClose}>
        <Box sx={modalStyle}>
          <Typography variant="h6" component="h2">
            Upload a file to add a new game.
          </Typography>
          <Box marginTop="20px">
            <input type="file" accept=".pdf" onChange={handleFileChange} />
          </Box>
          <Box marginTop="10px">
            <TextField
              variant="standard"
              value={textFieldValue}
              onChange={handleTextFieldChange}
              label="Game Name"
            />
          </Box>
          <Box
            sx={{
              display: "flex",
              justifyContent: "end",
            }}
          >
            <button onClick={props.handleClose}>Submit</button>
          </Box>
        </Box>
      </Modal>
    </div>
  );
}
