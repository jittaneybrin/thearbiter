import { ToggleButton, ToggleButtonGroup } from "@mui/material";
import React, { useState } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { PdfUpload } from "./PdfUpload";

export function FileSelectBox() {
  const [alignment, setAlignment] = React.useState("web");
  const [showUpload, setShowUpload] = useState(false); // State to control rendering of PdfUpload component

  const handleChange = (
    event: React.MouseEvent<HTMLElement>,
    newAlignment: string
  ) => {
    setAlignment(newAlignment);
  };

  const handleAddClick = () => {
    setShowUpload(true);
    console.log("Add button clicked");
  };

  const handlePdfUpload = (file: File | null) => {
    console.log("Uploaded file:", file);
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
      <ToggleButton value="chess">Chess</ToggleButton>
      <ToggleButton value="monopoly">Monopoly</ToggleButton>
      <ToggleButton value="root">Root</ToggleButton>
      <ToggleButton value="add" onClick={handleAddClick}>
        <FontAwesomeIcon icon={faPlus} />
      </ToggleButton>
      {showUpload && <PdfUpload onUpload={handlePdfUpload} />}
    </ToggleButtonGroup>
  );
}
