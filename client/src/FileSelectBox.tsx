import {
  SnackbarContent,
  ToggleButton,
  ToggleButtonGroup,
  Popover,
} from "@mui/material";
import React, { useState, useEffect } from "react";
import { PdfUpload } from "./PdfUpload";

export interface game {
  name: string;
  index: string;
}

interface fileSelectBoxComponentProps {
  setSelectedGame: React.Dispatch<React.SetStateAction<game | undefined>>;
}

export function FileSelectBox(props: fileSelectBoxComponentProps) {
  const [alignment, setAlignment] = React.useState("web");
  const [gameNameValue, setGameNameValue] = React.useState("");
  const [file, setFile] = useState<File | null>(null);
  const [toggleButtons, setToggleButtons] = useState<game[]>([]);
  const [snackBarOpen, setSnackBarOpen] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/getSupportedGames")
      .then((response) => response.json())
      .then((json) => {
        console.log(json.games);
        setToggleButtons(json.games);
      })
      .catch((error) =>
        console.error("Error fetching supported games:", error)
      );
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

  const handleSubmit = () => {
    if (gameNameValue == "") {
      setSnackBarOpen(true);
    } else {
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
            const newToggleButtons = [
              ...toggleButtons,
              { name: `${gameNameValue}`, index: `${index}` },
            ];
            setToggleButtons(newToggleButtons);
          })
          .catch((error) => {
            console.error("Error uploading file:", error);
          });
      }
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
      {toggleButtons.length > 1 &&
        toggleButtons.map((game) => (
          <ToggleButton
            key={game.index}
            value={game.name}
            onClick={() => {
              const selectedGame: game = {
                name: game.name,
                index: game.index,
              };
              props.setSelectedGame(selectedGame);
            }}
          >
            {game.name
              ? game.name.charAt(0).toUpperCase() + game.name.slice(1)
              : ""}
          </ToggleButton>
        ))}
      <ToggleButton value="add-pdf">
        <PdfUpload
          handleSubmit={handleSubmit}
          setGameNameValue={setGameNameValue}
          setFile={setFile}
        />
      </ToggleButton>
      <Popover
        open={snackBarOpen}
        onClose={() => {
          setSnackBarOpen(false);
        }}
        anchorReference="anchorPosition"
        anchorPosition={{ top: 0, left: 0 }}
      >
        <SnackbarContent message={"Please provide a Game Name with a PDF"} />
      </Popover>
    </ToggleButtonGroup>
  );
}
