####...... ASSUMPTIONS.....
# 1. over number given in query must be in digits not words
# 2. first letter of names of players must be capitalized

import nltk	
import sys
import re
import textblob
from textblob import TextBlob
import os
from nltk.util import ngrams

os.system('clear')

question=""
query_question=[]
query_desc=[]
comm =[]
parsed_query=[]
over = 'None'
min_max_constraints = 'None'
number_specification = 0
player_name = 'None'
query_country ='None'
pos_tagged_query = []

def add_to_dictionary_player(dictionary, fname):
	f = open(fname, 'r')
	for line in f:
		temp = line[:-1]
		temp = temp.split('\t')
		a=temp[0]
		#print a
		b=temp[1:]
		if a not in dictionary:
			dictionary[a] = b

def parse_commentary(file):
	
	commentary_file = open(file,'r')
	commentary_parse= []
	for line in commentary_file:
		temp1 = line[:-1]
		temp2 = temp1.split(' ')
		for i in range(0,len(temp2)):
			#print temp2[i]
			if (len(temp2[i]) !=0 ):
				temp2[i]=re.sub('[^0-9a-zA-Z .-]+', '', str(temp2[i]))
				#temp2[i]=re.sub('[.]+', '$', str(temp2[i]))

		commentary_parse.append(temp2) 
	
	return commentary_parse

def select_commentary_file(player_type, player_info, parsed_query):
	
	global comm
	global query_desc
	
	#print 'ques:'
	#print question
	#print player_info
	file1 = '../dataset/match'
	file2 = '../dataset/match'
	
	match = parse_for_match_no(parsed_query)
	match_number = re.sub('[ ]+', '', str(match))
	
	if(player_info != 'None'):
		
		player_country_data = player_info[3]
		country_temp = player_country_data.split(',')
		country1 = country_temp[0]
		country1 = re.sub('[ ]+', '', str(country1))
		query_country = country1.lower()

	else:
		
		query_temp = parsed_query.split('.')
		desc_temp = query_temp[1]
		query_desc = desc_temp.split (' ')
		
		for i in range(0,len(query_desc)):
			word = query_desc[i].lower()
			
			if word== 'india':
				query_country = 'india'
				
			elif word == 'new':
				next_word = query_desc[i+1]
				if next_word.lower() == 'zealand':
					query_country = 'newzealand'	
	
	if(query_country == 'india'):
		not_country = 'newzealand'
	else:
		not_country = 'india'	
	
	if(player_type!= 'None'):
		if(player_type == 'bowler'):
			file1 += str(match_number) + '/odi' + str(match_number)+ '_' +  str(not_country) + '_commentary.txt'	
		
		else:
			file1 += str(match_number) + '/odi' + str(match_number)+ '_' + str(query_country) + '_commentary.txt'
		
		#print 'file1'
		#print file1
		comm = parse_commentary(file1)
			
	else:
		
		file1 += str(match_number) + '/odi' + str(match_number)+ '_' + str(query_country) + '_commentary.txt'
		file2 += str(match_number) + '/odi' + str(match_number)+ '_' +  str(not_country) + '_commentary.txt'	
		
		#print 'file1 + file2'
		#print file1
		#print file2
		
		comm = parse_commentary(file1)
		comm = parse_commentary(file2)
		
	return comm				


def query_match_number_info():
	
	global question
	ques = question.split(' ')
	matchno="none"
	for q in range (0, len(ques)):
		
		if((ques[q]=='match,')or(ques[q]=='match.')or(ques[q]=='match')):
			
			if(((ques[q-1]=='first')or(ques[q-1]=='second')or(ques[q-1]=='third')or(ques[q-1]=='fourth')or(ques[q-1]=='fifth'))or((ques[q-1]=='one')or(ques[q-1]=='two')or(ques[q-1]=='three')or(ques[q-1]=='four')or(ques[q-1]=='five'))):
				
				matchno=ques[q-1]
				
			elif(((ques[q+1]=='first')or(ques[q+1]=='second')or(ques[q+1]=='third')or(ques[q+1]=='fourth')or(ques[q+1]=='fifth'))or((ques[q+1]=='one')or(ques[q+1]=='two')or(ques[q+1]=='three')or(ques[q+1]=='four')or(ques[q+1]=='five'))):	
				
				matchno=ques[q+1]
				
	#print "match_no"
	#print matchno
	return matchno

