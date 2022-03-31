class Model():
        
    def __init__(self, model_file):
        super().__init__()
        self.reset()
        self.GOALS = { 
            0: (20, False),
            # 5: (80, False),
            10: (9, False),
            # 15: (85, False),
            20: (99, True)
        }

    def get_goal(self, step):
        self.current_goal = self.GOALS.get(step, self.current_goal) 
        return self.current_goal

    def next_action(self):
        action = input()
        self.check_action(action)
        return action

    def check_action(self, action):
        if action not in ["N", "E", "S", "W"]:
            raise ValueError("Run Ended - Invalid Action")

    def reset(self):
        self.current_goal = None

    def is_win_goal(self):
        if self.current_goal == None:
            return False
        return self.current_goal[1]

