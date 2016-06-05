from PlanElementGraph import *

print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')
excavate = Operator(id = 1, type = 'Action', name = 'excavate', num_args = 3, instantiated = True)

p1 = Literal(id=2, type='Condition', name= 'alive', 			num_args = 1, truth = True)
p2 = Literal(id=3, type='Condition', name= 'at', 				num_args = 2, truth = True)
p3 = Literal(id=4, type='Condition', name= 'burried', 			num_args = 2, truth = True)
p4 = Literal(id=5, type='Condition', name= 'knows-location', 	num_args = 3, truth = True)

e1 = Literal(id=6, type='Condition', name='burried',	num_args=2,	 truth = False)
e2 = Literal(id=7, type='Condition', name='has', 		num_args=2,	 truth = True)

consent = 	Actor(id=8,	 		type='actor',	 arg_pos_dict = {excavate.id :	1})
item = 		Argument(id = 9, 	type='var',		 arg_pos_dict=	{excavate.id :  2})
place = 	Argument(id = 10, 	type='var',		 arg_pos_dict=	{excavate.id :  3})

edge0 = Edge(excavate, consent, 'actor-of')
edge1 = Edge(excavate, p1,	 	'precond-of')
edge2 = Edge(excavate, p2, 		'precond-of')
edge3 = Edge(excavate, p3, 		'precond-of')
edge4 = Edge(excavate, p4, 		'precond-of')

edge5 = Edge(excavate, e1, 'effect-of')
edge6 = Edge(excavate, e2, 'effect-of')

edge7 = Edge(	p1, consent, 'first-arg')
edge8 = Edge(	p2, consent, 'first-arg')
edge9 = Edge(	p4, consent, 'first-arg')
edge10 = Edge(	e2, consent, 'first-arg')

edge12 = Edge(p2, item, 'sec-arg')
edge13 = Edge(p3, item, 'first-arg')
edge14 = Edge(p4, item, 'sec-arg')
edge15 = Edge(e1, item, 'first-arg')
edge16 = Edge(e2, item, 'sec-arg')

edge17 = Edge(p2, place, 'sec-arg')
edge18 = Edge(p3, place, 'sec-arg')
edge19 = Edge(p4, place, 'third-arg')
edge20 = Edge(e1, place, 'sec-arg')

excavate_elements = {excavate, p1, p2, p3, p4, e1, e2, consent, item, place}
excavate_edges = {edge0, edge1, edge2, edge3, edge4, edge5, edge6, edge7, edge8, edge9, edge10, \
					edge12, edge13, edge14,edge15, edge16,edge17, edge18, edge19, edge20}
					
op_kill = Operator(id = 3111, name = 'kill', type = 'Action', num_args = 4, executed = None, instantiated = True)
pre_kill_1 = Literal(id = 3211, name = 'alive', type = 'Condition', num_args = 1, truth = True)
pre_kill_2 = Literal(id = 3311, name = 'at', type = 'Condition', num_args = 2, truth = True)
pre_kill_3 = Literal(id = 3411, name='has', type = 'Condition', num_args = 2, truth = True)
pre_kill_4 = Literal(id = 3511, name = 'alive', type = 'Condition', num_args = 1, truth = True)
pre_kill_5 = Literal(id = 3611, name = 'at', type = 'Condition', num_args = 2, truth = True)
eff_kill_1 = Literal(id=3711, name='alive', type = 'Condition', num_args = 1, truth = False)
killer = Actor(id = 3811, name = None, type = 'actor', arg_pos_dict = {3111:1})
weapon = Argument(id=3911, type = 'var', arg_pos_dict = {3111:2})
victim = Actor(id = 3911, name = None, type = 'actor', arg_pos_dict = {3111:3})
place1 = Actor(id = 3921, name = None, type = 'var', arg_pos_dict = {3111:4})

kill_edges = {	Edge(op_kill, pre_kill_1, 'precond-of'),\
				Edge(op_kill, pre_kill_2, 'precond-of'),\
				Edge(op_kill, pre_kill_3, 'precond-of'),\
				Edge(op_kill, pre_kill_4, 'precond-of'),\
				Edge(op_kill, pre_kill_5, 'precond-of'),\
				Edge(op_kill, eff_kill_1, 'effect-of'),\
				Edge(pre_kill_1, killer, 'first-arg'),\
				Edge(pre_kill_2, killer, 'first-arg'),\
				Edge(pre_kill_2, place1, 'sec-arg'),\
				Edge(pre_kill_3, killer, 'first-arg'),\
				Edge(pre_kill_3, weapon, 'sec-arg'),\
				Edge(pre_kill_4, victim, 'first-arg'),\
				Edge(pre_kill_5, victim, 'first-arg'),\
				Edge(pre_kill_5, place1, 'sec-arg')}
				
kill_elements = {op_kill, pre_kill_2, pre_kill_1, pre_kill_3, pre_kill_4, pre_kill_5, eff_kill_1, weapon, place1, victim, killer}
	
example = Operator(id = 111, type= 'Action')
example2 = Operator(id = 2111, type= 'Action')
te = Literal(id = 2211, type='Condition', name='alive', truth= False, num_args = 1)

