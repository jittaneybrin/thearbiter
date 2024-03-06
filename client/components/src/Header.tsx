import { Box } from "@mui/material";
import theme from "./theme";

export function Header() {
  return (
    <Box
      sx={{
        height: "10vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        fontWeight: "bold",
        fontSize: "25px",
        zIndex: "1",
        background: theme.palette.primary.light,
      }}
    >
      The Arbiter
    </Box>
  );
}
