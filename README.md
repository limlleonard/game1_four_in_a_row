# Four in a row

## Description

This is a classic puzzle game. Two players play pieces of two colors in turn. The pieces would fall to the bottom. The one who make a row with four pieces wins.

## Installation

1. Clone the repository and switch to the folder:
   ```bash
   git clone https://github.com/limlleonard/game1_four_in_a_row.git
   cd game1_four_in_a_row
   ```
2. Install required python packages
   ```bash
   pip install -r ./requirements.txt
   ```
3. Start the game
   ```bash
   python app.py
   ```
   Alternatively, you could play the terminal version by running
   ```bash
   python app_terminal.py
   ```

## Play

1. Select mode by clicking the number keys
2. Click on the column where you want to play your piece
3. Have fun

## Behind the scene

The game has three internal stages.

- Stage 1: Select mode
- Stage 2: Playing
- Stage 3: Choose if to continue

For the robot, I used Minimax algorithm. Because the goal is to make a row with four pieces and prevent the opponent the do this, the algorithm would calculate a score with the following rules:

- 10k points if the next move would get a four in a row in any direction
- 100 points if the next move woult get a three in a row and the fourth place is not taken by the opponent
- 5 points if the next move would get a two in a row and the rest places are not taken
- 1k points if the opponents move would get a four in a row
- 10 points if the opponents move would get a three in a row
- 2 points if the opponents move would get a two in a row

For each possible move, the scores are summed up. Then the robost would compare, which point has the highest score and make the move.
