import Node from "./Djikstra/Node";
import NavigationBar from "./Djikstra/NavigationBar";
import { dijkstra, getNodesInShortestPathOrder } from "./Djikstra/dijkstra";
import React, { useState, useEffect } from 'react';
import { Button } from "@mui/material";

export default function Main() {
  const [ourRobotX, setOurRobotX] = useState(0);
  const [ourRobotY, setOurRobotY] = useState(0);
  const [rawMap, setRawMap]  = useState([]);
  const [grid, setGrid] = useState([]);

var FINISH_NODE_ROW = 1;
var FINISH_NODE_COL = 9;
const [intervalId, setIntervalId] = useState(0);

const postDjikstra = () =>  {
    
  // Send data to the backend via POST
  fetch('http://<REMOTE IP>:9823/autonomous?password=<PASSWORD>&remote=True', {  // Enter your IP address here

    method: 'POST', 
    body: JSON.stringify(
      {
        "Coordinates":
         [
            [15, 1],
            [15, 2],
            [15, 3],
            [15, 4],
            [15, 5],
            [15, 6],
            [15, 7],
            [15, 8],
            [15, 9]
        ]
     }
    ) 

  })
  
}

 const fetchMap = () => {
  fetch("http://<REMOTE IP>:9823/mapdata?password=<PASSWORD>&remote=True")
    .then((response) => response.json())
    .then((response) => {
      for (let i = 0; i < response.length; i++) {
        setRawMap(response)
        if(response[i].object_type == "OurRobot"){
          setOurRobotX(response[i].location[0])
          setOurRobotY(response[i].location[1])
        }
        
      }
    }).then(setGrid(getObstacleGrid(rawMap)))
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
  const getInitialGrid = () => {
    const grid = [];
    for (let row = 0; row < 11; row++) {
      const currentRow = [];
      for (let col = 0; col < 11; col++) {
        currentRow.push(createNode(col, row));
      }
      grid.push(currentRow);
    }
    return grid;
  };
  const getObstacleGrid = (rawMap) => {
    const grid = [];
    for (let row = 0; row < 11; row++) {
      const currentRow = [];
      for (let col = 0; col < 11; col++) {
        currentRow.push(createNode(col, row));
      }
      grid.push(currentRow);
    }
    console.log(rawMap)
    for (let i = 0; i < rawMap.length ; i++) {
        const newGrid = getNewGridWithWallToggled(grid, rawMap[i].location[0], rawMap[i].location[1]);
    setGrid(newGrid);
      
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
 
  useEffect(() => {
    setGrid(getInitialGrid())
  }, []);
 
  function animateDijkstra(visitedNodesInOrder, nodesInShortestPathOrder) {
    for (let i = 0; i <= visitedNodesInOrder.length; i++) {
      if (i === visitedNodesInOrder.length) {
        setTimeout(() => {
          animateShortestPath(nodesInShortestPathOrder);
        }, 11 * i);
        return;
      }
      setTimeout(() => {
        const node = visitedNodesInOrder[i];
        document.getElementById(`node-${node.row}-${node.col}`).className =
          "node node-visited";
      }, 11 * i);
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

  function visualizeDijkstra() {
    const startNode = grid[ourRobotX][ourRobotY+1];
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
  
    return (
      <div>
        <NavigationBar
          onVisiualizePressed={() => visualizeDijkstra()}
          onClearPathPressed={() => clearPath()}
          getCoordinates={() => fetchMap()}
          timeCoordinates={() => getData()}

        />

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


