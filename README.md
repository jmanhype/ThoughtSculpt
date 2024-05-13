# ThoughtSculpt

ThoughtSculpt is a powerful application that leverages large language models (LLMs) to iteratively refine and improve solutions to complex tasks. It combines techniques like Monte Carlo Tree Search (MCTS) and reinforcement learning to explore the solution space and converge on optimal solutions.

## Features

- **Task Description and Initial Solution**: Provide a detailed description of the task you want to solve and an initial solution to start the iterative refinement process.
- **Thought Evaluation**: Leverage LLMs to evaluate the current solution and provide feedback on its strengths and weaknesses.
- **Solution Generation**: Based on the feedback, generate multiple candidate solutions using LLMs.
- **Decision Simulation**: Use MCTS to simulate the decision process and select the most promising candidate solution for further refinement.
- **Iterative Refinement**: Repeat the evaluation, generation, and simulation steps to iteratively refine the solution until a satisfactory result is achieved.
- **API and CLI**: Interact with ThoughtSculpt through a RESTful API or a command-line interface (CLI).
- **Extensible Architecture**: Easily integrate with different LLM providers (e.g., OpenAI, Anthropic, Groq) and customize the behavior according to your needs.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/thoughtsculpt.git
```

2. Install the required dependencies:

```bash
cd thoughtsculpt
pip install -r requirements.txt
```

3. Set up the environment variables:

```bash
cp .env.example .env
```

Edit the `.env` file and provide your API keys and other configuration settings.

4. Initialize the database:

```bash
python thoughtsculpt/scripts/initialize_db.py
```

## Usage

### API

1. Start the FastAPI server:

```bash
python -m uvicorn thoughtsculpt.api:app --reload
```

2. Use tools like Postman or curl to interact with the API endpoints:

- `POST /api/thoughtsculpt`: Sculpt a thought by providing a task description and initial solution.
- `POST /api/evaluate`: Evaluate a solution and get feedback.
- `POST /api/generate`: Generate candidate solutions based on feedback.

### CLI

Use the command-line interface to sculpt thoughts:

```bash
python -m thoughtsculpt.cli.main sculpt --task-description "Your task description" --initial-solution "Your initial solution"
```

## Contributing

Contributions are welcome! Please follow the standard GitHub workflow:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [OpenAI](https://openai.com/) for their powerful language models
- [Anthropic](https://www.anthropic.com/) for their innovative AI research
- [Groq](https://groq.com/) for their efficient AI hardware and software solutions