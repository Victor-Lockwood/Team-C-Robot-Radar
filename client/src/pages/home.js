import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import { AppBar, Button, Stack, Toolbar, Typography } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Latency from '../components/latency';
import ControlGrid from '../components/controlGrid';
import Webcam from "react-webcam";
import SensorChart from '../components/sensorChart';


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
            Hello Adam!
            </h2>
    
         <br/>
         <br/>
         </Paper>
         <br/>

             <ControlGrid/>

       
        </Grid>
        <Grid item xs={6}>
            <Paper elevation={3}>
         Latency
         <br/>
<SensorChart/>    
            <br/>
           
            </Paper>
            <br/>
            <Paper elevation={3}>
         Radar View
    
         <br/>
        
         </Paper>
        </Grid>
        <Grid item xs={3}>
        <Paper elevation={3} >
         Camera
            <br/>
            <Webcam height={200}/>
         <br/>
        
         </Paper>
         <br/>
         <Paper elevation={3}>
         Console
    
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