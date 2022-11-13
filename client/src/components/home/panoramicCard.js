import { Avatar, Button, CardHeader, Paper } from '@mui/material'
import { red } from '@mui/material/colors';
import React, { Component, useEffect } from 'react'
import CameraswitchRoundedIcon from '@mui/icons-material/CameraswitchRounded';
import VrpanoRoundedIcon from '@mui/icons-material/VrpanoRounded';
import { Pannellum, PannellumVideo } from "pannellum-react";

function PanoCard() {
     useEffect(() => {
      fetch('http://<REMOTE IP>:9823/panoramic?password=<PASSWORD>&remote=true')
         .then((res) => res.json())
         .then((data) => {
            console.log(data);         })
         .catch((err) => {
            console.log(err.message);
         });
   }, []);
    return (
        <Paper elevation={3} >
        <CardHeader
        style={{'background': '#b0bec5'}}
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="Camera">
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
            <div>
            <Pannellum
        width="100%"
        height="400px"
        image='http://<REMOTE IP>:9823/panoramic?password=<PASSWORD>&remote=true'
        pitch={10}
        yaw={180}
        hfov={110}
        autoLoad
        onLoad={() => {
            console.log("panorama loaded");
        }}
    >
 
    </Pannellum>
            </div>
         <br/>
        
         </Paper>
    )
}

export default PanoCard;