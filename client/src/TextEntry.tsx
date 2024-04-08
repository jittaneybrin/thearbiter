import { Box, TextField } from "@mui/material";
import { borderRadius } from "@mui/system";
import React from "react";
import { MessageObject } from "./ChatInterface";
import axios from "axios";

interface TextEntryComponentProps {
  messages: MessageObject[];
  setMessages: React.Dispatch<React.SetStateAction<MessageObject[]>>;
}




export function TextEntry(props: TextEntryComponentProps) {


  function postQuestion(myQuestion : string){
    console.log("postquestion");
    // Make a POST request to the Flask backend
    axios
      .post("http://127.0.0.1:5000/getAnswer?prompt=" + myQuestion, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET,PUT,POST,DELETE,PATCH,OPTIONS"
        },
        responseType: "json"
      })
      .then(response => {
        console.log(props.messages)

        let newMessage = { message: response.data.response, id: 0 }
        let prevMessages = props.messages;
        props.setMessages(prevMessages => [...prevMessages, newMessage]);

        // props.setMessages(props.messages => [
        //   ...props.messages,
        //   { message: response.data.response, id: 0 },
        // ]);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }

  async function setClientMessage() {
    // client
    let newMessage = { message: textFieldValue, id: 1 }
    let prevMessages = props.messages;
    props.setMessages(prevMessages => [...prevMessages, newMessage])
  }

  const [textFieldValue, setTextFieldValue] = React.useState("");

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {

      setClientMessage().then(() => {
        // Once setMessages is fully executed, call postQuestion
        postQuestion(textFieldValue);
        setTextFieldValue("");
      });
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
