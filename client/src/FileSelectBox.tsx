import { ToggleButton, ToggleButtonGroup } from "@mui/material";
import React, { useState, useEffect } from "react";
import { PdfUpload } from "./PdfUpload";


interface game {
  name: string;
  index: string;
}

export function FileSelectBox() {
  const [alignment, setAlignment] = React.useState("web");

  const [textValue, setTextValue] = React.useState("");

  const [indexValue, setIndexValue] = React.useState("");

  const [toggleButtons, setToggleButtons] = useState<game[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/getSupportedGames")
      .then(response => response.json())
      .then(json => {
        console.log(json.games);
        setToggleButtons(json.games);
      })
      .catch(error => console.error("Error fetching supported games:", error));
  }, []);

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
    const newToggleButtons = [...toggleButtons, {name: textValue, index: indexValue}];
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
      {toggleButtons.length > 1 && toggleButtons.map((game) => (
        <ToggleButton key={game.index} value={game.name}>
          {game.name ? game.name.charAt(0).toUpperCase() + game.name.slice(1) : ""}
        </ToggleButton>
      ))}
      <ToggleButton value="add-pdf">
        <PdfUpload
          handleOpen={handleOpen}
          handleClose={handleClose}
          setTextValue={setTextValue}
          setIndexValue={setIndexValue}
        />
      </ToggleButton>
    </ToggleButtonGroup>
  );
}
