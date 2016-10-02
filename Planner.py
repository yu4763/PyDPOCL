#from Flaws import *
from pddlToGraphs import *
import collections
from heapq import heappush, heappop
import itertools
from clockdeco import clock
from Ground import GLib
from Plannify import TopicLib

"""
	Algorithm for Plan-Graph-Space search of Story Plan
"""

class Frontier:
	def __init__(self):
		self._frontier = []

	def __len__(self):
		return len(self._frontier)

	def pop(self):
		return heappop(self._frontier)

	def insert(self, plan):
		heappush(self._frontier, plan)

	def __getitem__(self, position):
		return self._frontier[position]

	def extend(self, itera):
		for item in itera:
			self.insert(item)

import pickle

@clock
def upload(GL):
	afile = open("GL","wb")
	pickle.dump(GL,afile)
	afile.close()

@clock
def reload():
	afile = open("GL","rb")
	GL = pickle.load(afile)
	afile.close()
	return GL


class PlanSpacePlanner:

	def __init__(self, op_graphs, objects, init_action, goal_action, preprocess = False):
		#Assumes these parameters are already read from file

		self.op_graphs = op_graphs
		self.objects = objects

		print('preprocessing...')

		if preprocess:
			self.GL = GLib(op_graphs, objects, Argument.object_types, init_action, goal_action)
			upload(self.GL)
			print(len(self.GL))
		else:
			try:
				print('try to reload:')
				self.GL = reload()
				print(len(self.GL))
			except:
				print('could not reload')
				self.GL = GLib(op_graphs, objects, Argument.object_types, init_action, goal_action)
				upload(self.GL)

		from Relax import RelaxHeuristic
		RelaxHeuristic(self.GL)

		init = copy.deepcopy(self.GL[-2])
		init.replaceInternals()
		goal = copy.deepcopy(self.GL[-1])
		goal.replaceInternals()

		init_plan = PlanElementGraph(uuid.uuid1(0), Elements = objects | init.elements | goal.elements,
									  				 Edges = init.edges | goal.edges)

		init_plan.initial_dummy_step = init.root
		init_plan.final_dummy_step = goal.root

		#create special dummy step for init_graph and add to graphs {}
		self.setup(init_plan, init, goal)
		self.Open =  Frontier()
		self.Open.insert(init_plan)
		print('finished preprocessing...')

	def __len__(self):
		return len(self._frontier)

	def __getitem__(self, position):
		return self._frontier[position]

	def __setitem__(self, plan, position):
		self._frontier[position] = plan

	def setup(self, plan, start_action, end_action):
		"""
			Create step typed element DI, with effect edges to each condition of start_set
			Create step typed element DG, with precondition edges to each condition of end_set
			Add ordering from DI to DG
		"""

		dummy_start = start_action.root
		dummy_final = end_action.root

		plan.OrderingGraph.addOrdering(dummy_start, dummy_final)

		#Add initial Open precondition flaws for dummy step
		init_flaws = (Flaw((dummy_final, prec), 'opf') for prec in plan.getNeighborsByLabel(dummy_final, 'precond-of'))
		for flaw in init_flaws:
			plan.flaws.insert(self.GL, plan, flaw)


	#@clock
	def newStep(self, plan, flaw):
		"""
		@param plan:
		@param flaw:
		@return:
		"""

		results = set()
		s_need, precondition = flaw.flaw

		#antecedent is of the form (antecedent_action_with_missing_eff_link, eff_link)
		antecedents = self.GL.pre_dict[precondition.replaced_ID]
		#print('flaw precondition.replaced_ID: {}'.format(precondition.replaced_ID))
		for ante in antecedents:
			if ante.action.name == 'dummy_init':
				continue

			#step 1 - make a copy
			cndt = copy.deepcopy(ante)

			#step 2 - replace its internals, to distinguish from other identical antesteps
			(anteaction, eff_link) = cndt
			anteaction.replaceInternals()

			#step 3 - make a copy of the plan
			new_plan = plan.deepcopy()

			#step 4 - set sink before replace internals
			preserve_original_id = eff_link.sink.replaced_ID
			eff_link.sink = new_plan.getElementById(precondition.ID)
			eff_link.sink.replaced_ID = preserve_original_id
			# check: eff_link.sink should till be precondition of s_need

			#step 5 - add new stuff to new plan
			new_plan.elements.update(anteaction.elements)
			new_plan.edges.update(anteaction.edges)

			#step 6 - update orderings and causal links, add flaws
			self.addStep(new_plan, anteaction.root, new_plan.getElementById(s_need.ID), eff_link.sink, new=True)
			new_plan.flaws.addCndtsAndRisks(self.GL, anteaction.root)

			#step 7 - add new_plan to open list
			results.add(new_plan)

		return results

	#@clock
	def reuse(self, plan, flaw):
		results = set()
		s_need, precondition = flaw.flaw

		#antecedents - a set of stepnumbers
		antecedents = self.GL.id_dict[precondition.replaced_ID]
		if len(antecedents) == 0:
			return set()

		for s_old in plan.Steps:
			if not s_old.stepnumber in antecedents:
				continue
			if s_old == s_need:
				continue

			#step 1 - make a copy of the plan, also replaces the plan number
			new_plan = plan.deepcopy()

			#step 2 - Actionize the steps from new_plan
			S_Old = Action.subgraph(new_plan, s_old)
			S_Need = Action.subgraph(new_plan, s_need)

			#step 3-4 retarget precondition to be s_old effect
			pre_link_sink = self.RetargetPrecondition(new_plan, S_Old, precondition)

			#step 5 - add orderings, causal links, and create flaws
			self.addStep(new_plan, S_Old.root, S_Need.root, pre_link_sink,  new=False)

			#step 6 - add new plan to open list
			results.add(new_plan)

		return results

	def RetargetPrecondition(self, plan,  S_Old, precondition):
		effect_token = self.GL.getConsistentEffect(S_Old, precondition)
		pre_link = plan.RemoveSubgraph(precondition)
		pre_link.sink = effect_token
		return pre_link.sink

	def addStep(self, plan, s_add, s_need, condition, new=None):
		"""
			when a step is added/reused, 
			add causal link and ordering edges (including to dummy steps)
			If step is new, add open precondition flaws for each precondition
		"""
		if new == None:
			new = False

		if not s_add == plan.initial_dummy_step:
			plan.OrderingGraph.addEdge(plan.initial_dummy_step, s_add)
			plan.OrderingGraph.addEdge(plan.initial_dummy_step, s_need)

		if not s_need == plan.final_dummy_step:
			plan.OrderingGraph.addEdge(s_add, plan.final_dummy_step)
			plan.OrderingGraph.addEdge(s_need, plan.final_dummy_step)

		#Always add this ordering
		plan.OrderingGraph.addEdge(s_add, s_need)
		plan.CausalLinkGraph.addEdge(s_add, s_need, condition)

		if new:
			for prec in plan.getIncidentEdgesByLabel(s_add, 'precond-of'):
				plan.flaws.insert(self.GL, plan, Flaw((s_add, prec.sink), 'opf'))

		#Good time as ever to updatePlan
		#plan.updatePlan()
		return plan

	#@clock
	def resolveThreatenedCausalLinkFlaw(self, plan, flaw):
		"""
			Promotion: Add ordering from sink to threat, and check if cycle
			Demotion: Add ordering from threat to source, and check if cycle
		"""
		results = set()
		threat, causal_link = flaw.flaw

		#Promotion
		promotion = plan.deepcopy()
		promotion.OrderingGraph.addEdge(causal_link.sink, threat)
		results.add(promotion)


		#Demotion
		demotion = plan.deepcopy()
		demotion.OrderingGraph.addEdge(threat, causal_link.source)
		results.add(demotion)

		return results


	def generateChildren(self, plan, flaw):
		results = set()
		if flaw.name == 'opf':
			results = self.reuse(plan, flaw)
			results.update(self.newStep(plan, flaw))

		if flaw.name == 'tclf':
			results = self.resolveThreatenedCausalLinkFlaw(plan, flaw)

		#for result, res in results:
		for result in results:
			new_flaws = result.detectThreatenedCausalLinks(self.GL)
			result.flaws.threats.update(new_flaws)

		return results

	@clock
	def POCL(self, num_plans = 5):
		Completed = []
		visited = 0
		#Visited = []

		while len(self.Open) > 0:

			#Select child
			plan = self.Open.pop()

			visited+=1

			if not plan.isInternallyConsistent():
				#print('branch terminated')
				continue

			#for step in topoSort(plan):
				#print(Action.subgraph(plan, step))

			if len(plan.flaws) == 0:
				print('solution found at {} nodes visited and {} nodes expanded'.format(visited, len(self.Open)))
				Completed.append(plan)
				if len(Completed) == num_plans:
					return Completed
				continue

			#print(plan)
			#print(plan.flaws)

			#Select Flaw
			flaw = plan.flaws.next()
			#print('selected : {}\n'.format(flaw))

			#Add children to Open List
			children = self.generateChildren(plan, flaw)

			#print('generated children: {}'.format(len(children)))
			for child in children:
				self.Open.insert(child)

			#print('open list number: {}'.format(len(self.Open)))
			#print('\n')


