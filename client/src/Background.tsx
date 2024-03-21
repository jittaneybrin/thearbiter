import { Box, Grid } from "@mui/material";
import theme from "./theme";
import { Sidebar } from "./Sidebar";
import { TextEntry } from "./TextEntry";
import { useEffect, useState } from "react";
import axios from "axios";

export function Background() {
  const [message, setMessage] = useState("");

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
          {message}
          <Box
            sx={{
              backgroundColor: theme.palette.secondary.light,
              height: "93%",
              width: "85%",
              borderRadius: "20px",
            }}
            marginTop="2.5%"
            marginLeft="7.5%"
            display="flex"
            alignItems="end"
            justifyContent="center"
          >
            <Box
              width="70%"
              justifyContent="center"
              display="flex"
              paddingBottom="2%"
            >
              <TextEntry />
            </Box>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
