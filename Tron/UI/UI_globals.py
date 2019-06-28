from ..Backend.Classes.Game import Game



print("GAME CREATED...", flush=True)
# Define global GAME object
GAME = Game()
GAME.me.setName("Peter")
GAME.me.setColor((1, 1, 0))
GAME.me.setVelocity(1, 0)
GAME.me.setPosition(20, 20)
