import nltk	
import sys
import os
import re
import textblob
from textblob import TextBlob
from nltk.util import ngrams

os.system('clear')
# function to add the contents of file, after proper parsing, to the given dictionary

#database =['player of match','player of winning team','losing side','duck','strike rate of player is above 200','more sixes than four','winning side','at least 1 boundary','strike rate was below 100','scored more than 50 runs','atleast 1 wicket','bowled more than 7 overs','failed to get any wicket','did not claim any wicket','more than 8 runs per','scored more than hundred','the team lost','less than 26 years old']
database = {'player of match':'mom','player of winning team':'win','losing side':'loss','duck':'duck','strike rate of player is above 200.0':'strike_gt_200','more six than four':'six_gt_four','winning side':'win','at least 1 boundary':'boundary_gt_0','strike rate was below 100':'strike_lt_100','scored more than 50 run':'runs_gt_50','at least 1 wicket':'wicket_gt_0','bowled more than 7 over':'over_gt_7','failed to get any wicket':'wicket_lt_0','did not claim any wicket':'wicket_lt_0','more than 8 run per':'rpo_gt_8','scored hundred':'runs_gt_100','the team lost':'loss','less than 26 year old':'age_lt_26'}
#print database

quantifier =''
quantified =''
predicate1 =''
predicate2 =''
connector  =''

def add_to_dict_mom(dictionary, fname):
	f = open(fname, 'r')
	for line in f:
		temp = line[:-1]
		temp = temp.split(',')
		a = fname[-5] + str (',') + temp[0]
		b = temp[1:]
		if a not in dictionary:
			dictionary[a] = b

def add_to_dict_win_team(dictionary, fname):
	f = open(fname, 'r')
	for line in f:
		temp = line[:-1]
		temp = temp.split(',')
		a = fname[-18]
		b = temp[0:]
		if a not in dictionary:
			dictionary[a] = b

def add_to_dict_batting_stats(dictionary, fname):
	f = open(fname, 'r')
	for line in f:
		temp = line[:-1]
		temp = temp.split(',')
		a = fname[-14] + str (',') + temp[0]
		b = temp[1:]
		if a not in dictionary:
			dictionary[a] = b

def add_to_dict_bowling_stats(dictionary, fname):
	f = open(fname, 'r')
	for line in f:
		temp = line[:-1]
		temp = temp.split(',')
		a = fname[-15] + str (',') + temp[0]
		b = temp[1:]
		if a not in dictionary:
			dictionary[a] = b
			
def add_to_dict_player_details(dictionary, fname):
	f = open(fname, 'r')
	for line in f:
		temp = line[:-1]
		temp = temp.split('\t')
		if (str(fname[-21]) == 'n'):
			country = 'India'
		else: 
			country = 'New Zealand'
		a = temp[0] + str(',') + country 
		b = temp[1:]
		if a not in dictionary:
			dictionary[a] = b

#expects mom dict as input
def parse_for_mom(match):
	toreturn  = []

	# man of match is in 1st column
	for i in match:
		temp = match[i]
		k = (temp[0])
		toreturn.append(i + str(',') + str(k))
	return toreturn

#expects winning team dict
def parse_for_win(match):
	toreturn  = []

	for i in match:
		temp = match[i]
		k = (temp[0])
		if (k != 'Tied'):
			toreturn.append(i + str(',') + str(k))
		else:
			toreturn.append(i + str(',') + "India")
			toreturn.append(i + str(',') + "New Zealand")
	return toreturn

#expects batting stats dict
def parse_for_duck(bat):
	toreturn  = []
	
	for i in bat:
		temp = bat[i]
		k = int(temp[1])
		t= temp[0]
		if ((k ==0) & (t!= 'not out')):
			x= temp[-1]
			toreturn.append(i+str(',')+x)
	return toreturn

