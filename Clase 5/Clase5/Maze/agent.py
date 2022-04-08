import time
class Agent():

    def __init__(self, model):
        super().__init__()
        self.model = model
        print(model)

    def run(self, env):
        self.model.reset()
        return self._loop(env)

    def _loop(self, env):
        print("Play manually...")
        obs = env.reset()
        env.render()
        done = False
        step_counter = 0
        all_rewards = 0

        while not done:
            self.set_goal(step_counter, env)
            
            node = obs[0] + obs[1]*env.maze_size[1]
        
            action = self.model.next_actionV2(str(node))
            obs, reward, done_env, _ = env.step(action)
            print("obs=" + str(obs) + " reward=" +
                  str(reward) + " done_env=" + str(done_env))
            all_rewards += reward
            done = done_env and self.model.is_win_goal()
            env.render()
            step_counter += 1
            time.sleep(0.5)

        return all_rewards, step_counter

    def set_goal(self, step_counter, env):
        goalId = self.model.get_goal(step_counter)[0]
        print("Goal " + str(step_counter) +
              " is " + str(self.model.current_goal))
        env.set_goal(goalId)
