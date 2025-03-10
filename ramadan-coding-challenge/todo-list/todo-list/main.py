import click  
import json  
import os  

TODO_FILE = "todo.json"

def load_todos():
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return [] 

def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

@click.group()
def cli():
    """Simple Todo List Manager"""
    pass

@cli.command()
@click.argument("task")
def add(task):
    """Add a new task to the list"""
    tasks = load_todos()
    tasks.append({"task": task, "done": False})
    save_tasks(tasks)
    click.echo(f"Task added Successfully: {task}")

@cli.command()
def list():
    """List all tasks"""
    tasks = load_todos()
    if not tasks:
        click.echo("No Task Found")
        return
    for index, task in enumerate(tasks):
        status = "Done" if task["done"] else "Not Done"
        click.echo(f"{index + 1}. {task['task']} - {status}")

@cli.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as complete"""
    tasks = load_todos()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as completed")
    else: 
        click.echo("Invalid Task Number")    

@cli.command()
@click.argument("task_number", type=int)
def delete(task_number):
    """Delete a task"""
    tasks = load_todos()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"Task '{removed_task['task']}' deleted")
    else:
        click.echo("Invalid Task Number")

cli.add_command(list)
cli.add_command(complete)
cli.add_command(delete)

if __name__ == "__main__":
    cli()
