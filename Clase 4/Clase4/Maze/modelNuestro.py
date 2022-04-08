from cgitb import text
from random import choice
from model import Model
from priorityQueue import PriorityQueue
import math;

class ModelNuestro(Model):

    def __init__(self, model_file):
        super().__init__(model_file)
        self.reset()
        relative_path = 'gym_maze/envs/maze_samples/'
        self._load_model(relative_path + model_file)

    def _load_model(self, fullpath):
        print("Load your model here with file:", fullpath)
        with open(str(fullpath), 'r') as f:
            textList = list(f)
            nodosDict = dict()
            largo = int(len(textList)/4)
            self.maze_size = math.sqrt(largo)
            for i in range(0, largo):
                pos = i*4
                currentDict = dict()
                north = textList[pos].split()
                east = textList[1 + pos].split()
                south = textList[2 + pos].split()
                west = textList[3 + pos].split()
                currentDict["N"] = north[2]
                currentDict["E"] = east[2]
                currentDict["S"] = south[2]
                currentDict["W"] = west[2]
                nodosDict[north[0]] = currentDict
            self._raw_model = nodosDict
            self.last_goal = -1

    def set_state(self, state):
        self.state = state

    def next_state(self, action):
        state = self.state.copy()
        next_state, _, _, _ = self.step(action)
        self.state = state
        return next_state

    def next_actionV2(self, node):
        if(self.last_goal != self.current_goal):
            #end_node, prev_node = self.bfs(node)
            end_node, prev_node = self.a_star(node)
            self.make_strategy(end_node, prev_node)
        return self.strategy(node)

    def set_mazeSize(self, size):
        self.maze_size = size

    def bfs(self, node):
        goal = self.current_goal
        self.last_goal = goal
        actions = ['N', 'S', 'E', 'W']

        to_visit = [node]
        reached = set()
        prev_node = dict()

        while to_visit != []:
            node = to_visit.pop(0)
            reached.add(node)
            if str(self.current_goal[0]) == node:
                return node, prev_node
            for a in actions:
                child = self._raw_model[node][a]
                if not (child in to_visit or child in reached):
                    to_visit.append(child)
                    prev_node[child] = (node, a)

    def a_star(self, node):
        goal = self.current_goal
        self.last_goal = goal
        actions = ['N', 'S', 'E', 'W']

        to_visit = PriorityQueue()
        to_visit.push(node, 0)
        reached = set()
        prev_node = dict()

        while not to_visit.is_empty():
            node, cost = to_visit.pop()
            reached.add(node)
            if str(self.current_goal[0]) == node:
                return node, prev_node
            for a in actions:
                child = self._raw_model[node][a]
                if not (child in to_visit or child in reached):
                    cost_value = cost + self.heuristica(node, goal)
                    to_visit.push(child, cost_value)
                    prev_node[child] = (node, a)

    def heuristica(self, node, goal):
        y_node, x_node = self.interpretCoords(node)
        y_goal, x_goal = self.interpretCoords(str(goal[0]))
        return abs(y_node - y_goal) + abs(x_node - x_goal)

    def interpretCoords(self, node):
        largo = len(str(self.maze_size - 1))
        largoNode = len(str(node))
        
        der = int(str(node)[-largo:])
        try:
            izq = int(str(node)[0:largoNode-largo])
            return izq, der
        except:
            return der, 0

    def make_strategy(self, node, prev_node):
        strategyDict = dict()
        try:
            while True:
                parent, action = prev_node[node]
                strategyDict[parent] = action
                node = parent
        except:
            self.strategyDict = strategyDict
            return

    def strategy(self, node):
        actions = ['N', 'S', 'E', 'W']
        try:
            return self.strategyDict[node]
        except:
            return choice(actions)
