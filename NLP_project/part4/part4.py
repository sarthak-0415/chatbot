####.....ASSUMPTIONS.........
####......1. the match number is given as digits e.g. 'match 3'.....
####......2. if no country given assume country = india.....
####......3. if match no not given and player name not given too....

import nltk	
import sys
import re
import textblob
from textblob import TextBlob
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn
import os
from nltk.util import ngrams

os.system('clear')

question=''
ques =[]
query_pos = []
player= 'None'
country= 'None'
player_type= 'None'
query_ques= []
search_keywords =[]
match_number = 0
commentary =[]

def add_to_dict_player(dictionary, fname):
	f = open(fname, 'r')
	for line in f:
		temp = line[:-1]
		temp = temp.split('\t')
		a=temp[0]
		#print a
		b=temp[1:]
		if a not in dictionary:
			dictionary[a] = b

def parse_for_match_no():
	global question
	global match_number
	
	ques_temp=re.sub('[^0-9a-zA-Z ]+', '', str(question))
	q = ques_temp.split(' ')
	
	for i in q:
		i=re.sub('[ ]+', '', str(i))
		word = i.lower()
		if word == 'match' :
			index=q.index(i)
			if q[index+1].isdigit():
				match_number = q[index+1]
			elif q[index-1].isdigit():
				match_number = q[index+1]	
				
	#print 'match_number::'
	#print match_number						

def parse_for_player_type():
	
	global ques
	global player_type
	
	for word in ques:
		word =re.sub('[^a-zA-Z]+', '', str(word))
		word_l = word.lower()
		if (word_l=='bowled'or word_l=='wickets' or word_l=='wicket' or word_l=='economy rate' or word_l=='no ball' or word_l=='no balls' or word_l=='wide' or word_l=='wides'):
			player_type = 'bowler'
		
		elif (word_l=='dismissed' or word_l == 'boundary' or word_l=="four" or word_l=="six" or word_l=="strike rate" or word_l=='out' or word_l=='dismissed' or word_l=='fours' or word_l=='sixes' or word_l=='hit'):
			player_type = 'batsman'
			
	#print 'player_type::'
	#print player_type		


def parse_for_commentary(file, commentary_parse):
	
	commentary = open(file,'r')
	ans = []
	
	for line in commentary:
		temp1 = line[:-1]
		temp2 = temp1.split(' ')			
		commentary_parse.append(temp2) 
	
	return commentary_parse	


def select_commentary(player_data):
	
	global commentary
	global player_type
	global match_number
	global country
	
	comm=[]
	f1 = './dataset/match'
	f2 = './dataset/match'
	
	if(country == 'india'):
		not_country = 'newzealand'
		
	elif country == 'newzealand':
		not_country = 'india'	
	
	if player_type!= 'None' and country != 'None':
		if(player_type == 'bowler'):
			f1 += str(match_number) + '/odi' + str(match_number)+ '_' +  str(not_country) + '_commentary.txt'	
		else:
			f1 += str(match_number) + '/odi' + str(match_number)+ '_' + str(country) + '_commentary.txt'
		
		#print 'f1::'
		#print f1
		commentary = parse_for_commentary(f1,commentary)
			
	elif player_type == 'None' and country != 'None':
		f1 += str(match_number) + '/odi' + str(match_number)+ '_' + str(country) + '_commentary.txt'
		f2 += str(match_number) + '/odi' + str(match_number)+ '_' +  str(not_country) + '_commentary.txt'	
		
		##print 'f1 + f2::'
		#print f1
		#print f2
		comm = parse_for_commentary(f1,comm)
		commentary = parse_for_commentary(f2,comm)
		
	else:
		f1 += str(match_number) + '/odi' + str(match_number)+ '_india_commentary.txt'
		f2 += str(match_number) + '/odi' + str(match_number)+ '_newzealand_commentary.txt'	
		
		#print 'f1 + f2::'
		#print f1
		#print f2
		comm = parse_for_commentary(f1,comm)
		comm1 = parse_for_commentary(f2,comm)	
		commentary = comm1


