# othello-agent

This was an assignment for the artificial intelligence course at Columbia University. The assignment was to take skeleton code for the game Othello, and create a rational agent to play the game and beat the random player, greedy player, as well as other students, using the minimax algorithm, as well as alpha-beta pruning.

To get started with this assignment, three different agents have already been implemented:

* human: read user input to get the move to make
* random: play completely randomly
* greedy: maximize the difference in number of pieces in the given color's favor

The game allows for two of these implementations to play against each other. To start an Othello game, you can run:

    $ python othello.py [-aB] [-aW] [-t T] [-v] black_engine white_engine

where black_engine and white_engine are one of the above agents. For example:

    $ python othello.py [-aB] [-aW] [-t T] [-v] human greedy
    
To play with the rational agent (sks2187.py) using alpha-beta pruning run:
    
    $ python othello.py -aW -v random sks2187

When using the student agent, the alpha-beta pruning of the black and white engines is turned on by using the -aB and -aW options. 

The optional -t option allows you to change the *total* time granted to each player for the match. The default value is 30 seconds.

The -v option allows you to increase the verbosity of the game (display the board on each turn). This option is automatically activated if one of the agent is human.

You can also get helpful messages by typing:

    $ python othello.py -h
