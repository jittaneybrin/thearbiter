import { Box, Icon, ToggleButton, ToggleButtonGroup } from "@mui/material";
import React from "react";
import theme from "./theme";

export function FileSelectBox() {
  const [alignment, setAlignment] = React.useState("web");

  const handleChange = (
    event: React.MouseEvent<HTMLElement>,
    newAlignment: string
  ) => {
    setAlignment(newAlignment);
  };

  return (
    <ToggleButtonGroup
      color="secondary"
      value={alignment}
      orientation="vertical"
      size="large"
      fullWidth
      exclusive
      onChange={handleChange}
      aria-label="Platform"
    >
      <ToggleButton value="chess">Chess</ToggleButton>
      <ToggleButton value="monopoly">Monopoly</ToggleButton>
      <ToggleButton value="root">Root</ToggleButton>
      <ToggleButton value="add">Add Icon</ToggleButton>
    </ToggleButtonGroup>
  );
}
