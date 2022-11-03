import VideocamRounded from '@mui/icons-material/VideocamRounded';
import { Avatar, CardHeader, Paper } from '@mui/material'
import { green } from '@mui/material/colors';
import React, { Component } from 'react'

function VideoCard() {
  
    return (
        <Paper elevation={3} >
        <CardHeader
        style={{'background': '#b0bec5'}}
        avatar={
          <Avatar sx={{ bgcolor: green[500] }} aria-label="Camera">
           <VideocamRounded/>
          </Avatar>
        }
        
        title="I M A G I N G"
        subheader="LIVE IMAGING"
      />
            <br/>
            <div>
            <iframe height="200" width="200 " src="http://karr.local:98/"></iframe>

            </div>
         <br/>
        
         </Paper>
    )
}

export default VideoCard;