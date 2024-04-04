import { Box, Grid } from "@mui/material";
import theme from "./theme";
import { Sidebar } from "./Sidebar";
import { ChatInterface } from "./ChatInterface";
import { useEffect, useState } from "react";
import axios from "axios";
import { Logo } from "./Logo";
import { Message } from "./Message";

export function Background() {
  const [message, setMessage] = useState("");

  const [uploadOpen, setUploadOpen] = useState(false);

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
              <ChatInterface />
            </Box>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
