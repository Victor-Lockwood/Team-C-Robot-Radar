import { Button, Stack } from "@mui/material";
import React, { Component } from "react";
import RefreshRoundedIcon from '@mui/icons-material/RefreshRounded';
import RouteRoundedIcon from '@mui/icons-material/RouteRounded';
import AltRouteRoundedIcon from '@mui/icons-material/AltRouteRounded';
import PlayArrowRoundedIcon from '@mui/icons-material/PlayArrowRounded';
import StopRoundedIcon from '@mui/icons-material/StopRounded';
import BrowserUpdatedRoundedIcon from '@mui/icons-material/BrowserUpdatedRounded';

export default class NavigationBar extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  hideFixedMenu = () => this.setState({ fixed: false });
  showFixedMenu = () => this.setState({ fixed: true });

  render() {
    const { onVisiualizePressed } = this.props;
    const { getCoordinates } = this.props;
    const { postCoordinates } = this.props;
    const { timeCoordinates } = this.props;
    


    return (
      <div>
        
        <Stack direction="row" spacing={1} paddingLeft={1}>
        <Button startIcon={<RefreshRoundedIcon />} variant="contained" color="warning" onClick={() => window.location.reload(false)}>System Reset</Button>
        <Button startIcon={<RouteRoundedIcon />} variant="contained" onClick={() => onVisiualizePressed()}>Generate Path</Button>
        <Button startIcon={<BrowserUpdatedRoundedIcon />} variant="contained" color="warning" onClick={() => getCoordinates()}>Manual Update</Button>
        
</Stack>
<br/>
        
        <Stack direction="row" spacing={1} paddingLeft={1}>
        <Button startIcon={<AltRouteRoundedIcon />} variant="contained" onClick={() => postCoordinates()}>Execute Path Radar</Button>
        <Button startIcon={<PlayArrowRoundedIcon />} variant="contained" color="success" onClick={() => timeCoordinates()}>Initialize Radar</Button>
        <Button startIcon={<StopRoundedIcon />} variant="contained"color="error" onClick={() => getCoordinates()}>Halt Read</Button>


        </Stack>
      </div>
    );
  }
}
