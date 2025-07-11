# linkedin-solvers
Solvers for LinkedIn's [Tango](https://www.linkedin.com/games/tango/) and [Queens](https://www.linkedin.com/games/tango/) games, written in Python.

## 1. Tango Solver
The first solver works for [LinkedIn's Tango](https://www.linkedin.com/games/tango/) game, the [Tango](https://apps.apple.com/us/app/tango-daily-binairo-puzzle) app, and the [Puzzle Binairo](https://www.puzzle-binairo.com/binairo-plus-6x6-easy/) website. It can solve text and image inputs.

### Example (LinkedIn Tango)
Puzzle solved in 4 ms.

**Input**

<img src="tango/screenshots/linkedin-2025-05-05-input.png" alt="" width="300">

**Output**

<img src="tango/screenshots/linkedin-2025-05-05-solved.png" alt="" width="300">

### Example (Tango App)
Puzzle solved in 70 ms.

**Input**

<img src="tango/screenshots/tango-genius-2-input.png" alt="" width="300">


**Output**

<img src="tango/screenshots/tango-genius-2-solved.png" alt="" width="300">


## 2. Queens Solver

The second solver is for [LinkedIn's Queens](https://www.linkedin.com/games/queens/) game. It can solve text or image inputs.

### Example
Puzzle solved in 14 ms.

**Input**

<img src="queens/screenshots/2025-05-25-B-input.png" alt="" width="300">

**Output**

<img src="queens/screenshots/2025-05-25-B-solved.png" alt="" width="300">

# How do they work?
To solve the games, each program applies a set of simple deduction strategies over and over until it gets stumped.

Then, it makes a guess on an unknown cell and continues solving recursively. If solving runs into a contradiction, we know our guess is incorrect. This continues until we have a complete and valid board.

This combination of known deduction strategies and recursive backtracking improves program performance while ensuring that even the most challenging puzzles can be solved quickly.