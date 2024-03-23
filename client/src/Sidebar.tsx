import { Box } from "@mui/material";
import { FileSelectBox } from "./FileSelectBox";

export function Sidebar() {
  return (
    <Box
      sx={{
        height: "100%",
        color: "white",
      }}
      borderRight={1}
      borderRadius="4px"
      borderColor={"gray"}
    >
      <FileSelectBox />
    </Box>
  );
}
