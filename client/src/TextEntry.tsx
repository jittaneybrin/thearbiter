import { Box, TextField } from "@mui/material";
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
      <TextField
        fullWidth
        label="Ask Me A Question!"
        variant="outlined"
        color="secondary"
      ></TextField>
    </Box>
  );
}
