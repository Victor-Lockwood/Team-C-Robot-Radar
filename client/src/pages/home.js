import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import GreetingCard from '../components/home/greetingCard';
import ControlCard from '../components/home/controlCard';
import ConsoleCard from '../components/home/consoleCard';
import RadarCard from '../components/home/radarCard';
import VideoCard from '../components/home/videoCard';
import PanoCard from '../components/home/panoramicCard';
import React, { Component, useEffect, useState } from 'react'
import axios, { Axios } from 'axios';
import { Button } from '@mui/material';
import Main from '../components/Main/Main';

export default function Home() {
  const [mapObjects, setMapObjects] = useState([]);
  const [logs, setLogs] = useState([]);
  const [data, setData] = useState({data: []});
  const [err, setErr] = useState('');
  //const getLogs = () => {
    // try{
    //   fetch("http://<REMOTE IP>:9823/logs?password=<PASSWORD>&remote=True").then(
    //   (response) => console.log("THIS" + response)
    // )
    // }
    // catch(error){
    //   console.log(error)
    // }
     
      const fetchLogs = () => {
        fetch("http://<REMOTE IP>:9823/logs?password=<PASSWORD>&remote=True")
          .then((response) => response.json())
          .then((response) => {
            console.log(response);
          })
          .catch(() => {
            console.log("ERROR");
          });
        }
        const fetchMap = () => {
          fetch("http://<REMOTE IP>:9823/mapdata?password=<PASSWORD>&remote=True")
            .then((response) => response.json())
            .then((response) => {
              console.log(response);
            })
            .catch(() => {
              console.log("ERROR");
            });
          }
        const getData = () => {
          fetchLogs();
          const timerId = setInterval(() => {
            fetchMap();
            console.log('Successful Location GET');
          }, 5000);
          
        }
        function myStopFunction() {
          clearInterval(getData);
        }
  return (
    
    <Box sx={{ flexGrow: 1 }}>
        <br/>
      <Grid container spacing={3} padding={2}>
        <Grid item xs={3}>
            <GreetingCard/>
            <Button onClick={getData}>Initialize</Button>
              <br/>
              <Button onClick={myStopFunction}>TIME STOP</Button>
            <ControlCard/>
              <br/>
            <ConsoleCard/>  
        </Grid>
        <Grid item xs={6}>
          <RadarCard/>
        </Grid>
        <Grid item xs={3}>
            <PanoCard/>
        </Grid>
      </Grid>
    </Box>
  );
}