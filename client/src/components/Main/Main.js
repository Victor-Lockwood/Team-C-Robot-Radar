import Node from "./Djikstra/Node";
import NavigationBar from "./Djikstra/NavigationBar";
import { dijkstra, getNodesInShortestPathOrder } from "./Djikstra/dijkstra";
import React, { useState, useEffect } from 'react';
import axios from "axios";

var START_NODE_ROW = 5;
var START_NODE_COL = 5;
var FINISH_NODE_ROW = 1;
var FINISH_NODE_COL = 15;

export default function Main() {
  const [ourRobotX, setOurRobotX] = useState(0);
  const [ourRobotY, setOurRobotY] = useState(0);
  axios.get('http://<REMOTE IP>:9823/mapdata?password=<PASSWORD>&remote=True')
  .then((response) => {
    for(let i = 0; i < response.data.length; i++){
      if(response.data[i].object_type == 'OurRobot'){
        setOurRobotX(response.data[i].location[0])
        setOurRobotY(response.data[i].location[1])
        setGrid(getInitialGrid())

      } else {
        setGrid(getInitialGrid())
        handleMouseDown(response.data[i].location[0], response.data[i].location[1])
      }

    }
  })
  .catch((err) => {
     console.log(err);
  });
  

  const getInitialGrid = () => {
    const grid = [];
    for (let row = 0; row < 20; row++) {
      const currentRow = [];
      for (let col = 0; col < 20; col++) {
        currentRow.push(createNode(col, row));
      }
      grid.push(currentRow);
    }
    return grid;
  };
  const createNode = (col, row) => {
    return {
      col,
      row,
      isStart: row === ourRobotX && col === ourRobotY,
      isFinish: row === FINISH_NODE_ROW && col === FINISH_NODE_COL,
      distance: Infinity,
      isVisited: false,
      isWall: false,
      previousNode: null
    };
  };
  
  //inital state for hooks
  const [grid, setGrid] = useState([]);
  const [mouseIsPressed, setmouseIsPressed] = useState(false);
  const [obstacleList, setObstacleList] = useState([]);
  const [test, setTest] = useState(1);
 
  useEffect(() => {
    const fetchData = async () => {
      const result = await axios(
        'http://<REMOTE IP>:9823/mapdata?password=<PASSWORD>&remote=True',
      );
      for(let i = 0; i < result.data.length; i++){
        if(result.data[i].object_type == 'OurRobot'){
          setOurRobotX(result.data[i].location[0])
          setOurRobotY(result.data[i].location[1])
          setGrid(getInitialGrid())

        } else {
          setGrid(getInitialGrid())
          handleMouseDown(result.data[i].location[0], result.data[i].location[1])
        }

      }
    
      //console.log(result.data[0]);
    };

    fetchData();
  }, []);


  // grid: [],
  // mouseIsPressed: false,
  // obstacleList: [],
  // ourRobot:[],
  // ourRobot_X: 0,
  // ourRobot_Y: 0,
  // testCoordinateX : 0


  //  fetch('http://<REMOTE IP>:9823/mapdata?password=<PASSWORD>&remote=True')
  //   .then((response) => response.json())
  //   .then(Main => {
  //       this.setState({ obstacleList: Main });
  //   })
  //   console.log(this.obstacleList)
   
  //   const grid = getInitialGrid();
    
  //   this.setState({ grid });
    

  function handleMouseDown(row, col) {
    const newGrid = getNewGridWithWallToggled(grid, row, col);
    setGrid(newGrid);
    setmouseIsPressed(true);
  }

  function handleMouseEnter(row, col) {
    if (!mouseIsPressed) return;
    const newGrid = getNewGridWithWallToggled(grid, row, col);
    setGrid(newGrid)
  }

  function handleMouseUp() {
    setmouseIsPressed(false);
  }

  function animateDijkstra(visitedNodesInOrder, nodesInShortestPathOrder) {
    for (let i = 0; i <= visitedNodesInOrder.length; i++) {
      if (i === visitedNodesInOrder.length) {
        setTimeout(() => {
          animateShortestPath(nodesInShortestPathOrder);
        }, 10 * i);
        return;
      }
      setTimeout(() => {
        const node = visitedNodesInOrder[i];
        document.getElementById(`node-${node.row}-${node.col}`).className =
          "node node-visited";
      }, 10 * i);
    }
  }

  function animateShortestPath(nodesInShortestPathOrder) {
    for (let i = 0; i < nodesInShortestPathOrder.length; i++) {
      setTimeout(() => {
        const node = nodesInShortestPathOrder[i];
        document.getElementById(`node-${node.row}-${node.col}`).className =
          "node node-shortest-path";
      }, 50 * i);
    }
  }

  function visualizeDijkstra(X, Y) {
    const startNode = grid[X][Y];
    const finishNode = grid[FINISH_NODE_ROW][FINISH_NODE_COL];
    const visitedNodesInOrder = dijkstra(grid, startNode, finishNode);
    const nodesInShortestPathOrder = getNodesInShortestPathOrder(finishNode);
    animateDijkstra(visitedNodesInOrder, nodesInShortestPathOrder);
  }

  function clearPath() {
     setGrid(getInitialGrid());
  }
 
  
 
  const getNewGridWithWallToggled = (grid, row, col) => {
    const newGrid = grid.slice();
    const node = newGrid[row][col];
    const newNode = {
      ...node,
      isWall: !node.isWall
    };
    newGrid[row][col] = newNode;
    return newGrid;
  };
  
//     this.state.ourRobot = this.state.obstacleList.filter((obj) => obj.object_type === "OurRobot")
//     this.state.ourRobot.map((obstacle) => (
//     this.state.ourRobot_X = obstacle.location[0],
//     this.state.ourRobot_Y = obstacle.location[1],
//     console.log("PIN", this.state.ourRobot_X, this.state.ourRobot_Y)
// ))
 
    return (
      <div>

        <NavigationBar
          onVisiualizePressed={() => visualizeDijkstra(ourRobotX , ourRobotY )}
          onClearPathPressed={() => clearPath()}
        />
 <ul>
                {obstacleList.map((obstacle) => (
                    <li key={obstacle.map_id}>{obstacle.object_type}</li>
                ))}
            </ul>
        <div className="grid">
          {grid.map((row, rowIdx) => {
            return (
       
              <div key={rowIdx}>
                {row.map((node, nodeIdx) => {
                  const { row, col, isFinish, isStart, isWall } = node;
                  return (
                    <Node
                      key={nodeIdx}
                      col={col}
                      isFinish={isFinish}
                      isStart={isStart}
                      isWall={isWall}
                      mouseIsPressed={mouseIsPressed}
                      onMouseDown={(row, col) => handleMouseDown(row, col)}
                      onMouseEnter={(row, col) =>
                        handleMouseEnter(row, col)
                      }
                      onMouseUp={() => handleMouseUp()}
                      row={row}
                    ></Node>
                  );
                })}
              </div>
             
            );
          })}
        </div>
      </div>
    );
  }


