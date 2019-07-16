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

	#erase bad symbols
	try:
		bad_char_index = text.index("\'")
		text = text[:(bad_char_index-1)] + text[(bad_char_index+1):]
	except:
		pass

	word_list = shlex.split(text, comments=False, posix=True)
	answer = 0

	for word in range (0, len(word_list)):
		#check bad symbols
		try:
			bad_char_index = word_list[word].index("\'")
			word_list[word][bad_char_index] = "q"
		except:
			pass

		# for letter in range (0, len(word_list[word])):
		# 	if word_list[word] == "'":
		# 		word_list[word] = word_list[word][0:letter-1]

	# built string
		string = word_list[word].lower() + "*" 
		#inversion test
		for item in range (0,len(not_list)):
			if re.match(string,"not"):
				inversion = True

		#win list
		for item in range (0, len(win_list)):
			if re.match(string, win_list[item]):
				answer = 1

		if answer == 0:
			# looser list
			for item in range (0,len(looser_list)):
				if re.match(string,looser_list[item]) :
					answer = -1
		
	if inversion & (answer != 0):
		answer *= -1

	return answer
