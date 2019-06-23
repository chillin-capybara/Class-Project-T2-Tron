import typing
import sys
import json
sys.path.append("/Users/marcellpigniczki/Documents/GitHub/Class-Project-T2-Tron")
from Tron.Backend.Classes.Player import Player as Player
from Tron.Backend.Classes.Factory import Factory
from Tron.Backend.Classes.Game import Game
def example(in1: int, in2: str, in3: Player) -> str:
	if type(in1) is not int:
		raise TypeError
	
	return "Hello"


var = example(1, 2, Player())
print(var)

def example2(in1: list):
	for item in in1:
		item: int # Fixes the type
		item = str(item) # Converts the type
		print(item)

example2([1,2,3,4,5,6])


class Dummy(object):
	name = "I'm Dummy!"

	def __str__(self): # convert to string Implemetierung
		return self.name

new = Dummy()
print(str(new))


myplayer = Factory.Player("Dummy", 2)
myplayer.setColor(2)

# Nur example
def update_ui():
	players = Game.getPlayers()
	for player in player:
		player: Player
		color = player.getColor()

def update_track():
	for track in Game.getTrack():
		track: Track
		track.getStart()
		track.getEnd()


mydict = {"playername": "Dummy", "color": 2}
json_string = json.dumps(mydict)

with open("myfile.json", "w") as fh:
	fh.write(json_string)

# THE EASY WAY
data = ""

with open("myfile.json", "r") as fh:
	data = fh.readlines()

mydict = json.loads(data)

# THE HARD WAY
try:
	fh = open("irgendwas.json", "w")
	json.dump(mydict, fh)
finally:
	try:
		fh.close()
	except:
		pass