def parse_question():
	global parsed_query
	global question
	global pos_tagged_query
	global query_desc
	
	ques = re.sub('[^0-9a-zA-Z ]+', '', str(question))
	q = ques.split()
	pos_tagged_query = nltk.pos_tag(q)
	
	question=re.sub('[^0-9a-zA-Z ]+', '', str(question))
	q=question.split(' ')
	
	for i in range (0,len(q)):
		
		if((q[i]=='match,')or(q[i]=='match.')or(q[i]=='match')):
			#print 'inside'
			m_no=query_match_number_info()
			#print m_no
			qnew=q[i+1:]
			
		if((q[i]=='which')or(q[i]=='who')):
			
			#print "query_question"
			#print q[i:]
			query_question=q[i:]
			
			for k in range (0,len(qnew)):
				
				if((qnew[k]=='which')or(qnew[k]=='who')):
					
					qnew=qnew[:k]
					query_desc=qnew	
					#print "query_desc"
					#print query_desc
					parsed_query_desc =''
					parsed_query_question=''
					parsed_query=''
					parse_m_no= str(m_no)+' ' + '.'
					
					for elements in query_desc:
						parsed_query_desc = str(parsed_query_desc) +str(elements) +' ' 
					parsed_query_desc = parsed_query_desc[:-1]
					parsed_query_desc = str(parsed_query_desc) +'.'
					
					for elements in query_question:
						parsed_query_question = str(parsed_query_question) + str(elements) +' '
					
					parsed_query = str(parse_m_no) +str(parsed_query_desc) +str(parsed_query_question)
					
					parsed_query=re.sub('[^0-9a-zA-Z .]+', '', str(parsed_query))
					#print parsed_query
					return parsed_query
					break


def parse_for_match_no(player_info):
	
	data_temp1 = player_info.split('.')
	
	match1 = data_temp1[0]
	match2 = match1.lower()
	match = str(match2)
	match = re.sub('[ ]+','', str(match))
	
	
	if (match == 'one' or match == 'first'):
		return 1
	elif( match == 'two' or match == 'second'):
		return 2
	elif( match == 'three' or match == 'third'):
		return 3
	elif( match == 'four' or match == 'fourth'):
		return 4
	elif( match == 'five' or match == 'fifth'):
		return 5				


def parse_for_player_type(parsed_query):
	desc=parsed_query.split('.')
	desc=desc[1]
	query_desc=desc.split(' ')
	for i in query_desc:
		#print i
		if (i=='bowled'or i=='wickets' or i=='wicket' or i=='economy rate' or i=='no ball' or i=='no balls' or i=='wide' or i=='wides'):
			return 'bowler'
		
		elif (i=="four" or i=="six" or i=="strike rate" or i=='out' or i=='dismissed' or i=='fours' or i=='sixes' or i=='hit'):
			return 'batsman'


