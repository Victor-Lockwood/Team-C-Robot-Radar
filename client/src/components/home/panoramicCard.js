import { Avatar, Button, CardHeader, Paper } from '@mui/material'
import { red } from '@mui/material/colors';
import React, { Component } from 'react'
import CameraswitchRoundedIcon from '@mui/icons-material/CameraswitchRounded';
import VrpanoRoundedIcon from '@mui/icons-material/VrpanoRounded';

function PanoCard() {
  
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
            <br/>
            <div>
            <iframe height="200" width="200 " src="http://karr.local:98/"></iframe>

            </div>
         <br/>
        
         </Paper>
    )
}

export default PanoCard;