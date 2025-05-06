# linkedin-solvers
Solvers for LinkedIn daily games, written in Python.

## Tango
Solver for Tango game on LinkedIn. The program accepts text or image inputs. Also works to solve puzzles from the Tango iOS app.

### LinkedIn
This puzzle was solved in 0.5 seconds.

**Input**

![](tango/screenshots/linkedin-210-input.png)

**Output**

![](tango/screenshots/linkedin-210-solved.png)

### Tango App
This puzzle was solved in 0.9 seconds.

**Input**

![](tango/screenshots/tango-genius-2-input.png)

**Output**

![](tango/screenshots/tango-genius-2-solved.png)

### How does it work?
#### Input parsing - Text

For text inputs, parsing is straightforward. Here's an example .txt input:

![](tango/screenshots/linkedin-210-text.png)

#### Input parsing - Images

For image inputs, the program finds all the cells and edges of the board using OpenCV.

Here's what the program "sees" when parsing an image:

![](tango/screenshots/linkedin-210-debug.png)

#### Puzzle data structure

We store the parsed cells and edges in a puzzle object. Here's what a puzzle looks after parsing:

![](tango/screenshots/linkedin-210-parsed.png)

#### Solution algorithm

To solve the game, it applies a few simple deduction strategies over and over until it gets stumped. Then, it just makes a guess on an unknown cell and continues solving. If solving the puzzle with that guess runs into a contradiction, we know the cell must be the other symbol. This continues until we have a complete and valid board. The algorithm is a type of recursive backtracking.

Here's an example output of the program

![](tango/screenshots/linkedin-210-solved.png)