def parse_for_player_information(india, nz, ques_data):

	global player_name
	global query_country
	global over
	global query_desc
	over =''
	player_info = 'None'
	query_desc_string=''
	
	for i in query_desc:
		query_desc_string += str(i) + ' '
		
	query_desc_string = query_desc_string[:-1]
	
	unigram = ngrams(query_desc_string.split(), n=1)
	unigram_string = []
	for i in unigram :
		string = ''
		for j in i :
			string += str(j) + ' '
		string = string[:-1]
		unigram_string.append(string)
	
	bigram = ngrams(query_desc_string.split(), n=2)
	bigram_string = []
	for i in bigram :
		string = ''
		for j in i :
			string += str(j) + ' '
		string = string[:-1]
		bigram_string.append(string)
	
	for word in unigram_string:
		for key in nz :
			#print key
			name = key.split(' ')
			#print name[1]
			if  (word == name[1]):
				player_name = word
				query_country ='newzealand'
				player_info =nz[key]
	
	for word in bigram_string:
		for key in nz :
			if word == key :
				player_name = word
				query_country ='newzealand'
				player_info =nz[key]
	
	for word in unigram_string:
		for key in india :
			#print key
			name = key.split(' ')
			#print name[1]
			if  (word == name[1]):
				player_name = word
				query_country ='india'
				player_info =india[key]
			
	for word in bigram_string:
		for key in india :
			if word == key :
				player_name = word
				query_country ='india'
				player_info =india[key]
	
	for word in query_desc:
		if (str(word) == 'over' or str(word) == 'overs'):
			previous_tag =''
			next_ttag =''

			next_index = query_desc.index(word) +1
			if (next_index < len (query_desc)):
				next_word = query_desc[next_index]
				next_word = TextBlob(str(next_word))
				next_ttag = next_word.tags
				#print 'tag:'
				#print next_ttag
				temp = str(next_ttag[0]).split(', u')
				next_ttag=re.sub('[^0-9a-zA-Z]+', '', str(temp[1]))
				#print next_ttag
			
			prev_index = query_desc.index(word) -1
			if (prev_index > 0):
				prev_word = query_desc[prev_index]
				prev_word = TextBlob(str(prev_word))
				previous_tag = prev_word.tags
				#print 'tag:'
				#print previous_tag
				temp = str(previous_tag[0]).split(', u')
				previous_tag=re.sub('[^0-9a-zA-Z]+', '', str(temp[1]))
				#print next_ttag
				
			if next_ttag=='CD' or previous_tag == 'LS' or str(next_word) == '2' or str(next_word) == '4':
				over = str(next_word)

			if previous_tag == 'CD' or previous_tag == 'LS' or str(prev_word) == '2' or str(prev_word) == '4':
				over = str(prev_word)
			
	return player_info

						
def answer_for_case(parsed_query,player_info):
	query =parsed_query.split('.')
	#print query
	temp_info = query[0]
	temp_desc = query[1]
	temp_ques = query[2]
	info = temp_info.split(' ')
	desc = temp_desc.split(' ')
	ques = temp_ques.split(' ')
	case=0
	
	for word1 in desc:
		word_l =word1.lower()
		#print 'word'
		#print word_l
		if word_l =='hit' or  word_l =='hits' or word_l =='stroke':
			desc_case =1
			break
			
		elif word_l =='over' or word_l =='ball' or word_l =='overs' or word_l =='balls' :
			desc_case =2
			break
			
		elif word_l == 'out' or  word_l =='dismissed' or word_l == 'OUT' :
			desc_case =3
			break
			
		elif word_l == 'bowled'  or word_l =='no' or word_l =='wide' or word_l =='wides' :
			desc_case= 4
			break


	for word1 in ques:
		word1_l = word1.lower()
		word1_l=re.sub('[^0-9a-zA-Z]+', '', str(word1_l))
		
		#print word1_l
		if word1_l =='ball' or word1_l =='balls' or word1_l =='ball(s)':
			ques_case ='a'
			break
		if word1_l =='over' or word1_l =='overs' or word1_l =='over(s)' :
			ques_case ='b'
			break
		if word1_l =='dismissed' or word1_l =='dismiss' or word1_l =='dismissed(s)':
			ques_case ='c'
			break
		if word1_l == 'hit' or word1_l == 'hits' or word1_l == 'hit(s)' :
			ques_case='d'
			break
		if word1_l == 'bowler' or word1_l == 'bowlers' or word1_l == 'bowler(s)' :
			ques_case='e'
			break

	case =str(desc_case) +' '+ str(ques_case)
	
	return case

