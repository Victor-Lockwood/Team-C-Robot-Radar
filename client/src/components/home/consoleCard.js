import TerminalRounded from '@mui/icons-material/TerminalRounded';
import { Avatar, CardHeader, Paper, Typography } from '@mui/material'
import { purple } from '@mui/material/colors';
import React, { Component } from 'react'

function ConsoleCard() {
  
    return (
        <Paper elevation={3} style={{'background': '#455a64'}}>
        <CardHeader
       style={{'background': '#b0bec5'}}
       avatar={
         <Avatar sx={{ bgcolor: purple[500] }} aria-label="Console">
          <TerminalRounded/>
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
    )
}

export default ConsoleCard;