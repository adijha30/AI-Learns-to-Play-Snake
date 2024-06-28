# AI-Learns-to-Play-Snake
A project to train an AI how to play snake using the NEAT-Python Framework <br/>
We utilise [neat-python](https://github.com/CodeReclaimers/neat-python) for evolution of the neural network and [pygame](https://github.com/pygame/pygame) for the UI of the game.<br/>

# Overview of how the Snake Learns
The initial few generations have the snake learn that dying due to wall collisions is bad. What this effectively does is teach them how to turn to avoid death. The best snakes are bred <br/>

Over the next generations the best snakes are chosen for reproduction <br/>


By the time the snake reaches the 12-15th generations, it has learned quite well and is easily able to grow to long lengths <br/>


# Overview on how the snake is trained
The Snake function rewards/punishes the snakes by increasing/decreasing its fitness according to what it does: <br/>

Activities that increase Fitness: Eating an Apple <br/>
Activities that decrease Fitness: Dying, staying alive without eating an apple <br/>

[Note that the Snake is punished differently based on the cause of death; there are 2 ways it dies, self-collisions and wall-collisions]

