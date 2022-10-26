import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import ArrowUpwardRoundedIcon from '@mui/icons-material/ArrowUpwardRounded';
import ArrowBackRoundedIcon from '@mui/icons-material/ArrowBackRounded';
import ArrowForwardRoundedIcon from '@mui/icons-material/ArrowForwardRounded';
import ArrowDownwardRoundedIcon from '@mui/icons-material/ArrowDownwardRounded';
import GamepadRoundedIcon from '@mui/icons-material/GamepadRounded';
import { Avatar, CardHeader } from '@mui/material';
import { blueGrey } from '@mui/material/colors';

export default function ControlGrid() {

  const Item = styled(Paper)(({ theme }) => ({
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  }));
  return (
    <Paper elevation={3}>
       <CardHeader
        style={{'background': '#b0bec5'}}
        avatar={
          <Avatar sx={{ bgcolor: blueGrey[500] }} aria-label="Camera">
           <GamepadRoundedIcon/>
          </Avatar>
        }
        title="C O N T R O L "
      />
      <br/>
    <Grid container spacing={2}>
  <Grid item xs={6} md={4}>
    <Item elevation={0}></Item>
  </Grid>
  <Grid item xs={6} md={4}>
  <Button variant="outlined"><ArrowUpwardRoundedIcon/></Button>

  </Grid>
  <Grid item xs={6} md={4}>
    <Item elevation={0}></Item>
  </Grid>
  <Grid item xs={6} md={4}>
  <Button variant="outlined"><ArrowBackRoundedIcon/></Button>

  </Grid>
  <Grid item xs={6} md={4}>
    <Item elevation={0}></Item>
  </Grid>
  <Grid item xs={6} md={4}>
  <Button variant="outlined"><ArrowForwardRoundedIcon/></Button>

  </Grid>
  <Grid item xs={6} md={4}>
    <Item elevation={0}></Item>
  </Grid>
  <Grid item xs={6} md={4}>
  <Button variant="outlined"><ArrowDownwardRoundedIcon/></Button>

  </Grid>
  <Grid item xs={6} md={4}>
    <Item elevation={0}></Item>
  </Grid>
</Grid>
<br/>
    </Paper>
  );
}