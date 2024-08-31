# BuzzQuiz

Library for handling the controllers of the acclaimed PlayStation 2 game _Buzz!_
In a future, also for organizing quizzes just like the game.

# Buzz - Controllers handling

Buzz library contains two modules, 'reader' and 'lights'. As their names
indicate, they handle input reading and lights changes, respectively.

Buzz must be initialized via `buzz.init()`. It will find all available
controllers (doesn't matter how many sets or ports are being used), and
register them so they can be used.