#expects batting stats dict
def parse_for_strike_gt_200(bat):
	toreturn = []

	# strike rate is in the 7th column
	for i in bat:
		temp = bat[i]
		k = float(temp[6])
		if k > 200.0:
			x= temp[7]
			toreturn.append(i+str(',')+x)
	return  toreturn

#expects batting stats dict
def parse_for_six_gt_four(bat):
	toreturn  = []

	# number of six hit are in 6th column
	for i in bat:
		temp = bat[i]
		k = int(temp[5])
		f = int(temp[4])
		if k > f:
			x= temp[-1]
			toreturn.append(i+str(',')+x)
	return toreturn

#expects batting stats dict
def parse_for_boundary_gt_0(bat):
	toreturn  = []
	
	for i in bat:
		temp = bat[i]
		k = int(temp[4])
		f = float(temp[6])
		if ( (k !=0)  ):
			x= temp[-1]
			toreturn.append(i+str(',')+x)
	return toreturn
	
#expects batting stats dict
def parse_for_strike_lt_100(bat):
	toreturn  = []
	
	for i in bat:
		temp = bat[i]
		k = int(temp[4])
		f = float(temp[6])
		if (  (f<100.0) ):
			x= temp[-1]
			toreturn.append(i+str(',')+x)
	return toreturn
	
#expects batting stats dict
def parse_for_runs_gt_50(bat):
	toreturn  = []

	# number of six hit are in 6th column
	for i in bat:
		temp = bat[i]
		k = int(temp[1])
		if k > 50:
			x= temp[-1]
			toreturn.append(i+str(',')+x)
	return toreturn

#expects batting stats dict
def parse_for_runs_gt_100(bat):
	toreturn  = []
	
	for i in bat:
		temp = bat[i]
		k = int(temp[1])
		f = float(temp[6])
		if ( k > 100 ):
			x= temp[-1]
			toreturn.append(i+str(',')+x)
	return toreturn
	
#expects bowling stats dict
def parse_for_wicket_gt_0(bowl):
	toreturn  = []
	
	for i in bowl:
		temp = bowl[i]
		k = int(temp[3])
		if k > 0:
			x= temp[-1]
			toreturn.append(i+str(',')+x)
	return toreturn

#expects bowling stats dict
def parse_for_wicket_lt_0(bowl):
	toreturn  = []
	
	for i in bowl:
		temp = bowl[i]
		k = int(temp[3])
		j = float(temp[0])
		if (k <= 0) :
			x= temp[-1]
			toreturn.append(i+str(',')+x)
	return toreturn
	
#expects bowling stats dict
def parse_for_overs_gt_7(bowl):
	toreturn  = []
	
	for i in bowl:
		temp = bowl[i]
		k = int(temp[3])
		j = float(temp[0])
		if  (j>7):
			x= temp[-1]
			toreturn.append(i+str(',')+x)
	return toreturn

#expects bowling stats dict
def parse_for_rpo_gt_8(bowl):
	toreturn  = []
	
	for i in bowl:
		temp = bowl[i]
		k = int(temp[3])
		j = float(temp[4])
		if (j>8.0):
			x= temp[6]
			toreturn.append(i+str(',')+x)
	return toreturn

#expects bowling stats dict
def parse_for_age_lt_26(player):
	toreturn  = []
	
	for i in player:
		temp = player[i]
		j = str(temp[2])
		k = j.split(' ');
		age = int(k[0])
		#print 'age::'
		#print age
		if (age < 26):
			key=i.split(',')
			toreturn.append(key[1]+str(',')+key[0])
		
	return toreturn

