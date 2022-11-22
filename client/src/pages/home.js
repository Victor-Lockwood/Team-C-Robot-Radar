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
  const [intervalId, setIntervalId] = useState(0);
  const [data, setData] = useState({data: []});
  const [err, setErr] = useState('');
 
  
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
          if(intervalId) {
            clearInterval(intervalId);
            setIntervalId(0);
            return;
          }
          const timerId = setInterval(() => {
            fetchMap();
            console.log('Successful Location GET');
          }, 5000);
          setIntervalId(timerId);
          
        }
       
  return (
    
    <Box sx={{ flexGrow: 1 }}>
        <br/>
      <Grid container spacing={3} padding={2}>
        <Grid item xs={3}>
            <GreetingCard/>
            <Button onClick={getData}>Initialize</Button>
              <br/>
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