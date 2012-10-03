#!/usr/bin/env python
# ECE 2524 | Homework 4, Problem 1 | Brandon Fairburn

import sys

argc = len(sys.argv)
argv = sys.argv

help_msg = """usage: inventory.py [-f, --data-file] filename
\toptional arguments: -h, --help: show this message

Perform actions on parts in data file.

The data file is formatted as follows
PartID:Description:Footprint:Quantity

Minilanguage description:
list\t\t\t\t\t- display every part 
list sort Field\t\t\t\t- display every part, sorted by Field
list Field=Value\t\t\t- display parts where Field is equal to Value
remove Field=Value\t\t\t- removes any part from data file with Field equal to Value
set Value=Value1 for Target=Value2\t- change Value field to Value1 for any part where Target field is equal to Value2
add Fields=Values\t\t\t- add a new part with Fields equal to Values (must supply all fields)""" 

##############################
#functions

#parse the action through the minilanguage
def parse(action):
	action = action.split(' ')
	
	if action[0] == 'list':
		if len(action) == 1:
			list('all')
		elif len(action) == 2:
			list(action[1])
		else:
			sort = None
			for i in range(len(action)):
				if action[i] == 'sort':
					sort = action[i+1]
			if sort != None:
				sortlist(sort)
	
	elif action[0] == 'add':
		newpart = []
		for word in action:
			if word != 'add':
				newpart.append(word)
		add(newpart)
		
	elif action[0] == 'remove':
		remove(action[1])
		
	elif action[0] == 'set':
		for i in range(len(action)):
			if action[i] == 'set':
				value = action[i+1]
			if action[i] == 'for':
				target = action[i+1]
		update(value, target)
		
	else:
		sys.stderr.write('Error: invalid action \'%s\'\n'%(action[0]))
		sys.exit(1)
		
#list specified parts
def list(which):
	if which == 'all':
		for line in data:
			print line,
	
	else:
		key = which.split('=')
		
		field = getField(key[0])
		for line in data:
			line = line.split(':')
			if line[field].replace('\n', '') == key[1]:
				line[field] = str(line[field])
				print ':'.join(line),

#return field index
def getField(fieldname):
	if fieldname == 'PartID':
		field = 0
	elif fieldname == 'Description':
		field = 1
	elif fieldname == 'Footprint':
		field = 2
	elif fieldname == 'Quantity':
		field = 3
	else:
		sys.stderr.write('Error: invalid fieldname \'%s\'\n'%(fieldname))
		sys.exit(1)
	
	return field

#display list sorted by specified field
def sortlist(sort):
	output = []
	
	lam = lambda key: key[field] #used as key for sorting list
	#determine what field the parts list is sorted by
	field = getField(sort)
	if field == 3:
		lam = lambda key: int(key[field])
		
	for line in data:
		if not line.strip():
			continue
		output.append(line.split(':'))
	output = sorted(output, key=lam)
	for i in range(len(output)):
		output[i] = ':'.join(output[i])
		print output[i],

#add a new part
def add(part):
	newpart = [0, 0, 0, 0] #initializing list of size 4
	for field in part:
		field = field.split('=')
		key = getField(field[0])
		newpart[key] = field[1]
	print 'OK'
		
	
	newpart = ':'.join(newpart)
	with open(filename, 'a') as f:
		f.write(newpart + '\n')
		
#remove a specified part
def remove(part):
	part = part.split('=')
	field = getField(part[0])
	
	newpartslist = []
	for line in data:
		chunks = line.split(':')
		#special case for quantity since it is an integer
		if field == 3:
			if int(chunks[field]) == int(part[1]):
				continue
		
		if chunks[field] == part[1]:
			continue
		newpartslist.append(line)
		
	newpartslist = ''.join(newpartslist)
	with open(filename, 'w') as f:
		f.write(newpartslist)
	print 'OK'
		
#update a value in specified parts
def update(value, target):
	value = value.split('=')
	target = target.split('=')
	
	valuekey = getField(value[0])
	targetkey = getField(target[0])
		
	updatedparts = []
	for line in data:
		line = line.split(':')
		if line[targetkey] == target[1]:
			#make sure to add a new line after quantity
			if valuekey == 3:
				line[valuekey] = str(value[1]) + '\n'
			else:
				line[valuekey] = value[1]
		updatedparts.append(':'.join(line))
		
	updatedparts = ''.join(updatedparts)
	with open(filename, 'w') as f:
		f.write(updatedparts)
	print 'OK'
##############################

filename = None
for i in range(0, argc):
	if argv[i] == '-f' or argv[i] == '--data-file':
		filename = argv[i+1]
	if argv[i] == '-h' or argv[i] == '--help':
		print help_msg
		sys.exit(0)

#process actions
while True:
	try:
		action = raw_input()
	except EOFError:
		break
	#ignore blank lines and commented lines
	if action == '\n' or action[0] == '#':
		continue
	if filename != None:
		with open(filename, 'r') as f:
			data = f.readlines()
		print 'Action: ', action
		print '--------------------------'
		parse(action)
		print '\n',