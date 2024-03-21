import { Box, TextField } from "@mui/material";
import theme from "./theme";
import { useEffect, useState } from "react";
import axios from "axios";

export function TextEntry() {
  const [myQuestion, setQuestion] = useState("");

  function postQuestion(){
    console.log("postquestion");
    // Make a POST request to the Flask backend
    axios
      .post("http://localhost:5000/getAnswer?prompt=" + myQuestion, {
        headers: {
          "Access-Control-Allow-Origin": "*",
        },
        responseType: "json"
      })
      .then((response) => {
        console.log(response);
        setQuestion(response.data.response);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }

  return (
    
    <Box
      sx={{
        width: "80%",
      }}
      display="flex"
      alignItems="center
      "
    >
      <TextField
        fullWidth
        label="Ask Me A Question!"
        variant="outlined"
        color="secondary"
        value = {myQuestion} 
			  onChange={(e) => setQuestion(e.target.value)} 
        onKeyDown={(ev) => {
          console.log(`Pressed keyCode ${ev.key}`);
          if (ev.key === 'Enter') {
            postQuestion();
            ev.preventDefault();
          }
        }}
      ></TextField>
    </Box>
  );
}