@clock
def preprocessDomain(operators):
	#get all effect predicates
	pred_set = set()
	for op in operators:
		pred_set.update({eff.name for eff in  op.getNeighborsByLabel(op.root, 'effect-of')})
	return pred_set

def topoSort(graph):
	OG  = copy.deepcopy(graph.OrderingGraph)
	L =[]
	S = {graph.initial_dummy_step}
	while len(S) > 0:
		n = S.pop()
		L.append(n)
		for m_edge in OG.getIncidentEdges(n):
			OG.edges.remove(m_edge)
			if len({edge for edge in OG.getParents(m_edge.sink)}) == 0:
				S.add(m_edge.sink)
	if len(OG.edges) > 0:
		print('error')
		return
	return L

def obTypesDict(object_types):
	obtypes = defaultdict(set)
	for t in object_types:
		obtypes[t.name].add(t.parent)
		accumulated = set()
		rFollowHierarchy(object_types, t.parent, accumulated)
		obtypes[t.name].update(accumulated)
	return obtypes


def rFollowHierarchy(object_types, child_name, accumulated = set()):
	for ob in object_types:
		if not ob.name in accumulated:
			if ob.name == child_name:
				accumulated.add(ob.parent)
				rFollowHierarchy(object_types, ob.parent, accumulated)

