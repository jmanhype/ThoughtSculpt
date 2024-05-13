# cli/main.py
import click
from thoughtsculpt.utils.logger import get_logger

logger = get_logger(__name__)

@click.group()
def cli():
    """ThoughtSculpt CLI"""
    pass

@cli.command()
@click.option("--task-description", "-t", required=True, help="Task description")
@click.option("--initial-solution", "-i", required=True, help="Initial solution")
@click.option("--max-depth", "-d", type=int, default=3, help="Maximum depth")
@click.option("--num-simulations", "-s", type=int, default=10, help="Number of simulations")
def sculpt(task_description, initial_solution, max_depth, num_simulations):
    """Sculpt a thought using ThoughtSculpt"""
    logger.debug("Starting the sculpt command")
    from thoughtsculpt.services.thought_process import ThoughtProcess

    thought_process = ThoughtProcess(task_description, initial_solution, api_key)
    final_solution = thought_process.sculpt_thought(max_depth, num_simulations)
    logger.info(f"Final solution: {final_solution}")

if __name__ == "__main__":
    cli()
    cli()