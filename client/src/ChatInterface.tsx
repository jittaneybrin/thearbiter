import { Box, TextField } from "@mui/material";
import React, { useRef, useEffect } from "react";
import { ChatBubbles } from "./ChatBubbles";
import { TextEntry } from "./TextEntry";

export interface MessageObject {
  message: string;
  id: number;
}

export function ChatInterface() {
  const [messages, setMessages] = React.useState<MessageObject[]>([
    { message: "Hello! I am The Arbiter. How may I help you?", id: 0 },
  ]);

  const boxRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (boxRef.current) {
      boxRef.current.scrollTop = boxRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <Box
      sx={{
        height: "90%",
        width: "80%",
        backgroundColor: "white",
        display: "flex",
        borderRadius: "20px",
        flexDirection: "column",
      }}
    >
      <Box
        sx={{ maxHeight: "500px", height: "85%", overflowY: "scroll" }}
        ref={boxRef}
      >
        <ChatBubbles messages={messages} scrollToBottom={scrollToBottom} />
      </Box>
      <Box sx={{ height: "17%" }}>
        <TextEntry messages={messages} setMessages={setMessages} />
      </Box>
    </Box>
  );
}
