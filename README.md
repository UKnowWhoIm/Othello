This is the classic game othello(a variant of reversi) written in python hosted in a django server.
The board class written in Game/engine.py contains the implementations of the rules
The methods in Game/views.py communicates data between player and the engine
For AI, I used minimax along with alpha beta pruning(to increase efficency) as seen in Game/ai.py


