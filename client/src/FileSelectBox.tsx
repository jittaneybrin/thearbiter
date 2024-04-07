import { ToggleButton, ToggleButtonGroup } from "@mui/material";
import React, { useState } from "react";
import { PdfUpload } from "./PdfUpload";

export function FileSelectBox() {
  const [alignment, setAlignment] = React.useState("web");
  const [gameNameValue, setGameNameValue] = React.useState("");
  const [file, setFile] = useState<File | null>(null);

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

  const handleSubmit = () => {
    const newToggleButtons = [...toggleButtons, `${gameNameValue}`];
    setToggleButtons(newToggleButtons);

    //send file here
    if (file) {
      const formData = new FormData();
      formData.append("the_file", file);
      fetch("http://127.0.0.1:5000/uploadPDF", {
        method: "POST",
        body: formData,
      })
        .then((res) => res.json())
        .then((json) => {
          let index = json.index;
          // I don't know what's happening with textFieldValue, but it seems to be blank here.
          // console.log(`Created game ${textFieldValue} with index ${index}`);
          console.log(`Created index ${index}`);
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
        });
    }
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
          handleSubmit={handleSubmit}
          setGameNameValue={setGameNameValue}
          setFile={setFile}
        />
      </ToggleButton>
    </ToggleButtonGroup>
  );
}
