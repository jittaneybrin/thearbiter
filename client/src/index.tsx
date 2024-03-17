import ReactDOM from 'react-dom/client';
import "./index.css";
import { ThemeProvider } from "@mui/material";
import * as React from "react";
import theme from "./theme";
import { Layout } from "./Layout";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <ThemeProvider theme={theme}>
    <Layout />
  </ThemeProvider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