def parse_for_player_data(india, nz):

	global player
	global country
	global que
	player_data = 'None'
	
	#print 'prntitng'
	#print ques
	
	ques_string =''
	for i in ques:
		ques_string += str(i) + ' '
	ques_string = ques_string[:-1]
	#print 'prntitng'
	#print ques_string
	
	unigram = ngrams(ques_string.split(), n=1)
	unigram_string = []
	for i in unigram :
		string = ''
		for j in i :
			string += str(j) + ' '
		string = string[:-1]
		unigram_string.append(string)
	#print unigram_string

	bigram = ngrams(ques_string.split(), n=2)
	bigram_string = []
	for i in bigram :
		string = ''
		for j in i :
			string += str(j) + ' '
		string = string[:-1]
		bigram_string.append(string)
	#print bigram_string
	

	for word in unigram_string:
		for key in nz :
			#print key
			name = key.split(' ')
			#print name[1]
			if  (word == name[1]):
				player = word
				country ='newzealand'
				player_data =nz[key]

	for word in bigram_string:
		for key in nz :
			if word == key :
				player = word
				country ='newzealand'
				player_data =nz[key]
	
	for word in unigram_string:
		for key in india :
			#print key
			name = key.split(' ')
			#print name[1]
			if  (word == name[1]):
				player = word
				country ='india'
				player_data =india[key]

	for word in bigram_string:
		for key in india :
			if word == key :
				player = word
				country ='india'
				player_data =india[key]
	
	#print 'country::'
	#print country
	
	#print 'player_data::'
	#print player_data
	
	return player_data			

def match_words(words, keywords):
	score = 0
	temp = wn.synsets(words)
	
	if len(temp) > 0:
		word_temp = str(temp[0])
		split_char = word_temp[-2]
		word_temp1 = word_temp.split(split_char)
		word = word_temp1[1]
		#print 'word'
		#print word
	else:
		score = 0
		return score	
	
	word_pos = word.split('.')	
	keyword_pos = keywords.pos
	
	if word_pos[1] == keyword_pos :
		
		word_compare = wn.synset(word)
		
		score = word_compare.wup_similarity(keywords)
		if len(str(score)) != 4:
			#print 'score::'
			#print score
			return score
	
	else:
		score = 0
		return score
			

def pos_tag_ques():
	
	global question
	global query_pos
	
	question = re.sub('[^0-9a-zA-Z ]+', '', str(question))
	q = question.split()
	query_pos = nltk.pos_tag(q)
	#print 'query_pos::'
	#print query_pos

