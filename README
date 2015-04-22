README
--

To get started with this assignment, three different agents have already been implemented in the '~cs4701/Project2/engines' directory:

* human: read user input to get the move to make
* random: play completely randomly
* greedy: maximize the difference in number of pieces in the given color's favor

The game allows for two of these implementations to play against each other. To start an Othello game, you can run:

    $ python ~cs4701/Project2/othello.py [-aB] [-aW] [-t T] [-v] black_engine white_engine

where black_engine and white_engine are one of the above agents. For example:

    $ python ~cs4701/Project2/othello.py [-aB] [-aW] [-t T] [-v] human greedy

When using the student agent, the alpha-beta pruning of the black and white engines is turned on by using the -aB and -aW options. 

The optional -t option allows you to change the *total* time granted to each player for the match. The default value is 30 seconds.

The -v option allows you to increase the verbosity of the game (display the board on each turn). This option is automatically activated if one of the agent is human.

You can also get helpful messages by typing:

    $ python ~cs4701/Project2/othello.py -h
