import { Box } from "@mui/system";
import { MessageObject } from "./ChatInterface";

interface MessageComponentProps {
  message: MessageObject;
}

export function Message(props: MessageComponentProps) {
  return (
    <Box
      sx={{
        borderRadius: "20px",
        maxWidth: "40%",
        backgroundColor: props.message.id == 0 ? "#F9AF36" : "#FE913F",
        border:
          props.message.id == 0 ? "2px solid #FE913F" : "2px solid #F9AF36",
        display: "inline-flex",
        padding: "10px",
        marginTop: "10px",
        color: "white",
        marginLeft: "5px",
        marginRight: "5px",
      }}
    >
      {props.message.message}
    </Box>
  );
}