def query_generation():
	global quantifier
	global quantified
	global predicate1
	global predicate2
	global connector
	query = ''
	#qunatifiers
	if quantifier == 'for all':
		query += "all"
	else :
		query += "exists"

	element =[]
	q=['m','c','p']

	#quantified elements
	if quantified == 'match' or quantified == 'innings' or quantified == 'inning':
		query += ' m.'
		element.append('m')
	elif quantified == 'country':
		query += ' c.'
		element.append('c')
	elif quantified == 'player':
		query += ' p.'
		element.append('p')

	for i in q:
		if i not in element:
			query +='exists ' +str(i) +'1'+'.'
			query +='exists ' +str(i) +'2'+'.'
	
	query +='('
	
	#predicate 1
	if len(predicate1) > 0:
		if (predicate1 == 'loss' or predicate1 == 'win'):
			query += str(predicate1) +'('
			if 'm' in element:
				query += 'm,'
			else:
				query += 'm1,'

			if 'c' in element:
				query += 'c,'
			else:
				query += 'c1,'

			query = query[:-1]
			query += ')'
		
		elif (predicate1 == 'age_lt_26'):
			query += str(predicate1) +'('
			if 'c' in element:
				query += 'c,'
			else:
				query += 'c1,'

			if 'p' in element:
				query += 'p,'
			else:
				query += 'p1,'

			query = query[:-1]
			query += ')'
		
		else:
			query += str(predicate1) +'('
			if 'm' in element:
				query += 'm,'
			else:
				query += 'm1,'

			if 'c' in element:
				query += 'c,'
			else:
				query += 'c1,'

			if 'p' in element:
				query += 'p,'
			else:
				query += 'p1,'

			query = query[:-1]
			query += ')'
	
	
	#connector
	query += ' '

	if connector == 'and':
		query += '& '
	else:
		query += '=> '

	#predicate 2
	if len(predicate2) > 0:
		#print predicate2
		if (predicate2 == 'loss' or predicate2 == 'win'):
			query += str(predicate2) +'('
			if 'm' in element:
				query += 'm,'
			else:
				query += 'm2,'

			if 'c' in element:
				query += 'c,'
			else:
				query += 'c2,'

			query = query[:-1]
			query += ')'
		
		elif (predicate2 == 'age_lt_26'):
			query += str(predicate2) +'('
			if 'c' in element:
				query += 'c,'
			else:
				query += 'c2,'

			if 'p' in element:
				query += 'p,'
			else:
				query += 'p2,'

			query = query[:-1]
			query += ')'
		
		else:
			query += str(predicate2) +'('
			if 'm' in element:
				query += 'm,'
			else:
				query += 'm2,'

			if 'c' in element:
				query += 'c,'
			else:
				query += 'c2,'

			if 'p' in element:
				query += 'p,'
			else:
				query += 'p2,'

			query = query[:-1]
			query += ')'
	
		query += ")"

	return query
# the function to make the model and answer the query, given the properly formatted strings
def make_model_and_answer(v,query):
	global quantifier
	global quantified
	global predicate1
	global predicate2
	global connector

	l = nltk.LogicParser()

	val = nltk.parse_valuation(v)
	#print 'val:'
	#print val
	#print 'end val:'
	
	dom = val.domain
	#print 'dom:'
	#print dom
	#print 'end dom:'
	
	model = nltk.Model(dom, val)
	#print 'model:'
	#print m
	#print 'end m:'
	
	g = nltk.Assignment(dom, [])
	
	
	temp = l.parse('match(x)')
	m =  model.satisfiers(temp, 'x', g)
	temp = l.parse('match(x)')
	m1 =  model.satisfiers(temp, 'x', g)
	temp = l.parse('match(x)')
	m2 =  model.satisfiers(temp, 'x', g)
	#print match
	
	temp = l.parse('country(x)')
	c  =  model.satisfiers(temp, 'x', g)
	temp = l.parse('country(x)')
	c1 =  model.satisfiers(temp, 'x', g)
	temp = l.parse('country(x)')
	c2 =  model.satisfiers(temp, 'x', g)
	#print country

	temp = l.parse('player(x)')
	p =  model.satisfiers(temp, 'x', g)
	temp = l.parse('player(x)')
	p1 =  model.satisfiers(temp, 'x', g)
	temp = l.parse('player(x)')
	p2 =  model.satisfiers(temp, 'x', g)
	#print player
	
	#query formation
	#query = 'all m.exists c1.exists c2.exists p1.exists p2.(mom(m,c1,p1) => win(m,c2))'
	
	print "The anwer for the query is : ",
	print model.evaluate(query, g)

