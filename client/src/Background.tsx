import { Box, Grid, Typography } from "@mui/material";
import theme from "./theme";
import { Sidebar } from "./Sidebar";
import { TextEntry } from "./TextEntry";
import { useEffect, useState } from "react";
import axios from "axios";
import { Logo } from "./Logo";

export function Background() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Make a GET request to the Flask backend
    axios
      .post("http://127.0.0.1:5000/gptapi", {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET,PUT,POST,DELETE,PATCH,OPTIONS",
        },
        responseType: "json",
      })
      .then((response) => {
        console.log(response);
        setMessage(response.data.response);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <Grid container spacing={0}>
      <Grid xs={1.5}>
        <Sidebar />
      </Grid>
      <Grid xs={10.5}>
        <Box
          sx={{
            height: "100vh",
          }}
        >
          <Box
            sx={{
              backgroundColor: theme.palette.secondary.light,
              height: "93%",
              width: "93%",
              borderRadius: "20px",
              marginTop: "3.5%",
              marginLeft: "3.5%",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <Box
              sx={{
                height: "10%",
                padding: "10px",
                fontWeight: "500",
              }}
            >
              The Arbiter
            </Box>

            <Box
              sx={{
                height: "20%",
                paddingTop: "2%",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <Logo />
            </Box>
            <Box
              sx={{
                height: "80%",
                display: "flex",
                justifyContent: "center",
                alignItems: "end",
                paddingBottom: "2%",
              }}
            >
              <TextEntry />
            </Box>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