def search_commentary():
	global commentary
	global search_keywords
	global player
	ans =[]
	player_flag =0
	found = 0
	score_uni =[]
	score_bi = []
	comm_player = []
	

	if player!= 'None':
		player_flag = 1
		
		for line in commentary:
			
			prev_index = commentary.index(line) -1
			prev_line = commentary[prev_index]
			
			line_string =''
			for i in line:
				line_string += str(i) + ' '
			line_string = line_string[:-1]

			unigram = ngrams(line_string.split(), n=1)
			unigram_string = []
			for i in unigram :
				string = ''
				for j in i :
					string += str(j) + ' '
				string = string[:-1]
				unigram_string.append(string)
			#print unigram_string

			bigram = ngrams(line_string.split(), n=2)
			bigram_string = []
			for i in bigram :
				string = ''
				for j in i :
					string += str(j) + ' '
				string = string[:-1]
				bigram_string.append(string)
			#print bigram_string
			
			for word in unigram_string:
				word = re.sub('[^0-9a-zA-Z]+', '', str(word))	
				if word == player:
					comm_player.append(prev_line)
					comm_player.append(line)
					break

			for word in bigram_string:
				word = re.sub('[^0-9a-zA-Z]+', '', str(word))
				if word == player:
					comm_player.append(prev_line)
					comm_player.append(line)
					break
				
	#print 'player::'
	#print player
	
	#print 'player_flag::'
	#print player_flag
	search_keywords_unigram = []
	search_keywords_bigram = []
	if player_flag == 1:
		if len(comm_player) > 0:
			for line in comm_player:	
				line_score = 0.0
			
				line_string =''
				for i in line:
					line_string += str(i) + ' '
				line_string = line_string[:-1]
				#print line_string
				
				search_keywords_string =''
				for i in search_keywords:
					x= i[0]
					search_keywords_string += str(x) + ' '
				search_keywords_string = search_keywords_string[:-1]


				unigram_line = ngrams(line_string.split(), n=1)
				unigram_line_string = []
				
				for i in unigram_line :
					string = ''
					for j in i :
						string += str(j) + ' '
					string = string[:-1]
					unigram_line_string.append(string)
				#print unigram_line_string
				
				unigram_keywords = ngrams(search_keywords_string.split(), n=1)
				unigram_keywords_string = []
				
				for i in unigram_keywords :
					string = ''
					for j in i :
						string += str(j) + ' '
					string = string[:-1]
					unigram_keywords_string.append(string)
				#print unigram_keywords_string

				
				uni_line_score =0
				for word in unigram_line_string:
					word = re.sub('[^0-9a-zA-Z]+', '', str(word))	
					for verse in unigram_keywords_string:
						keyword_syn = wn.synsets(verse[0])
						#print 'words ::   ' + word
							
						if len(keyword_syn) > 0:
							for word_k in keyword_syn:
								uni_lscore = match_words(word, word_k)
							
							#print 'uni_lscore::'
							#print uni_lscore
							
							if len(str(uni_lscore)) != 4:
								uni_line_score += uni_lscore

				score_uni.append(str(uni_line_score) +',' + str(comm_player.index(line)))
	

		else:
			player_flag = 0				
	
					
	if player_flag == 0:
		for line in comm_player:	
			line_score = 0.0
		
			line_string =''
			for i in line:
				line_string += str(i) + ' '
			line_string = line_string[:-1]
			#print line_string
			
			search_keywords_string =''
			for i in search_keywords:
				x= i[0]
				search_keywords_string += str(x) + ' '
			search_keywords_string = search_keywords_string[:-1]


			unigram_line = ngrams(line_string.split(), n=1)
			unigram_line_string = []
			
			for i in unigram_line :
				string = ''
				for j in i :
					string += str(j) + ' '
				string = string[:-1]
				unigram_line_string.append(string)
			#print unigram_line_string
			
			unigram_keywords = ngrams(search_keywords_string.split(), n=1)
			unigram_keywords_string = []
			
			for i in unigram_keywords :
				string = ''
				for j in i :
					string += str(j) + ' '
				string = string[:-1]
				unigram_keywords_string.append(string)
			#print unigram_keywords_string


			bigram_line = ngrams(line_string.split(), n=2)
			bigram_line_string = []
			
			for i in bigram_line :
				string = ''
				for j in i :
					string += str(j) + ' '
				string = string[:-1]
				bigram_line_string.append(string)
			#print bigram_line_string
			
			bigram_keywords = ngrams(search_keywords_string.split(), n=2)
			bigram_keywords_string = []
			
			for i in bigram_keywords :
				string = ''
				for j in i :
					string += str(j) + ' '
				string = string[:-1]
				bigram_keywords_string.append(string)
			#print bigram_keywords_string
				
			uni_line_score =0
			for word in unigram_line_string:
				word = re.sub('[^0-9a-zA-Z]+', '', str(word))	
				for verse in unigram_keywords_string:
					if word == verse:
						
						#print 'words ::   ' + word
						uni_lscore = match_words(word, verse)
						#print 'uni_lscore::'
						#print uni_lscore
						if len(str(uni_lscore)) != 4:
							uni_line_score += uni_lscore

			score_uni.append(str(uni_line_score) +',' + str(comm_player.index(line)))

			bi_line_score =0
			for word in bigram_line_string:
				word = re.sub('[^0-9a-zA-Z]+', '', str(word))	
				for verse in bigram_keywords_string:
					if word == verse:
						
						#print 'words ::   ' + word
						bi_lscore = match_words(word, verse)
						#print 'bi_lscore::'
						#print bi_lscore
						if len(str(bi_lscore)) != 4:
							bi_line_score += bi_lscore

			score_bi.append(str(bi_line_score) +',' + str(comm_player.index(line)))

					
	max_score = 0
	
	#print 'score_uni'
	#print score_uni

	#print 'score_bi'
	#print score_bi


	for num in score_uni:
		number = num.split(',')
		if number[0] > max_score :
			max_score = number[0]
			max_index = int(number[1])
	
	for num in score_bi:
		number = num.split(',')
		if number[0] > max_score :
			max_score = number[0]
			max_index = int(number[1])
	
	prev_index =  max_index -1
	
	if player_flag == 0:
		ans.append(commentary[prev_index])
		ans.append(commentary[max_index])		
	else :
		ans.append(comm_player[prev_index])
		ans.append(comm_player[max_index])	
	
	ans_string =''
	for i in ans:
		ans_string += str(i) + ' '
	ans_string = ans_string[:-1]
	
	print 'matching line :: \n' + ans_string + '\n'
	
	return ans	

	