# 	the function to 
#	1. generate the appropriate Model, after getting the values of the required predicates;
#	2. construct the query 
#	3. to prove/disprove the query.
def generate_and_solve_query(mom_dict,win_dict,bat_dict,bowl_dict,player_dict):
	
	mom = parse_for_mom(mom_dict)
	win = parse_for_win(win_dict)
	duck = parse_for_duck(bat_dict)
	strike_gt_200 = parse_for_strike_gt_200(bat_dict)
	six_gt_four = parse_for_six_gt_four(bat_dict)
	boundary_gt_0 = parse_for_boundary_gt_0(bat_dict)
	strike_lt_100 = parse_for_strike_lt_100(bat_dict)
	runs_gt_50 = parse_for_runs_gt_50(bat_dict)
	runs_gt_100 = parse_for_runs_gt_100(bat_dict)
	wicket_gt_0 = parse_for_wicket_gt_0(bowl_dict)
	wicket_lt_0 = parse_for_wicket_lt_0(bowl_dict)
	over_gt_7 = parse_for_overs_gt_7(bowl_dict)
	rpo_gt_8 = parse_for_rpo_gt_8(bowl_dict)
	age_lt_26 = parse_for_age_lt_26(player_dict)

	'''
	print 'mom::'
	print mom
	print 'win::'
	print win
	print 'duck::'
	print duck
	print 'strike_gt_200::'
	print strike_gt_200
	print 'six_gt_four::'
	print six_gt_four
	print 'boundary_gt_0 ::'
	print boundary_gt_0 
	print 'strike_lt_100::'
	print strike_lt_100
	print 'runs_gt_50::'
	print runs_gt_50
	print 'runs_gt_100::'
	print runs_gt_100
	print 'wicket_gt_0::'
	print wicket_gt_0
	print 'wicket_lt_0::'
	print wicket_lt_0
	print 'over_gt_7::'
	print over_gt_7
	print 'rpo_gt_8::'
	print rpo_gt_8
	print 'age_lt_26::'
	print age_lt_26
	'''
	#Now constructing strings which are needed to create the model:
	
	name_to_var={'New Zealand': 'NZ','India': 'IN','Tied' : 'NO' ,'1':'odi1','2':'odi2','3':'odi3','4':'odi4','5':'odi5'}
	name_to_var2={'New Zealand': 'IN','India': 'NZ','Tied' : 'NO' ,'1':'odi1','2':'odi2','3':'odi3','4':'odi4','5':'odi5'}
	count = 0
	for i in player_dict:
		t1=i.split(',')
		j=t1[0]
		if j not in name_to_var:
			name_to_var[j] = 'r' + str(count)
			count += 1
	
	
	#print name_to_var
	#print name_to_var2
	
	# Now for creating a Model, we need to write down a string which shows mapping from predicates to varible names
	temp_strin1 = ''
	for i in name_to_var:
		temp_strin1 += i + ' => ' + name_to_var[i] + '\n'
	#print temp_strin1
	
	
	# this is for the predicate "mom"
	temp_strin2 = 'mom => {'
	count = 1
	for i in mom:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin2 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin2 = temp_strin2[:-1]  #removing the extra "," character
	temp_strin2 += '} \n'
	#print temp_strin2
	
	#now for the predicate "win"
	temp_strin3 = 'win => {'
	for i in win:
		t1= i.split(',')
		m_no = t1[0]
		co_nm = t1[1]
		temp_strin3 +='(' + name_to_var[m_no] + ',' + name_to_var[co_nm] +  '),'

	temp_strin3 = temp_strin3[:-1]  #removing the extra "," charater
	temp_strin3 += '}\n'
	
	#print temp_strin3
	
	temp_strin4 = 'loss => {'
	for i in win:
		t1= i.split(',')
		m_no = t1[0]
		co_nm = t1[1]
		temp_strin4 +='(' + name_to_var2[m_no] + ',' + name_to_var2[co_nm] +  '),'
	
	temp_strin4 = temp_strin4[:-1]  #removing the extra "," charater
	temp_strin4 += '}\n'
	#print temp_strin4
	
	temp_strin5 = 'duck => {'
	count = 1
	for i in mom:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin5 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin5 = temp_strin5[:-1]  #removing the extra "," character
	temp_strin5 += '} \n'
	#print temp_strin5
	
	temp_strin6 = 'strike_gt_200 => {'
	count = 1
	for i in strike_gt_200:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin6 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin6 = temp_strin6[:-1]  #removing the extra "," character
	temp_strin6 += '} \n'
	#print temp_strin6
	
	temp_strin7 = 'six_gt_four=> {'
	count = 1
	for i in six_gt_four:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin7 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin7 = temp_strin7[:-1]  #removing the extra "," character
	temp_strin7 += '} \n'
	#print temp_strin7

	temp_strin8 = 'boundary_gt_0=> {'
	count = 1
	for i in boundary_gt_0:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin8 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin8 = temp_strin8[:-1]  #removing the extra "," character
	temp_strin8 += '} \n'
	#print temp_strin8

	temp_strin9 = 'strike_lt_100=> {'
	count = 1
	for i in strike_lt_100:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin9 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin9 = temp_strin9[:-1]  #removing the extra "," character
	temp_strin9 += '} \n'
	#print temp_strin9
	

	temp_strin9 = 'strike_lt_100=> {'
	count = 1
	for i in strike_lt_100:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin9 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin9 = temp_strin9[:-1]  #removing the extra "," character
	temp_strin9 += '} \n'
	#print temp_strin9

	temp_strin10 = 'runs_gt_50=> {'
	count = 1
	for i in runs_gt_50:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin10 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin10 = temp_strin10[:-1]  #removing the extra "," character
	temp_strin10 += '} \n'
	#print temp_strin10
	
	temp_strin11 = 'runs_gt_100=> {'
	count = 1
	for i in runs_gt_100:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin11 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin11 = temp_strin11[:-1]  #removing the extra "," character
	temp_strin11 += '} \n'
	#print temp_strin11

	temp_strin12 = 'wicket_gt_0=> {'
	count = 1
	for i in wicket_gt_0:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin12 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin12 = temp_strin12[:-1]  #removing the extra "," character
	temp_strin12 += '} \n'
	#print temp_strin12

	temp_strin13 = 'wicket_lt_0=> {'
	count = 1
	for i in wicket_lt_0:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin13 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin13 = temp_strin13[:-1]  #removing the extra "," character
	temp_strin13 += '} \n'
	#print temp_strin13

	temp_strin14 = 'over_gt_7=> {'
	count = 1
	for i in over_gt_7:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin14 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin14 = temp_strin14[:-1]  #removing the extra "," character
	temp_strin14 += '} \n'
	#print temp_strin14

	temp_strin15 = 'rpo_gt_8=> {'
	count = 1
	for i in rpo_gt_8:
		t1= i.split(',')
		m_no = t1[0]
		pl_nm = t1[1]
		co_nm = t1[2]
		temp_strin15 +='(' + name_to_var[str(m_no)] + ',' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin15 = temp_strin15[:-1]  #removing the extra "," character
	temp_strin15 += '} \n'
	#print temp_strin15

	temp_strin16 = 'age_lt_26=> {'
	count = 1
	for i in age_lt_26:
		t1= i.split(',')
		pl_nm = t1[1]
		co_nm = t1[0]
		temp_strin16 +='(' + name_to_var[co_nm] + ',' + name_to_var[pl_nm] + '),'
		count = count +1

	temp_strin16 = temp_strin16[:-1]  #removing the extra "," character
	temp_strin16 += '} \n'
	#print temp_strin16

	temp_strin20= 'match => {odi1,odi2,odi3,odi4,odi5}\n'
	temp_strin21= 'country => {IN,NZ,NO}\n'
	temp_strin22= 'player => {r0,r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20,r21,r22,r23,r24,r25,r26,r27,r28,r29,r30}'

	v = temp_strin1 + temp_strin2 + temp_strin3+temp_strin4+temp_strin5+temp_strin6+temp_strin7+temp_strin8+temp_strin9+temp_strin10+temp_strin11+temp_strin12+temp_strin13+temp_strin15+temp_strin16+temp_strin20+temp_strin21+temp_strin22
	#print v
	
	# now forming the query
	return v
	

