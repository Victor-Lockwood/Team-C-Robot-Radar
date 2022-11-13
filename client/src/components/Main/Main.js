import React, { Component } from "react";
import Node from "./Djikstra/Node";
import NavigationBar from "./Djikstra/NavigationBar";
import { dijkstra, getNodesInShortestPathOrder } from "./Djikstra/dijkstra";

var START_NODE_ROW = 5;
var START_NODE_COL = 5;
var FINISH_NODE_ROW = 1;
var FINISH_NODE_COL = 15;

export default class Main extends Component {

  constructor(props) {
    super(props);
    this.state = {
      grid: [],
      mouseIsPressed: false,
      obstacleList: [],
      ourRobot:[],
      ourRobot_X: 0,
      ourRobot_Y: 0,
      testCoordinateX : 0
    
    };
  }

  componentDidMount() {
   fetch('http://<REMOTE IP>:9823/mapdata?password=<PASSWORD>&remote=True')
    .then((response) => response.json())
    .then(Main => {
        this.setState({ obstacleList: Main });
    })
    console.log(this.obstacleList)
   
    const grid = getInitialGrid();
    
    this.setState({ grid });
    
  }

  handleMouseDown(row, col) {
    const newGrid = getNewGridWithWallToggled(this.state.grid, row, col);
    this.setState({ grid: newGrid, mouseIsPressed: true });
  }

  handleMouseEnter(row, col) {
    if (!this.state.mouseIsPressed) return;
    const newGrid = getNewGridWithWallToggled(this.state.grid, row, col);
    this.setState({ grid: newGrid });
  }

  handleMouseUp() {
    this.setState({ mouseIsPressed: false });
  }

  animateDijkstra(visitedNodesInOrder, nodesInShortestPathOrder) {
    for (let i = 0; i <= visitedNodesInOrder.length; i++) {
      if (i === visitedNodesInOrder.length) {
        setTimeout(() => {
          this.animateShortestPath(nodesInShortestPathOrder);
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

  animateShortestPath(nodesInShortestPathOrder) {
    for (let i = 0; i < nodesInShortestPathOrder.length; i++) {
      setTimeout(() => {
        const node = nodesInShortestPathOrder[i];
        document.getElementById(`node-${node.row}-${node.col}`).className =
          "node node-shortest-path";
      }, 50 * i);
    }
  }

  visualizeDijkstra(X, Y) {
    const { grid } = this.state;
    const startNode = grid[X][Y];
    const finishNode = grid[FINISH_NODE_ROW][FINISH_NODE_COL];
    const visitedNodesInOrder = dijkstra(grid, startNode, finishNode);
    const nodesInShortestPathOrder = getNodesInShortestPathOrder(finishNode);
    this.animateDijkstra(visitedNodesInOrder, nodesInShortestPathOrder);
  }

  clearPath() {
    this.setState({ grid: [] });
    const grid = getInitialGrid();
    this.setState({ grid });
  }

  render() {
    this.state.ourRobot = this.state.obstacleList.filter((obj) => obj.object_type === "OurRobot")
    this.state.ourRobot.map((obstacle) => (
    this.state.ourRobot_X = obstacle.location[0],
    this.state.ourRobot_Y = obstacle.location[1],
    console.log("PIN", this.state.ourRobot_X, this.state.ourRobot_Y)
))
    const { grid, mouseIsPressed } = this.state;
 
    return (
      <div>
        <NavigationBar
          onVisiualizePressed={() => this.visualizeDijkstra(this.state.ourRobot_X , this.state.ourRobot_Y )}
          onClearPathPressed={() => this.clearPath()}
        />
 <ul>
                {this.state.obstacleList.map((obstacle) => (
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
                      onMouseDown={(row, col) => this.handleMouseDown(row, col)}
                      onMouseEnter={(row, col) =>
                        this.handleMouseEnter(row, col)
                      }
                      onMouseUp={() => this.handleMouseUp()}
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
}

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
    isStart: row === START_NODE_ROW && col === START_NODE_COL,
    isFinish: row === FINISH_NODE_ROW && col === FINISH_NODE_COL,
    distance: Infinity,
    isVisited: false,
    isWall: false,
    previousNode: null
  };
};

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
