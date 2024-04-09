import { Box, Grid } from "@mui/material";
import theme from "./theme";
import { Sidebar } from "./Sidebar";
import { ChatInterface } from "./ChatInterface";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { Logo } from "./Logo";
import { Message } from "./Message";
import { game } from "./FileSelectBox";

export function Background() {
  
  const [selectedGame, setSelectedGame] = React.useState<game>();

  return (
    <Grid container spacing={0}>
      <Grid xs={1.5}>
        <Sidebar setSelectedGame={setSelectedGame}/>
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
              height: "100%",
              width: "100%",
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
              <ChatInterface selectedGame={selectedGame}/>
            </Box>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
