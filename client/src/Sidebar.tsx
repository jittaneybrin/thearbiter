import { Box } from "@mui/material";
import { FileSelectBox, game } from "./FileSelectBox";

interface sidebarComponentProps {
  setSelectedGame: React.Dispatch<React.SetStateAction<game | undefined>>;
}

export function Sidebar(props: sidebarComponentProps) {
  return (
    <Box
      sx={{
        height: "100%",
        color: "white",
        overflowY: "scroll",
        maxHeight: "500px",
      }}
      borderRight={1}
      borderColor={"gray"}
    >
      <FileSelectBox setSelectedGame={props.setSelectedGame} />
    </Box>
  );
}
