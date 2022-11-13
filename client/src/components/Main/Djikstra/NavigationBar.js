import { Button, Stack } from "@mui/material";
import React, { Component } from "react";
import RefreshRoundedIcon from '@mui/icons-material/RefreshRounded';
import RouteRoundedIcon from '@mui/icons-material/RouteRounded';
import AltRouteRoundedIcon from '@mui/icons-material/AltRouteRounded';
export default class NavigationBar extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  hideFixedMenu = () => this.setState({ fixed: false });
  showFixedMenu = () => this.setState({ fixed: true });

  render() {
    const { onVisiualizePressed } = this.props;
    return (
      <div>
        <Stack direction="row" spacing={2} paddingLeft={2}>
        <Button startIcon={<RefreshRoundedIcon />} variant="contained" onClick={() => window.location.reload(false)}>Refresh Field</Button>
        <Button startIcon={<RouteRoundedIcon />} variant="contained" onClick={() => onVisiualizePressed()}>Generate Path</Button>
        <Button startIcon={<AltRouteRoundedIcon />} variant="contained" >Execute Path</Button>

        </Stack>
      </div>
    );
  }
}
