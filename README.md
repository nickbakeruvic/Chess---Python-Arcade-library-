# Python-Chess

# Installation
Requires arcade & stockfish modules downloaded, along with all the files in the repo\n
Arcade module&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> pip install arcade\n
Stockfish module&nbsp;&nbsp;-> pip install stockfish

# Running the game
simply run chess.py; may take a couple seconds to load in the sprites

# Instructions & notes
Clicking on a piece will display all legal moves (with a brown circle) and all possible takes with a red circle around the piece to be taken. If the king is in check, his square will be highlighted pink. Pressing the "undo" button in the bottom right of the window will reverse the last move; pressing the "lightbulb" button will automatically play the best engine move found by stockfish. If the game ends through checkmate / stalemate, one can undo moves and keep playing from any point in the game.
