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

    


    return (
      <div>
        
        <Stack direction="row" spacing={1} paddingLeft={1}>
        <Button startIcon={<RefreshRoundedIcon />} variant="contained" color="warning" onClick={() => window.location.reload(false)}>System Reset</Button>
        <Button startIcon={<BrowserUpdatedRoundedIcon />} variant="contained"  onClick={() => getCoordinates()}>Manual Update</Button>
        <Button startIcon={<RouteRoundedIcon />} variant="contained" onClick={() => onVisiualizePressed()}>Generate Path</Button>
        
        <Button startIcon={<AltRouteRoundedIcon />} variant="contained" color="warning" onClick={() => postCoordinates()}>Execute Path Radar</Button>
        
</Stack>
<br/>
        
      </div>
    );
  }
}