def parse_query(q1):
	

	q1=re.sub('[^0-9a-zA-Z .-]+', '', str(q1))
	q2 = q1.lower()
	q = TextBlob(q2)
	#print len(q.words)

	q4 = []
	for i in range (len(q.words)):
		q4.append(q.words[i].singularize())

	q5 = ''
	for i in range (len(q4)):
		q5 += str(q4[i]) + ' '
	q5 = q5[:-1]

	query = q5.split(' ')

	for word in query:
		if (word == 'match' or word =='inning' or word== 'player' or word == 'matches' or word =='innings' or word== 'players' ):
			q_info = query[:query.index(word)]
			q_info2 = query[query.index(word)]
			q_new = query[query.index(word)+1:]
			#print q_info
			#print q_new
			break
	
	info = ''
	for i in q_info:
		info += i +str(' ')
	info = info[:-1]
	info += str('/') + str(q_info2)

	q_new_string =''
	for i in q_new:
		q_new_string += str(i) + ' '
	q_new_string = q_new_string[:-1]
	#print q_new_string

	unigram = ngrams(q_new_string.split(), n=1)
	unigram_string = []
	for i in unigram :
		string = ''
		for j in i :
			string += str(j) + ' '
		string = string[:-1]
		unigram_string.append(string)
	#print unigram_string

	bigram = ngrams(q_new_string.split(), n=2)
	bigram_string = []
	for i in bigram :
		string = ''
		for j in i :
			string += str(j) + ' '
		string = string[:-1]
		bigram_string.append(string)
	#print bigram_string

	trigram = ngrams(q_new_string.split(), n=3)
	trigram_string = []
	for i in trigram :
		string = ''
		for j in i :
			string += str(j) + ' '
		string = string[:-1]
		trigram_string.append(string)
	#print trigram_string

	fourgram = ngrams(q_new_string.split(), n=4)
	fourgram_string = []
	for i in fourgram :
		string = ''
		for j in i :
			string += str(j) + ' '
		string = string[:-1]
		fourgram_string.append(string)
	#print fourgram_string

	fivegram = ngrams(q_new_string.split(), n=5)
	fivegram_string = []
	for i in fivegram :
		string = ''
		for j in i :
			string += str(j) + ' '
		string = string[:-1]
		fivegram_string.append(string)
	#print fivegram_string

	sixgram = ngrams(q_new_string.split(), n=6)
	sixgram_string = []
	for i in sixgram :
		string = ''
		for j in i :
			string += str(j) + ' '
		string = string[:-1]
		sixgram_string.append(string)
	#print sixgram_string

	sevengram = ngrams(q_new_string.split(), n=7)
	sevengram_string = []
	for i in sevengram :
		string = ''
		for j in i :
			string += str(j) + ' '
		string = string[:-1]
		sevengram_string.append(string)
	#print sevengram_string

	q_desc=[]

	for word in unigram_string:
		for verse in database :
			if word == verse :
				q_desc.append(database[verse]) 
				break

	for word in bigram_string:
		for verse in database :
			if word == verse :
				q_desc.append(database[verse]) 
				break

	for word in trigram_string:
		for verse in database :
			if word == verse :
				q_desc.append(database[verse]) 
				break

	for word in fourgram_string:
		for verse in database :
			if word == verse :
				q_desc.append(database[verse]) 
				break

	for word in fivegram_string:
		for verse in database :
			if word == verse :
				q_desc.append(database[verse]) 
				break

	for word in sixgram_string:
		for verse in database :
			if word == verse :
				q_desc.append(database[verse]) 
				break

	for word in sevengram_string:
		for verse in database :
			if word == verse :
				q_desc.append(database[verse]) 
				break
	print q_desc

	desc = ''
	for i in q_desc:
		desc += i +str('/')
	desc = desc[:-1]

	for word in unigram_string:
		if word == 'and' :
			q_ques = 'and'
		else :
			q_ques ='ifthen'
	#print q_ques
	
	parse_query = str(info) + str('.') + desc + str('.') + str(q_ques)
	return parse_query
