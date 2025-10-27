# Artificial Intelligence Assignment
## AI Hinger Game

### Overview
The objective of this coursework is to design and implement solutions for a combinatorial 
game problem known as Hinger, with a focus on comparing the efficiency of different 
techniques learned in the module

### Features
- Implementation of multiple AI strategies:
  - Minimax
  - Alpha-Beta Pruning
  - Monte Carlo Tree Search
  - Hybrid Strategy (Alpha-Beta + Monte Carlo)
- Board evaluation based on active regions and hingers.
- Random board generation and move simulation.
- Timing and performance comparison of strategies.

### Structure
- `a1_state.py` : Contains the `State` class representing the game board.
- `a3_agent.py` : Contains the `Agent` class implementing the AI strategies.
- `tester()` functions in both files allow demonstration and testing of functionality.

### Requirements
- Python 3.8 or higher
- Standard libraries: random, copy, typing, time