import unittest

from Plannify import Plannify
class TestPlanner(unittest.TestCase):
	def testArk(self):
		domain_file = 'domains/ark-domain.pddl'
		problem_file = 'domains/ark-problem.pddl'
		operators, objects, object_types, initAction, goalAction = parseDomainAndProblemToGraphs(domain_file,
																								 problem_file)
		FlawLib.non_static_preds = preprocessDomain(operators)
		Argument.object_types = obTypesDict(object_types)
		planner = PlanSpacePlanner(operators, objects, initAction, goalAction,preprocess = True)

		n = 2
		results = planner.POCL(n)
		assert len(results) == n
		for result in results:
			totOrdering = topoSort(result)
			print('\n\n\n')
			for step in topoSort(result):
				print(Action.subgraph(result, step))

	def testDecomp(self):
		sdomain_file = 'domains/ark-domain.pddl'
		sproblem_file = 'domains/ark-problem.pddl'
		operators, objects, object_types, initAction, goalAction = parseDomainAndProblemToGraphs(sdomain_file,
																								 sproblem_file)
		FlawLib.non_static_preds = preprocessDomain(operators)
		Argument.object_types = obTypesDict(object_types)
		story_planner = PlanSpacePlanner(operators, objects, initAction, goalAction,preprocess = False)


		domain_file = 'domains/ark-requirements-domain.pddl'
		problem_file = 'domains/ark-requirements-problem.pddl'
		doperators, dobjects, dobject_types, dinitAction, dgoalAction = parseDomainAndProblemToGraphs(domain_file,
																								problem_file)

		#empty_plan = story_planner.Open.pop()
		for op in doperators:
			decomp = next(iter(op.subgraphs))
			print('\ndiscourse /decomp name {}\n'.format(decomp.name))
			Plannify(decomp, story_planner.GL)
			#assignments = TopicLib(decomp, story_planner.GL, objects)
		print('ok')

if __name__ ==  '__main__':
	tp = TestPlanner()
	tp.testDecomp()
	#unittest.testDecomp()
	# unittest.main()