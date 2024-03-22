import { Box, TextField } from "@mui/material";
import Chat from "./TextBubbles";
import theme from "./theme";

export function TextEntry() {
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
