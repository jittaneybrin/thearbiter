import { createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    primary: {
      light: "rgb(238, 240, 242, .5)",
      main: "rgb(249, 187, 54)",
      dark: "rgb(254, 145, 62)",
      contrastText: "#fff",
    },
    secondary: {
      light: "rgb(54, 116, 249, .3)",
      main: "rgb(34, 46, 100, .8)",
      dark: "#353b3c",
      contrastText: "#000",
    },
  },
});

export default theme;
