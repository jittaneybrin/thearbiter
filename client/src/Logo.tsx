import { Box, Typography } from "@mui/material";

export function Logo() {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}
    >
      <Box sx={{ display: "flex", justifyContent: "center" }}>
        <img src="Logo.png" width="60px" height="60px" />
      </Box>
      <Box>
        <Typography variant="h4"> Ask me about a game! </Typography>
      </Box>
    </Box>
  );
}