example_p1 =		Literal(id=211, 		type='Condition', 		name='alive', 		num_args = 1,	truth = True)
example_e1 = 		Literal(id=311, 		type = 'Condition', 	name='has', 	num_args = 2,		truth = True)
example_e3 = 		Literal(id=911, 		type = 'Condition', 	name='has', 			truth = True)
ex_const_element = 	Literal(id=611, 		type ='Condition',		name='knows-location', 	truth = True)
example_actor = 	Actor(id=411, 		type='actor',			arg_pos_dict={example.id : 1})
example_item = 		Argument(id=511,		type='var', 			arg_pos_dict={})


example_edge5 = Edge(example,	 example_e3, 	'effect-of')


example_elements = 	{	example, \
						example_p1, \
						example_e1, \
					#	example_e3,\
						example_actor, \
						example_item,\
						ex_const_element}
						
# example_edges = 	{	Edge(example,	 example_p1, 	'precond-of'),\
						# Edge(example,	 example_e1, 	'effect-of'),\
						# Edge(example_p1, example_actor, 'first-arg'),\
						# Edge(example_e1, example_actor, 'first-arg'),\
						# Edge(example_e1, example_item, 	'sec-arg')}
						
example_edges = 	{	Edge(example,	 example_p1, 	'precond-of'),\
						Edge(example,	 example_e1, 	'effect-of'),\
						Edge(example_p1, example_actor, 'first-arg'),\
						Edge(example_e1, example_actor, 'first-arg'),\
						Edge(example_e1, example_item, 	'sec-arg'),\
						Edge(example2,	 te, 			'effect-of'),\
						Edge(te, 		 example_actor, 'first-arg')}

						
example_constraints = {	Edge(ex_const_element, example_actor,	'first-arg'),\
						Edge(ex_const_element, example_item, 	'sec-arg')}


####Operator - Domain Action
Excavate_operator =			Action(	id = 200,\
							graph_type = 'Action', \
							name = 'excavate', \
							Elements = excavate_elements, \
							root_element = excavate,\
							Edges = excavate_edges)
							
Kill_operator =				Action(	id = 3001,\
							graph_type = 'Action', \
							name = 'kill', \
							Elements = kill_elements, \
							root_element = op_kill,\
							Edges = kill_edges)

Example_step =	 			Action(	id = 1111, \
							graph_type='Action', \
							Elements = example_elements, \
							root_element = example,\
							Edges = example_edges, \
							Constraints = example_constraints)

Excavate_operator_A = Excavate_operator.copyGen()
Example_step_A  = Example_step.copyGen()

Excavate_operator_B = Excavate_operator.makeCopyFromID(9000,11)
#print(Excavate_graph_A.root.id)
Example_step_B  = Example_step.copyGen()

Excavate_operator_B = Excavate_operator.makeCopyFromID(9000,11)

#print('\n\texcavate operator:')
#Excavate_operator_A.print_graph()

# F	=	IntentionFrame(id = 2222, type_graph = 'IntentionFrame', name=None, \
		# Elements=example_elements,\
		# Edges=example_edges,\
		# Constraints=example_constraints,\
		# goal = example_e1,#change with example_p1 to fail\
		# ms = None,\
		# sat = example,\
		# actor=None)
		
#example_elements.add(F.root) #Intention Frame element
ife = IntentionFrameElement(	id = 2222, type_graph = 'IntentionFrame', name=None, ms =None, motivation =None,intender = None,goal = example_e1,sat = example)
example_elements.add(ife)
example_edges.update({Edge(ife,example_e1, 'goal-of'), Edge(ife, example, 'sat-of')})

P1 = 	PlanElementGraph(id = 5432,\
		Elements=example_elements,\
		Edges=example_edges,\
		Constraints=example_constraints)

print('___________________________________________')
print('Plan Before instantiation of partial step elements')
P1.print_plan()
print('\n')
#P1.print_graph()
print('___________________________________________\n')
#print('\n\tPlan')

s = next(iter(P1.Steps))
#step = P1.getElementGraphFromElement(s, Action)
print('___________________________________________')
print('Instantiating a partial step as an operator')
new_plans = P1.instantiate(s, Excavate_operator)
print('___________________________________________\n')
print('______________________________________')
print('New Plans from instantiated operator:')
for plan in new_plans:
	plan.print_plan()
	plan.print_graph()
print('______________________________________\n')

all_plans = P1.instantiate_steps_with({Excavate_operator, Kill_operator})
print('___________________________________________\n')
print('______________________________________')
print('New Plans from ALL instantiated operator:')
for plan in all_plans:
	plan.print_plan()
	plan.print_graph()
print('______________________________________\n')

print('Element Tests')
print('______________________________')
for plan in new_plans:
	for element in plan.elements:
		if type(element) is IntentionFrameElement:
			print("++++++++++++++++++++++++")
			goal_element = plan.getElementById(element.goal.id)
			print('goal: {}'.format(element.goal.id), end = " ")
			plan.getElementGraphFromElement(goal_element, Condition).print_graph()

#P1.print_plan()
#new_plans = step.instantiate(Excavate_operator_A,P1)


#print('num_consenting actors = {} in step {}'.format(len(P1.getConsistentActors(P1.Steps)),step.id))

#print(step.id)

#print('num new plans: {}'.format(len(new_plans)))
#for plan in new_plans:
	#print('num_consenting actors = {} in steps'.format(len(plan.getConsistentActors(plan.Steps))))
#	plan.print_plan()
	#for element in plan.elements:
		#element.print_element()
		


""" Test whether Actions in F.Steps are equivalent to Actions created in isolation"""
""" Test rPickActorFromSteps when there are and are not consistent_actors"""

"""	Test adding step to an intention frame if already in plan. 
"""