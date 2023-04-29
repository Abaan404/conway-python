<h3 align="center">Conway's Game of Life</h3>
<p align="center">A Python/Pygame implementation of the famous cellular automata.</p>
<br/>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

Conways game of life is a cellular automata created by <a href=https://conwaylife.com/wiki/John_Conway>John Horton Conway</a>. The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells, each of which (at any given time) is in one of two possible states, "live" (alternatively "on") or "dead" (alternatively "off"). Every cell interacts with its eight neighbours, which are the cells that are directly horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

These simple rules are enough to consider the game as "[Turing Complete](https://www.youtube.com/watch?v=4lO0iZDzzXk)" ([relevant xkcd](https://xkcd.com/2556/)).
The [ConwayLife Wiki Pattern Archive](https://conwaylife.com/wiki/Category:Patterns) has a large collection of various patterns to play with that can be downloaded into the `./patterns` directory. Some patterns may be larger than the default grid size, this can be increased within the `config.py` if necessary.
This project was created in 2 weeks as a uni assignment and as such will see minimal development, this was made mostly for fun and will stay as such.

## Getting Started

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Abaan404/conway-python
   ```

2. Install the required Python packages
   ```sh
   pip3 install -r requirements.txt
   ```
3. Run the script
   ```sh
   python3 main.py # tested with python 3.10
   ```

### Usage

Following are the default keybindings. There are more config options within the `config.py` file to tinker with.

| Name                |      Keybind       | Description                            |
| ------------------- | :----------------: | -------------------------------------- |
| Draw/Erase (Toggle) | Left Mouse Button  | Toggle a cell on the grid              |
| Zoom In/Out         | Mouse Scroll Wheel | Zoom in/out of the grid                |
| Move Highlight      |      W/A/S/D       | Move the current highlight on the grid |
| Toggle Highlight    |       Enter        | Toggle the current highlighted cell    |
| Run                 |         R          | Run the simulation                     |
| Step                |         E          | Step through each generation           |
| Reset               |         Q          | Reset the grid                         |
| Cycle Patterns      |     Left/Right     | Cycle through available patterns       |
| Debug               |         F3         | Display debug info                     |

## Acknowledgments

- The amazing video by [Rational Animations](https://www.youtube.com/watch?v=C2vgICfQawE) which had inspired me to make this project.
- Fonts by JetBrains Mono.