def parse_for_ans(comm):
	
	global query_pos
	global query_ques
	ans = []
	
	query_ques_l = query_ques.lower()
	
	if query_ques_l == 'when':
		over_temp = str(comm[0])
		over_temp =re.sub('[^0-9 .]+', '', str(over_temp))
		over = over_temp.split('.')
		ans = over_temp
	
	elif query_ques_l == 'how':
		#comm =re.sub('[^0-9a-zA-Z ,]+', '', str(comm))
		#print 'comm[1]'
		#print comm[1]		
		ans = comm[1][7:]
		
	elif query_ques_l == 'which' or query_ques_l == 'who':
		for word in ques_split:
			if word == 'bowler' or word == 'bowled':
				ans = comm[1][0]
				found = 1
			elif word == 'batsman' or word == 'hit':
				ans = comm[1][2]
				found = 1
			elif word == 'over':
				ans = comm[0]
				found = 1		
		if found != 1:
			ans = comm[1]			
	else:
		ans = comm	
	
	return ans	

 ## assigns search keywords and question words
def parse_query():    
	
	global question
	global query_pos
	global query_ques
	global search_keywords
	
	flag=0
	
	for i in query_pos:
		if len(i)<4:
			if i[1] == 'WDT' or i[1] == 'WRB' or i[1] == 'WP' or i[1] == 'WP$' :
				query_ques = i[0]
				index_i = query_pos.index(i)
				flag=index_i
		
		if i[1] == 'NNP':
			if player == i[0] :
				for j in query_pos:
					if j[0] == 'match' or j[0] == 'MATCH':
						index_j = query_pos.index(j)
						search_keywords = query_pos[index_i+1:index_j]
	
	if len(search_keywords) <= 0:
		search_keywords = query_pos[flag+1:]	
	
	#print 'query_ques::'
	#print query_ques
	#print 'search_keywords::'
	#print search_keywords

def main():
	testcases =input()
	
	for turn in range(0,testcases):
		global parse_query
		global question
		global ques
		question =raw_input('\ninput\n')
		ques = question.split()
		india={}
		nz={}
		
		f3='./dataset/player_profile/indian_players_profile.txt'
		f4='./dataset/player_profile/nz_players_profile.txt'
		
		add_to_dict_player(india,f3)
		add_to_dict_player(nz,f4)
		
		#q1 =raw_input()
		
		pos_tag_ques()
		#print 'query_pos::'
		#print query_pos
		
		player_data = parse_for_player_data(india, nz)
		#print 'player_data::'
		#print player_data
		
		parse_for_match_no()
		#print 'match_number::'
		#print match_printnumber	
		
		parse_for_player_type()
		#print 'player_type::'
		#print player_type		

		
		parse_query()
		#print 'query_ques::'
		#print query_ques
		#print 'search_keywords::'
		#print search_keywords
		print '\nCase #'+ str(turn)
		print '\nselect commentary::'
		select_commentary(player_data)
		
		comm_line = search_commentary()

		ans = parse_for_ans(comm_line)
		
		print '\nans::'
		print ans
		print '\n\n'
		turn +=1
	
if __name__ == "__main__":
	main()