def answer_for_desc(desc_case,commentary_parse):

	ans= []
	global parsed_query
	no_type = 'None'
	
	query =parsed_query.split('.')
	temp_info = query[0]
	temp_desc = query[1]
	temp_ques = query[2]
	info = temp_info.split(' ')
	desc = temp_desc.split(' ')
	ques = temp_ques.split(' ')
	
	number_specification = 0
	min_max_constraints = 'None'
	runs=''

	if (desc_case == '1'):
		for i in range(0, len(desc)):
			word = desc[i].upper()
			if (str(word) == 'ONE') or (str(word) == 'FOUR') or (str(word) == 'SIX') or (str(word) == 'TWO') or (str(word) == 'ONES')or (str(word) == 'SIXES')or (str(word) == 'FOURS')or (str(word) == 'TWOS'):
				
				if (str(word) == 'ONE') or (str(word) == 'ONES'):
					runs = 'ONE'
				if (str(word) == 'TWO') or (str(word) == 'TWOS'):
					runs = 'TWO'
				if (str(word) == 'FOUR') or (str(word) == 'FOURS'):
					runs ='FOUR'
				if (str(word) == 'SIX') or (str(word) == 'SIXES'):
					runs ='SIX'
				prev = re.sub('[^0-9]+', ' ', str(desc[i-1]))
		
				if(prev != ' '):
					number_specification = desc[i-1]
					
		if(number_specification==0):
			for j in desc:
				i = j.upper()
				if(i == 'MAX' or i == 'MAXIMUM' ):
					min_max_constraints = 'MAX'		
				if(i == 'MIN' or i == 'MINIMUM'):	
					min_max_constraints = 'MIN'
		
		if (number_specification != 0):
			parsed_query = parsed_query + str('.') + number_specification	
		elif(min_max_constraints != 'None'):
			parsed_query = parsed_query + str('.') + min_max_constraints		
		
			
		for line in commentary_parse:
			j=0
			for word in line:
				prev_word_index = line.index(word) -1
				prev_word = line[prev_word_index]
				prev_word_u = prev_word.upper()
				if (str(word) == player_name and prev_word_u == 'TO') and j<5:
					i=0
					
					for word3 in line:
						word2=word3.upper()
						
						word2 = re.sub('[^A-Za-z]+', '', str(word2))
						
						if (str(word2) == str(runs)) and (i<5):
							prev_index = commentary_parse.index(line) -1
							line_prev = commentary_parse[prev_index]
							ans.append(line_prev)
							ans.append(line)
													
							break
						i +=1
					break	
				j+=1

	if (desc_case == '2'):

		for i in range(0, len(desc)):
			word = desc[i].upper()
			if (str(word) == 'OVER' or str(word) == 'OVERS'or str(word) =='OVER(S)'):
				
				prev = re.sub('[^0-9]+', ' ', str(desc[i-1]))
		
				if(prev != ' '):
					number_specification = desc[i-1]
					
		if(number_specification==0):
			for j in desc:
				i = j.upper()
				if(i == 'MAX' or i == 'MAXIMUM' ):
					min_max_constraints = 'MAX'		
				if(i == 'MIN' or i == 'MINIMUM'):	
					min_max_constraints = 'MIN'		
		if (number_specification != 0):
			parsed_query = parsed_query + str('.') + number_specification	
		elif(min_max_constraints != 'None'):
			parsed_query = parsed_query + str('.') + min_max_constraints


		for line in commentary_parse:
			j=0
			for word in line:
				prev_word_index = line.index(word) -1
				prev_word = line[prev_word_index]
				prev_word_l = prev_word.lower()
				if (str(word) == player_name and prev_word_l == 'to') and j<5:
					i=0
					for word2 in line:
						if (str(word2) == 'over' or  str(word2) =='overs' or str(word2) == 'over(s)') and (i<5):
							prev_index = commentary_parse.index(line) -1
							line_prev = commentary_parse[prev_index]
							ans.append(line_prev)
							ans.append(line)
							print line
							break
						i+=1
					break
				j+=1

	if (desc_case == '3'):
		for i in range(0, len(desc)):
			word = desc[i].upper()
			if (str(word) == 'OUT' or str(word) == 'DISMISSED'):
				
				prev = re.sub('[^0-9]+', ' ', str(desc[i-1]))
		
				if(prev != ' '):
					number_specification = desc[i-1]
					
		if(number_specification==0):
			for j in desc:
				i = j.upper()
				if(i == 'MAX' or i == 'MAXIMUM' ):
					min_max_constraints = 'MAX'		
				if(i == 'MIN' or i == 'MINIMUM'):	
					min_max_constraints = 'MIN'		
		if (number_specification != 0):
			parsed_query = parsed_query + str('.') + number_specification	
		elif(min_max_constraints != 'None'):
			parsed_query = parsed_query + str('.') + min_max_constraints


		for line in commentary_parse:
			j=0
			for word in line:
				prev_word_index = line.index(word) -1
				prev_word = line[prev_word_index]
				prev_word_l = prev_word.lower()
				if (str(word) == player_name and prev_word_l == 'to') and j<5:
					i=0
					for word2 in line:
						if (str(word2) == 'out' or  str(word2) =='dismissed' or str(word2) == 'OUT') and (i<7):
							prev_index = commentary_parse.index(line) -1
							line_prev = commentary_parse[prev_index]
							ans.append(line_prev)
							ans.append(line)
							#print line
							break
						i+=1
					break
				j+=1
						
			

	if (desc_case == '4'):

		for i in range(0, len(desc)):
			word = desc[i].upper()
			if (str(word) == 'WIDE' or str(word) == 'WIDES' or str(word) == 'NO'):
				
				if(str(word)== 'NO'):
					extra = 'no'
					if desc[i+1].upper == 'RUN' or desc[i+1].upper() == 'RUNS':
						no_type = 'run'
					elif desc[i+1].upper == 'BALL' or desc[i+1].upper() == 'BALLS':
						no_type = 'ball'
				else :
					extra = 'wide'
				prev = re.sub('[^0-9]+', ' ', str(desc[i-1]))
		
				if(prev != ' '):
					number_specification = desc[i-1]
					
		if(number_specification==0):
			for j in desc:
				i = j.upper()
				if(i == 'MAX' or i == 'MAXIMUM' ):
					min_max_constraints = 'MAX'		
				if(i == 'MIN' or i == 'MINIMUM'):	
					min_max_constraints = 'MIN'		
		if (number_specification != 0):
			parsed_query = parsed_query + str('.') + number_specification	
		elif(min_max_constraints != 'None'):
			parsed_query = parsed_query + str('.') + min_max_constraints

		#print parsed_query
		for line in commentary_parse:
			
			#include the code for (n)wides as well ,this is calculating just wides..question can be of the form 2 wides or so 
			j=0
			for word in line:
				next_word_index = line.index(word) +1
				if  len(line) > next_word_index:
					next_word = line[next_word_index]
					next_word_l = next_word.lower()
					if (str(word) == player_name and next_word_l == 'to') and j<5:
					
						i=0
						for word1 in line:
							word2 = word1.lower()
							
							next_word_index2 = line.index(word1) +1
							if  len(line) > next_word_index2:
								next_word2 = line[next_word_index2]
								next_word2l = next_word2.lower()
								# word2
								if (str(word2) == 'no')  and (str(next_word2l)== no_type) and (i<5) and (extra =='no'):
									#print 'wide/no'
									next_index = commentary_parse.index(line) -1
									line_next = commentary_parse[next_index]
									ans.append(line_next)
									ans.append(line)
									#print line
								
								
								elif( str(word2) == 'wide' or  str(word2) =='wides' )  and (i<5) and (extra == 'wide'):
									#print 'wide/no'
									next_index = commentary_parse.index(line) -1
									line_next = commentary_parse[next_index]
									ans.append(line_next)
									ans.append(line)
									#print line
								i+=1
						break
					j+=1
					
	return ans

