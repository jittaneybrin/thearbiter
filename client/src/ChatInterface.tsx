import { Box } from "@mui/material";
import Chat from "./TextBubbles";

export function ChatInterface() {

  return (
    <Box
      sx={{
        width: "80%",
      }}
      display="flex"
      alignItems="center
      "
    >
      <Chat />
    </Box>
  );
}
