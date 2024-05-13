from thoughtsculpt.mcts_node import MCTSNode

class DecisionSimulator:
    def __init__(self, api_key):
        self.api_key = api_key

    def simulate(self, candidate_solutions, task_description, max_depth, num_simulations):
        root = MCTSNode(candidate_solutions[0])
        for _ in range(num_simulations):
            node = root
            while not node.is_terminal():
                if not node.is_fully_expanded():
                    child = node.expand(self.api_key, task_description)
                    reward = self.rollout(child, task_description, max_depth)
                    child.backpropagate(reward)
                    break
                else:
                    node = node.select_child()
        return root.best_child().solution

    def rollout(self, node, task_description, depth):
        if depth == 0:
            return node.evaluate(self.api_key, task_description)
        child = node.expand(self.api_key, task_description)
        return self.rollout(child, task_description, depth - 1)