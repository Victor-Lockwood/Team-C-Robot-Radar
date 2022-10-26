import * as React from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import { AppBar, Avatar, Button, CardHeader, Stack, Toolbar, Typography } from '@mui/material';
import CameraswitchRoundedIcon from '@mui/icons-material/CameraswitchRounded';
import ControlGrid from '../components/controlGrid';
import TerminalRoundedIcon from '@mui/icons-material/TerminalRounded';
import Main from '../components/Main/Main';
import { blue, green, pink, purple } from '@mui/material/colors';
import RadarRoundedIcon from '@mui/icons-material/RadarRounded';
import VrpanoRoundedIcon from '@mui/icons-material/VrpanoRounded';

export default function Home() {
  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log({
      email: data.get('email'),
      password: data.get('password'),
    });
  };
  return (
    <Box sx={{ flexGrow: 1 }}>
        <br/>
      <Grid container spacing={3} padding={2}>
        <Grid item xs={3}>
        <Paper elevation={3}>
            <br/>
            <h2>
            Hello, Adam!
            </h2>
    
         <br/>
         <br/>
         </Paper>
         <br/>

             <ControlGrid/>

       
        </Grid>
        <Grid item xs={6}>
            <Paper elevation={3}>
         <CardHeader
        style={{'background': '#b0bec5'}}
        avatar={
          <Avatar sx={{ bgcolor: blue[500] }} aria-label="Radar">
           <RadarRoundedIcon/>
          </Avatar>
        }
        title="R A D A R"
        subheader="PATHFINDER"
      />
         <br/>
         <Main/>
         </Paper>
        </Grid>
        <Grid item xs={3}>
        <Paper elevation={3} >
        <CardHeader
        style={{'background': '#b0bec5'}}
        avatar={
          <Avatar sx={{ bgcolor: green[500] }} aria-label="Camera">
           <CameraswitchRoundedIcon/>
          </Avatar>
        }
        action={
          <Button variant="contained" startIcon={<VrpanoRoundedIcon />}>
          Panoramic
        </Button>
        }
        title="I M A G I N G"
        subheader="PANORAMIC IMAGING"
      />
            <br/>
            <div>
            <iframe height="200" width="200 " src="http://karr.local:98/"></iframe>

            </div>
         <br/>
        
         </Paper>
         <br/>
         <Paper elevation={3} style={{'background': '#455a64'}}>
         <CardHeader
        style={{'background': '#b0bec5'}}
        avatar={
          <Avatar sx={{ bgcolor: purple[500] }} aria-label="Console">
           <TerminalRoundedIcon/>
          </Avatar>
        }
        title="H A R D W A R E"
        subheader="CONSOLE"
      />
  <Typography>$</Typography>
         <br/>
         <br/>
         <br/>
         <br/>
         <br/>
         <br/>
         </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}