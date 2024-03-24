import { ToggleButton, ToggleButtonGroup } from "@mui/material";
import React, { useState } from "react";
import { PdfUpload } from "./PdfUpload";

export function FileSelectBox() {
  const [alignment, setAlignment] = React.useState("web");

  const [textValue, setTextValue] = React.useState("");

  const [toggleButtons, setToggleButtons] = useState([
    "chess",
    "monopoly",
    "root",
  ]);

  const handleChange = (
    event: React.MouseEvent<HTMLElement>,
    newAlignment: string
  ) => {
    setAlignment(newAlignment);
  };

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

  const [open, setOpen] = React.useState(false);

  const handleOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    const newToggleButtons = [...toggleButtons, `${textValue}`];
    setToggleButtons(newToggleButtons);
    setOpen(false);
  };

  return (
    <ToggleButtonGroup
      color="secondary"
      value={alignment}
      orientation="vertical"
      size="large"
      fullWidth
      exclusive
      onChange={handleChange}
      aria-label="Platform"
    >
      {toggleButtons.map((value, index) => (
        <ToggleButton key={index} value={value}>
          {value.charAt(0).toUpperCase() + value.slice(1)}
        </ToggleButton>
      ))}
      <ToggleButton value="add-pdf">
        <PdfUpload
          handleOpen={handleOpen}
          handleClose={handleClose}
          setTextValue={setTextValue}
        />
      </ToggleButton>
    </ToggleButtonGroup>
  );
}
