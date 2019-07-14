import shlex
import re

def parser (text:str, player_name:str)->int:
	"""
	trying to understand, if the message is about
	player's death or win or ist it something else
	"""

	looser_list = ["die","lost","loose"]
	win_list = ["win","champion","winner"]
	not_list = ["not", "no"]
	inversion = False

	word_list = shlex.split(text, comments=False, posix=True)
	print (word_list)
	
	answer = 0

	for word in range (0, len(word_list)):
	# built string
		string = word_list[word].lower() + "*" 
		#string = word_list[word].lower() + ".*?" 
		for item in range (0,len(not_list)):
			if re.match(string,"not"):
				inversion = True


		for item in range (0,len(win_list)):
			if re.match(string,win_list[item]) :
				answer = 1
		
		if answer == 0:

			for item in range (0,len(looser_list)):
				if re.match(string,looser_list[item]) :
					answer = -1
		
	if inversion & (answer != 0):
		answer *= -1

	return answer
