import shlex
import re

def parser (text:str, player_name:str)->int:
	"""
	trying to understand, if the message is about
	player's death or win or ist it something else
	"""

	if len(text) < 1 or len(player_name) < 1 :
		raise ValueError


	looser_list = ["die","lost","loose","died","dead","worst"]
	win_list = ["win","champion","winner","won","best","lifes"]
	not_list = ["not", "no"]
	inversion = False

	word_list = shlex.split(text, comments=False, posix=True)
	print (word_list)
	
	answer = 0

	for word in range (0, len(word_list)):
		#check bad symbols


	# built string
		string = word_list[word].lower() + "*" 
		#inversion test
		for item in range (0,len(not_list)):
			try:
				neg_match= re.match(string,"not")
			except Exception:
				pass
			if neg_match:
				inversion = True

		#win list
		for item in range (0,len(win_list)):
			try:
				win_match = re.match(string,win_list[item])
			except Exception:
				pass
			if win_match :
				answer = 1
		
		if answer == 0:
			# looser list
			for item in range (0,len(looser_list)):
				try:
					looser_match = re.match(string,looser_list[item])
				except Exception:
					pass
				if looser_match :
					answer = -1
		
	if inversion & (answer != 0):
		answer *= -1

	return answer
