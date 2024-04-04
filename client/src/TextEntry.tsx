import { Box, TextField } from "@mui/material";
import { borderRadius } from "@mui/system";
import React from "react";
import { MessageObject } from "./ChatInterface";

interface TextEntryComponentProps {
  messages: MessageObject[];
  setMessages: React.Dispatch<React.SetStateAction<MessageObject[]>>;
}

export function TextEntry(props: TextEntryComponentProps) {
  const [textFieldValue, setTextFieldValue] = React.useState("");

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      props.setMessages([
        ...props.messages,
        { message: textFieldValue, id: 1 },
      ]);
      setTextFieldValue("");
      console.log(textFieldValue);
    }
  };

  return (
    <Box
      sx={{
        width: "100%",
        height: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#ECECEC",
        borderBottomLeftRadius: "15px",
        borderBottomRightRadius: "15px",
      }}
    >
      <TextField
        sx={{ width: "85%", backgroundColor: "white" }}
        value={textFieldValue}
        onChange={(e) => setTextFieldValue(e.target.value)}
        onKeyDown={handleKeyDown}
        variant="standard"
      />
    </Box>
  );
}