def answer_for_ques(ques_case,commentary_parse,ans_desc,parsed_query):
	
	ans =[]
	dictionary ={}
	global over
	global min_max_constraints
	global number_specification
	
	temp_extra = parsed_query.split('.')
	if(len(temp_extra)>3):
		if temp_extra[3].isdigit():
			number_specification = temp_extra[3]
		else:
			min_max_constraints = temp_extra[3]	
	
	if(ques_case == 'a'):
		
		if len(over) >0:
			for line in ans_desc:
				if(str(line[0][0]).isdigit() == True):
					overs = str(line[0]).split('.')
					
					if overs[0] != over:
						index = ans_desc.index(line)
						ans_desc.remove(ans_desc[index])
						ans_desc.remove(ans_desc[index-1])
		
		for line in ans_desc:
			if(str(line[0][0]).isdigit() == True):
				overs = str(line[0]).split('.')
				ans.append(overs[1])

	if(ques_case == 'b'):
		
		if(number_specification !=0):
			#print number_specification
			for line in ans_desc:
				t=str(line[0][0])
				if t.isdigit() :
					
					over_temp = line[0].split('.')
					over = over_temp [0]
					#print over
					if over not in dictionary:
						dictionary[over] = 1
					else:
						dictionary[over] += 1
			
			#print 'DICTIONARY'
			#print dictionary
			for key in dictionary:
				if int(dictionary[key]) == int(number_specification) :
					ans.append(key)		
		
		elif(min_max_constraints != 'None'):
			
			#print min_max_constraints
			for line in ans_desc:
				t=str(line[0][0])
				if t.isdigit() :
					
					over_temp = line[0].split('.')
					over = over_temp [0]
					#print over
					if over not in dictionary:
						dictionary[over] = 1
					else:
						dictionary[over] += 1
					
			
			if(min_max_constraints == 'MAX'):
					max_val = 1
					for key in dictionary:
						if dictionary[key] > max_val :
							max_val = dictionary[key]
							
					for key in dictionary:
						if dictionary[key] >= max_val:
							ans.append(key)	
						
			else:
				min_val = 100
				for key in dictionary:
					if dictionary[key] < min_val :
						min_val = dictionary[key]
							
				for key in dictionary:
					if dictionary[key] <= min_val:
						ans.append(key)	
				#print min_val
				 				
		else:
			
			for line in ans_desc:
				if(str(line[0][0]).isdigit() == True):
					overs = str(line[0]).split('.')
					ans.append(overs[0])
					

	if(ques_case == 'c'):
		
		
		if len(over) >0:
			#print over + '.'
			for line in ans_desc:
				if(str(line[0][0]).isdigit() == True):
					overs = str(line[0]).split('.')
					
					if overs[0] != over:
						index = ans_desc.index(line)
						ans_desc.remove(ans_desc[index])
						ans_desc.remove(ans_desc[index-1])
		
		if(number_specification !=0):
			for line in ans_desc:
				if len(line) > 1:
					last_name = ''
					first_name =''
					for word in line:
						temp = str(word).upper()
						prev_index = line.index(word) -1
						if( temp== 'TO'):
							
							bowler = line[0:prev_index+1]
							
							first_name = bowler[0]

							if len (bowler) == 2:	
								last_name = bowler[1]
							if last_name != '':
								name = first_name + ' ' +last_name
							else:
								name = first_name
							
							if name not in dictionary:
								dictionary[name] = 1
							else:
								dictionary[name] += 1
							break
			
			#print 'DICTIONARY'
			#print dictionary
			for key in dictionary:
				if int(dictionary[key]) == int(number_specification) :
					ans.append(key)		
		
		
		elif(min_max_constraints != 'None'):
			
			for line in ans_desc:
				if len(line) > 1:
					last_name = ''
					first_name =''
					for word in line:
						temp = str(word).upper()
						prev_index = line.index(word) -1
						if( temp== 'TO'):
							bowler = line[0:prev_index+1]
							
							first_name = bowler[0]

							if len (bowler) == 2:	
								last_name = bowler[1]
							
							if last_name != '':
								name = first_name + ' ' + last_name
							else:
								name = first_name

							if name not in dictionary:
								dictionary[name] = 1
							else:
								dictionary[name] += 1

							break
						
			if(min_max_constraints == 'MAX'):
				max_val = 1
				for key in dictionary:
					if dictionary[key] > max_val :
						max_val = dictionary[key]
									
				for key in dictionary:
					if dictionary[key] >= max_val:
						ans.append(key)	
			else:
				min_val = 100	
				for key in dictionary:
					#print key
					#print dictionary[key]
					if dictionary[key] < min_val :
						min_val = dictionary[key]
									
				for key in dictionary:
					if dictionary[key] <= min_val:
						ans.append(key)
				
				
		else:
			for line in ans_desc:
				if len(line) > 1:
					for word in line:
						temp = str(word).upper()
						prev_index = line.index(word) -1
						if( temp== 'TO'):
							#print 'temp'
							#print temp
							bowler = line[prev_index]
							#print bowler

							ans.append(line[0:prev_index+1])
							break	

	if(ques_case == 'd'):
		
		
		if len(over) >0:
			#print over + '.'
			for line in ans_desc:
				if(str(line[0][0]).isdigit() == True):
					overs = str(line[0]).split('.')
					if overs[0] != over:
						index = ans_desc.index(line)
						ans_desc.remove(ans_desc[index])
						ans_desc.remove(ans_desc[index-1])
		
		if(number_specification !=0):
			for line in ans_desc:
				if len(line) > 1:
					last_name = ''
					first_name =''
					for word in line:
						temp = str(word).upper()
						next_index = line.index(word) +1
						if( temp== 'TO'):
							
							batsman = line[next_index]
							
							first_name = batsman

							if len (batsman) == 2:	
								last_name = batsman[1]
							if last_name != '':
								name = first_name + ' ' +last_name
							else:
								name = first_name
							
							#print 'line ::' + str(line)
							#print 'name :: ' + name
							
							if name not in dictionary:
								dictionary[name] = 1
							else:
								dictionary[name] += 1
							break
			
			#print 'DICTIONARY'
			#print dictionary
			for key in dictionary:
				if int(dictionary[key]) == int(number_specification) :
					ans.append(key)		
		
		
		elif(min_max_constraints != 'None'):
			
			for line in ans_desc:
				if len(line) > 1:
					last_name = ''
					first_name =''
					for word in line:
						temp = str(word).upper()
						next_index = line.index(word) +1
						if( temp== 'TO'):
							batsman = line[next_index]
							
							first_name = batsman

							if len (batsman) == 2:	
								last_name = batsman[1]
							
							if last_name != '':
								name = first_name + ' ' + last_name
							else:
								name = first_name

							if name not in dictionary:
								dictionary[name] = 1
							else:
								dictionary[name] += 1

							break
						
			if(min_max_constraints == 'MAX'):
				max_val = 1
				for key in dictionary:
					if dictionary[key] > max_val :
						max_val = dictionary[key]
									
				for key in dictionary:
					if dictionary[key] >= max_val:
						ans.append(key)	
			else:
				min_val = 100	
				for key in dictionary:
					if dictionary[key] < min_val :
						min_val = dictionary[key]
									
				for key in dictionary:
					if dictionary[key] <= min_val:
						ans.append(key)
				
				
		else:
			for line in ans_desc:
				if len(line) > 1:
					for word in line:
						temp = str(word).upper()
						next_index = line.index(word) +1
						if( temp== 'TO'):
							#print 'temp'
							#print temp
							batsman = line[next_index]
							#print batsman

							ans.append(line[next_index])
							break

	if(ques_case == 'e'):
		
		if len(over) >0:

			#print over + '.'
			for line in ans_desc:
				if(str(line[0][0]).isdigit() == True):
					overs = str(line[0]).split('.')
					if overs[0] != over:
						index = ans_desc.index(line)
						ans_desc.remove(ans_desc[index])
						ans_desc.remove(ans_desc[index-1])
		
		if(number_specification !=0):
			for line in ans_desc:
				if len(line) > 1:
					last_name = ''
					first_name =''
					for word in line:
						temp = str(word).upper()
						prev_index = line.index(word) -1
						if( temp== 'TO'):
							bowler = line[0:prev_index+1]
							
							first_name = bowler[0]

							if len (bowler) == 2:	
								last_name = bowler[1]
							if last_name != '':
								name = first_name + ' ' +last_name
							else:
								name = first_name
							
							#print 'line ::' + str(line)
							#print 'name :: ' + name
							
							if name not in dictionary:
								dictionary[name] = 1
							else:
								dictionary[name] += 1
							break
			
			#print 'DICTIONARY'
			#print dictionary
			for key in dictionary:
				if int(dictionary[key]) == int(number_specification) :
					ans.append(key)		
		
		
		elif(min_max_constraints != 'None'):
			
			for line in ans_desc:
				if len(line) > 1:
					last_name = ''
					first_name =''
					for word in line:
						temp = str(word).upper()
						prev_index = line.index(word) -1
						if( temp== 'TO'):
							bowler = line[0:prev_index+1]
							
							first_name = bowler[0]

							if len (bowler) == 2:	
								last_name = bowler[1]
							
							if last_name != '':
								name = first_name + ' ' + last_name
							else:
								name = first_name

							if name not in dictionary:
								dictionary[name] = 1
							else:
								dictionary[name] += 1

							break
						
			if(min_max_constraints == 'MAX'):
				max_val = 1
				for key in dictionary:
					if dictionary[key] > max_val :
						max_val = dictionary[key]
									
				for key in dictionary:
					if dictionary[key] >= max_val:
						ans.append(key)	
			else:
				min_val = 100	
				for key in dictionary:
					if dictionary[key] < min_val :
						min_val = dictionary[key]
									
				for key in dictionary:
					if dictionary[key] <= min_val:
						ans.append(key)
				
				
		else:
			for line in ans_desc:
				if len(line) > 1:
					for word in line:
						temp = str(word).upper()
						prev_index = line.index(word) -1
						if( temp== 'TO'):
							#print 'temp'
							#print temp
							bowler = line[prev_index]
							#print bowler

							ans.append(line[0:prev_index+1])
							break

					
	return ans

