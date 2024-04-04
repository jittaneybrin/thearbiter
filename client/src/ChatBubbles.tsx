import { Box } from "@mui/material";
import { MessageObject } from "./ChatInterface";
import { Message } from "./Message";

interface ChatBubblesComponentProps {
  messages: MessageObject[];
  scrollToBottom: () => void;
}

export function ChatBubbles(props: ChatBubblesComponentProps) {
  return (
    <>
      {props.messages.map((message) => (
        <Box
          sx={{
            display: "flex",
            justifyContent: message.id === 0 ? "start" : "end",
          }}
        >
          <Message message={message} />
        </Box>
      ))}
    </>
  );
}
