from cgitb import text
from random import choice
from re import T
import math
from sqlalchemy import null
from model import Model
from priorityQueue import PriorityQueue


class ModelLRTA(Model):

    def __init__(self, model_file):
        super().__init__(model_file)
        self.reset()
        relative_path = 'gym_maze/envs/maze_samples/'
        self._load_model(relative_path + model_file)

    def _load_model(self, fullpath):
        self.arcos = dict()
        # {0:{N: 1, S: }}
        self.costos = dict()
        # {0:H()}
        self.reached = dict()
        
        self.inf = 100000
        self.H = 0
        self.pa = null
        self.pn = null
        self.actions = ['N', 'S', 'E', 'W']

    def set_state(self, state):
        self.state = state

    def next_state(self, action):
        state = self.state.copy()
        next_state, _, _, _ = self.step(action)
        self.state = state
        return next_state

    def next_actionV2(self, node):
        return self.lrta_star(node)

    def set_mazeSize(self, size):
        self.maze_size = size

    def lrta_star(self, node):
        if(self.current_goal == node):
            return
        try:
            self.costos[node]
        except:
            self.arcos[node] = dict()
            self.costos[node] =  self.heuristica(node, self.current_goal)
        if(self.pa != null and self.pn != null):
            self.arcos[self.pn][self.pa] = node

        goal = self.current_goal
        self.last_goal = goal
        
        costs = {
            'N': self.costo(node, 'N'),
            'S': self.costo(node, 'S'),
            'W': self.costo(node, 'W'),
            'E': self.costo(node, 'E')
        }

        
        
        min_val = min(costs.values()) 
        self.costos[node] = min_val
          
        possible_solutions = []
        for key, value in costs.items():
            if min_val == value:
              possible_solutions.append(key)
        
        prefered_direction = null
        for sol in possible_solutions:
            try:
                self.arcos[node][sol]
            except:
                prefered_direction = sol
        
        if(prefered_direction == null):
            self.pa = choice(possible_solutions)
        else:
            self.pa = prefered_direction
        self.pn = node

        return self.pa

    def costo(self, node, a):
        try:
            next_node = self.arcos[node][a]
            if(next_node == node):
                return 1000 + self.costos[next_node] 
            return 1 + self.costos[next_node] 
        except:
            return 0 + self.costos[node]
        

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