def main():
	testcases =input()
	
	for turn in range(0,testcases):
		global parsed_query
		global question

		#question="in fourth match Ashwin bowled maximum no balls in which over?"
		question = raw_input('\ninput (following grammar) \n<full question> : <info about match> <description> <question>\n')	

		f3='../dataset/player_profile/indian_players_profile.txt'
		f4='../dataset/player_profile/nz_players_profile.txt'

		india={}
		nz={}

		add_to_dictionary_player(india,f3)
		add_to_dictionary_player(nz,f4)

		parsed_query=parse_question()


		match_number=parse_for_match_no(parsed_query)
		#print 'match_number::'
		#print match_number

		player_info =parse_for_player_information(india, nz, parsed_query)
		#print 'player_info::'
		#print player_info

		player_type= parse_for_player_type(parsed_query)


		#print 'player_type::'
		#print player_type

		#print 'player_name::'
		#print player_name
		#print 'query_country::'
		#print query_country
		#print 'over::'
		#print over

		comm = select_commentary_file(player_type, player_info , parsed_query)

		cases = answer_for_case(parsed_query ,player_info)
		#print player_info
		#print 'case::'
		#print cases

		case =cases.split(' ')
		desc_case = case[0]
		ques_case = case[1]

		print '\nCase #'+ str(turn)

		ans_desc = answer_for_desc(desc_case,comm)
		print '\nans_desc::'
		print ans_desc
				
		print '\nparsed_query::'
		print parsed_query

		ans_ques = answer_for_ques(ques_case,comm,ans_desc,parsed_query)
		print '\nans_ques::'
		print ans_ques
		print '\n\n'
		
		turn +=1
	
if __name__ == "__main__":
	main()
