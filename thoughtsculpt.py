import dspy
from dspy.teleprompt import BootstrapFewShotWithRandomSearch
import os
from dotenv import load_dotenv
import logging
from sentence_transformers import SentenceTransformer, util
from rouge import Rouge
import random

# Load environment variables and setup logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure DSPy with LLM
llm = dspy.OpenAI(
    model='gpt-3.5-turbo',
    api_key=os.environ['OPENAI_API_KEY'],
    max_tokens=1000
)
dspy.settings.configure(lm=llm)

class ThoughtEvaluator(dspy.Signature):
    """Evaluate a thought and provide feedback."""
    thought = dspy.InputField()
    feedback = dspy.OutputField()
    score = dspy.OutputField(desc="A float between 0 and 1")

class ThoughtGenerator(dspy.Signature):
    """Generate a new thought based on instruction, current thought, and feedback."""
    instruction = dspy.InputField()
    current_thought = dspy.InputField()
    feedback = dspy.InputField()
    new_thought = dspy.OutputField()

class Evaluator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.evaluate = dspy.Predict(ThoughtEvaluator)

    def forward(self, thought):
        return self.evaluate(thought=thought)

class Generator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.Predict(ThoughtGenerator)

    def forward(self, instruction, current_thought, feedback):
        return self.generate(instruction=instruction, current_thought=current_thought, feedback=feedback)

class DecisionSimulator(dspy.Module):
    def forward(self, thoughts):
        return self.mcts(thoughts)
    
    def mcts(self, thoughts, iterations=10):
        root = MCTSNode(None, thoughts)
        for _ in range(iterations):
            node = root
            while node.children:
                node = node.select_child()
            if not node.is_terminal():
                node.expand()
            score = node.simulate()
            node.backpropagate(score)
        return max(root.children, key=lambda c: c.visits).thought

class MCTSNode:
    def __init__(self, parent, thoughts):
        self.parent = parent
        self.thoughts = thoughts
        self.children = []
        self.visits = 0
        self.score = 0
        self.thought = random.choice(thoughts) if thoughts else None

    def select_child(self):
        return max(self.children, key=lambda c: c.uct())

    def expand(self):
        for thought in self.thoughts:
            self.children.append(MCTSNode(self, self.thoughts))

    def simulate(self):
        return random.random()  # Placeholder for actual simulation

    def backpropagate(self, score):
        self.visits += 1
        self.score += score
        if self.parent:
            self.parent.backpropagate(score)

    def is_terminal(self):
        return len(self.thoughts) == 0

    def uct(self, c=1.41):
        if self.visits == 0:
            return float('inf')
        return (self.score / self.visits) + c * ((2 * self.parent.visits / self.visits) ** 0.5)

class THOUGHTSCULPT(dspy.Module):
    def __init__(self, num_thoughts=3):
        super().__init__()
        self.evaluate = Evaluator()
        self.generate = Generator()
        self.simulate = DecisionSimulator()
        self.num_thoughts = num_thoughts

    def forward(self, instruction, initial_thought, max_iterations=3):
        thought = initial_thought
        for _ in range(max_iterations):
            evaluation = self.evaluate(thought)
            new_thoughts = [
                self.generate(instruction, thought, evaluation.feedback).new_thought 
                for _ in range(self.num_thoughts)
            ]
            thought = self.simulate(new_thoughts)
        return dspy.Prediction(
            instruction=instruction,
            initial_thought=initial_thought,
            final_thought=thought,
            feedback=evaluation.feedback,
            score=evaluation.score
        )

def generate_trainset(num_examples=20):
    instructions = [
        "Write a short story about a robot learning to paint.",
        "Describe a futuristic city powered entirely by renewable energy.",
        "Explain the concept of time travel to a 5-year-old."
    ]
    trainset = []
    for _ in range(num_examples):
        instruction = random.choice(instructions)
        initial_thought = f"Initial thought for: {instruction}"
        example = dspy.Example(instruction=instruction, initial_thought=initial_thought)
        trainset.append(example.with_inputs('instruction', 'initial_thought'))
    return trainset

def improved_thought_evaluation(example, pred, trace=None, frac=0.5):
    rouge = Rouge()
    model = SentenceTransformer('all-MiniLM-L6-v2')

    def normalize_text(text):
        return ' '.join(text.lower().split())

    def calculate_rouge(prediction, ground_truth):
        scores = rouge.get_scores(prediction, ground_truth)
        return scores[0]['rouge-l']['f']

    def calculate_semantic_similarity(prediction, ground_truth):
        embeddings1 = model.encode([prediction], convert_to_tensor=True)
        embeddings2 = model.encode([ground_truth], convert_to_tensor=True)
        return util.pytorch_cos_sim(embeddings1, embeddings2).item()

    prediction = normalize_text(pred.final_thought)
    ground_truth = normalize_text(example.initial_thought)

    rouge_score = calculate_rouge(prediction, ground_truth)
    semantic_similarity = calculate_semantic_similarity(prediction, ground_truth)

    combined_score = (rouge_score + semantic_similarity) / 2

    return combined_score >= frac

def evaluate(compiled_thoughtsculpt, devset):
    results = []
    for example in devset:
        try:
            pred = compiled_thoughtsculpt(example.instruction, example.initial_thought)
            score = improved_thought_evaluation(example, pred)
            results.append(score)
        except Exception as e:
            logging.error(f"Error evaluating example: {e}")
    return sum(results) / len(results) if results else 0

def main():
    try:
        # Setup and compilation
        dataset = generate_trainset()
        trainset = dataset[:-5]
        devset = dataset[-5:]

        thoughtsculpt_instance = THOUGHTSCULPT()

        teleprompter = BootstrapFewShotWithRandomSearch(
            metric=improved_thought_evaluation,
            num_candidate_programs=10,
            max_bootstrapped_demos=4,
            max_labeled_demos=16,
            max_rounds=2,
            num_threads=1,
            max_errors=10
        )

        compiled_thoughtsculpt = teleprompter.compile(thoughtsculpt_instance, trainset=trainset, valset=devset)

        # Save the compiled program
        compiled_program_json = compiled_thoughtsculpt.save("compiled_thoughtsculpt.json")
        print("Program saved to compiled_thoughtsculpt.json")

        # Evaluate the compiled program
        results = evaluate(compiled_thoughtsculpt, devset)
        print("Evaluation Results:")
        print(results)

        # Interactive loop
        while True:
            instruction = input("Enter an instruction (or 'quit' to exit): ")
            if instruction.lower() == 'quit':
                break
            initial_thought = input("Enter an initial thought: ")
            try:
                prediction = compiled_thoughtsculpt(instruction, initial_thought)
                print(f"Instruction: {prediction.instruction}")
                print(f"Initial Thought: {prediction.initial_thought}")
                print(f"Final Thought: {prediction.final_thought}")
                print(f"Feedback: {prediction.feedback}")
                print(f"Score: {prediction.score}")
            except Exception as e:
                logging.error(f"Error during prediction: {e}")
                print("An error occurred while processing the instruction. Please try again.")

    except Exception as e:
        logging.error(f"An error occurred in the main execution: {e}")
        print("An error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main()
    print("Thank you for using THOUGHTSCULPT.")