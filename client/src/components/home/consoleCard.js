import TerminalRounded from '@mui/icons-material/TerminalRounded';
import { Avatar, CardHeader, Paper, Typography } from '@mui/material'
import { purple } from '@mui/material/colors';
import React, { Component, useEffect, useState } from 'react'

function ConsoleCard() {
    const [logs, setLogs] = useState("");
    const [isLoaded, setIsLoaded] = useState(false);
    const [items, setItems] = useState([]);
    var headers = {}
    useEffect(() => {
      fetch('http://<REMOTE IP>:9823/logs?password=<PASSWORD>&remote=True')
         .then((res) => res.json())
         .then((data) => {setLogs(data[0].message); })
         .catch((err) => {
            console.log(err.message);
         });
   }, []);

  
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
 <Typography>{logs}</Typography>
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