def parse_for_case(parse_query):
	global quantifier
	global quantified
	global predicate1
	global predicate2
	global connector

	query=parse_query.split('.')
		
	info = query[0].split('/')
	quantifier = info[0]
	quantified = info[1]

	desc = query[1].split('/')
	predicate1= desc[0]
	if len(desc) > 1:
		predicate2 = desc[1]

	connector = query[2]

	return query
def main():
	testcases =input()
	
	for turn in range(0,testcases):
		#q1="For all innings, if strike rate of player is above 200.0 then he has hit more sixes than fours."
		q1 = raw_input('input (following grammar)\n')	
		mom_dict = {}
		winning_team_dict = {}
		batting_stats_dict = {}
		bowling_stats_dict = {}
		player_details_dict = {}

		player_details_file1='./dataset/player_profile/indian_players_profile.txt'
		player_details_file2='./dataset/player_profile/nz_players_profile.txt'
		
		mom_file1 = './dataset/match1/player_of_the_match1.txt'
		mom_file2 = './dataset/match2/player_of_the_match2.txt'
		mom_file3 = './dataset/match3/player_of_the_match3.txt'
		mom_file4 = './dataset/match4/player_of_the_match4.txt'
		mom_file5 = './dataset/match5/player_of_the_match5.txt'

		win_team_file1 = './dataset/match1/odi1_winning_team.txt'
		win_team_file2 = './dataset/match2/odi2_winning_team.txt'
		win_team_file3 = './dataset/match3/odi3_winning_team.txt'
		win_team_file4 = './dataset/match4/odi4_winning_team.txt'
		win_team_file5 = './dataset/match5/odi5_winning_team.txt' 
		
		batting_stats_file1 = './dataset/match1/odi1_inn1_bat.txt'
		batting_stats_file2 = './dataset/match1/odi1_inn2_bat.txt'
		batting_stats_file3 = './dataset/match2/odi2_inn1_bat.txt'
		batting_stats_file4 = './dataset/match2/odi2_inn2_bat.txt'
		batting_stats_file5 = './dataset/match3/odi3_inn1_bat.txt'
		batting_stats_file6 = './dataset/match3/odi3_inn2_bat.txt'
		batting_stats_file7 = './dataset/match4/odi4_inn1_bat.txt'
		batting_stats_file8 = './dataset/match4/odi4_inn2_bat.txt'
		batting_stats_file9 = './dataset/match5/odi5_inn1_bat.txt'
		batting_stats_file10 = './dataset/match5/odi5_inn2_bat.txt'

		bowling_stats_file1 = './dataset/match1/odi1_inn1_bowl.txt'
		bowling_stats_file2 = './dataset/match1/odi1_inn2_bowl.txt'
		bowling_stats_file3 = './dataset/match2/odi2_inn1_bowl.txt'
		bowling_stats_file4 = './dataset/match2/odi2_inn2_bowl.txt'
		bowling_stats_file5 = './dataset/match3/odi3_inn1_bowl.txt'
		bowling_stats_file6 = './dataset/match3/odi3_inn2_bowl.txt'
		bowling_stats_file7 = './dataset/match4/odi4_inn1_bowl.txt'
		bowling_stats_file8 = './dataset/match4/odi4_inn2_bowl.txt'
		bowling_stats_file9 = './dataset/match5/odi5_inn1_bowl.txt'
		bowling_stats_file10 = './dataset/match5/odi5_inn2_bowl.txt'
		
		add_to_dict_mom(mom_dict, mom_file1)
		add_to_dict_mom(mom_dict, mom_file2)
		add_to_dict_mom(mom_dict, mom_file3)
		add_to_dict_mom(mom_dict, mom_file4)
		add_to_dict_mom(mom_dict, mom_file5)
		#print 'mom_dict::'
		#print mom_dict

		add_to_dict_win_team(winning_team_dict, win_team_file1)
		add_to_dict_win_team(winning_team_dict, win_team_file2)
		add_to_dict_win_team(winning_team_dict, win_team_file3)
		add_to_dict_win_team(winning_team_dict, win_team_file4)
		add_to_dict_win_team(winning_team_dict, win_team_file5)
		#print 'win_team_dict::'
		#print winning_team_dict

		add_to_dict_batting_stats(batting_stats_dict, batting_stats_file1)
		add_to_dict_batting_stats(batting_stats_dict, batting_stats_file2)
		add_to_dict_batting_stats(batting_stats_dict, batting_stats_file3)
		add_to_dict_batting_stats(batting_stats_dict, batting_stats_file4)
		add_to_dict_batting_stats(batting_stats_dict, batting_stats_file5)
		add_to_dict_batting_stats(batting_stats_dict, batting_stats_file6)
		add_to_dict_batting_stats(batting_stats_dict, batting_stats_file7)
		add_to_dict_batting_stats(batting_stats_dict, batting_stats_file8)
		add_to_dict_batting_stats(batting_stats_dict, batting_stats_file9)
		add_to_dict_batting_stats(batting_stats_dict, batting_stats_file10)
		#print 'batting_stats_dict::'
		#print batting_stats_dict

		add_to_dict_bowling_stats(bowling_stats_dict, bowling_stats_file1)
		add_to_dict_bowling_stats(bowling_stats_dict, bowling_stats_file2)
		add_to_dict_bowling_stats(bowling_stats_dict, bowling_stats_file3)
		add_to_dict_bowling_stats(bowling_stats_dict, bowling_stats_file4)
		add_to_dict_bowling_stats(bowling_stats_dict, bowling_stats_file5)
		add_to_dict_bowling_stats(bowling_stats_dict, bowling_stats_file6)
		add_to_dict_bowling_stats(bowling_stats_dict, bowling_stats_file7)
		add_to_dict_bowling_stats(bowling_stats_dict, bowling_stats_file8)
		add_to_dict_bowling_stats(bowling_stats_dict, bowling_stats_file9)
		add_to_dict_bowling_stats(bowling_stats_dict, bowling_stats_file1)
		#print 'bowling_stats_dict::'
		#print bowling_stats_dict
		
		add_to_dict_player_details(player_details_dict, player_details_file1)
		add_to_dict_player_details(player_details_dict, player_details_file2)
		#print 'player_details_dict::'
		#print player_details_dict
		print '\nCase #'+ str(turn)
		print 'predicates involved::'
		
		query=parse_query(q1)
		
		print 'query::'
		print query

		case = parse_for_case(query)
		#print case

		model =generate_and_solve_query(mom_dict,winning_team_dict,batting_stats_dict,bowling_stats_dict,player_details_dict)
		#print model
		#print quantifier
		#print quantified
		#print predicate1
		#print predicate2
		#rint connector
		
		q=query_generation()
		print 'generated query::'
		print q
		
		print 'answer::'
		make_model_and_answer(model,q)
		print '\n'

		turn +=1

if __name__ == "__main__":
	main()
