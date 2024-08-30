import click
from notion_client import Client
from datetime import datetime, timezone

from rich import box
from rich import print
from rich.prompt import Prompt
from rich.panel import Panel
from rich.traceback import install

install(show_locals=True)

NOTION_TOKEN = "secret_HIVva1cIRHa6OUTr2HlWJGIEgiY57n67XhRPJYB1v3"
DATABASE_ID = "81905f0c5b474254b19e8cf84fb2e83d"

def new_todo(client, notion_database_id):
          name = Prompt.ask("Write the task name")
          todo_type = Prompt.ask("What type of task is it ?", choices=["Academics", "Biz chore", "Chore", "Idea Development", "Business Development", "Business Study", "Revision", "Design", "Coding", "Coding Study", "Notes"])
          project = Prompt.ask("What project are you working on ?", choices=["Micro SaaS", "Reachify", "Clipify", ""])
          todo_status = Prompt.ask("What is the current task status ?", choices=["Not started", "In progress", "Done", "On Hold"])
          todo_deadline = Prompt.ask("Is there a deadline ?")
          
          panel_style = ""
          
          if todo_type == "Academics" or "Idea Development":
                    panel_style = "Yellow"
          elif todo_type == "Biz chore" or "Chore" or "Notes":
                    panel_style = "Orange"
          elif todo_type == "Design" or "Business Study":
                    panel_style = "Blue"
          elif todo_type == "Coding" or "Coding Study":
                    panel_style = "Green"
          elif todo_type == "Revision":
                    panel_style == "Red"
          
          # Prepare properties dynamically based on input
          properties = {
              'Name': {'title': [{'text': {'content': name}}]},
              'Status': {'select': {'name': todo_status}},
              'Type': {'multi_select': [{'name': todo_type}]},
          }

          # Conditionally add 'Project' property if not empty
          if project:
              properties['Project'] = {'select': {'name': project}}
          
          # Conditionally add 'Deadline' property if not empty
          if todo_deadline:
              properties['Deadline'] = {'date': {'start': todo_deadline}}

          # Create the page
          client.pages.create(
              **{
                  "parent": {"database_id": notion_database_id},
                  'properties': properties
              }
          )
          
          print(Panel.fit(f"Created To do task under [u]{todo_type}[/u] category\n[b]Current Status[/b] : {todo_status}\n[b]Deadline[/b] : {todo_deadline}", title=f"{name}", border_style=f"bold {panel_style}", box=box.SQUARE))

def get_task_page_id(client, database_id, task_name):
    try:
        # Query the database to find the page ID of the task
        response = client.databases.query(
            **{
                "database_id": database_id,
                "filter": {
                    "property": "Name",
                    "title": {
                        "equals": task_name  # Filter by task name
                    }
                }
            }
        )
        
        # Check if there are any results
        if response['results']:
            # Get the page_id of the first matching result
            page_id = response['results'][0]['id']
            return page_id
        else:
            print("Task not found.")
            return None

    except Exception as e:
        print(f"An error occurred while retrieving the task: {e}")
        return None

def get_tasks_by_type(client, database_id, task_type):
    """
    Retrieve tasks based on the task type from the Notion database.
    """
    try:
        # Query the database to find tasks of the specified type
        response = client.databases.query(
            **{
                "database_id": database_id,
                "filter": {
                    "property": "Type",
                    "multi_select": {
                        "contains": task_type  # Filter by task type
                    }
                }
            }
        )
        
        # Extract task names and page_ids from the results
        tasks = [(result['properties']['Name']['title'][0]['text']['content'], result['id']) for result in response['results']]
        return tasks

    except Exception as e:
        print(f"An error occurred while retrieving tasks: {e}")
        return []

def update_task_status(client, page_id, new_status):
    """
    Update the status of a task in the Notion database.
    """
    try:
        # Update the page (task) with a new status
        client.pages.update(
            **{
                "page_id": page_id,
                "properties": {
                    "Status": {
                        "select": {"name": new_status}  # Update the "Status" property
                    }
                }
            }
        )
        print(f"Task with ID {page_id} successfully updated to status: {new_status}")

    except Exception as e:
        print(f"An error occurred: {e}")

def update_database(client, database_id):
    # Step 1: Ask user for task type
    task_type = Prompt.ask(
        "What type of task do you want to update?", 
        choices=["Academics", "Biz chore", "Chore", "Idea Development", "Business Development", "Business Study", "Revision", "Design", "Coding", "Coding Study", "Notes"]
    )
    
    # Step 2: Get tasks of the specified type
    tasks = get_tasks_by_type(client, database_id, task_type)
    
    # Step 3: If tasks are found, display them and let user choose one
    if tasks:
        print(f"Tasks found for type '{task_type}':")
        for index, (task_name, _) in enumerate(tasks):
            print(f"[{index}] {task_name}")
        
        # Let user select which task to update
        task_index = int(Prompt.ask("Enter the number of the task you want to update"))

        # Ensure a valid index is chosen
        if 0 <= task_index < len(tasks):
            selected_task_id = tasks[task_index][1]
            new_status = Prompt.ask("Enter the new status for the task", choices=["Not started", "In progress", "Done", "On Hold"])

            # Step 4: Update the selected task's status
            update_task_status(client, selected_task_id, new_status)
        else:
            print("Invalid selection. Please run the script again and choose a valid task number.")
    else:
        print(f"No tasks found for type '{task_type}'.")

client = Client(auth=NOTION_TOKEN)

@click.command()
@click.option('--create', is_flag=True, help="Create a new todo task.")
@click.option('--update', is_flag=True, help="Update an existing todo task.")
def main(create, update):
    """CLI app for managing Notion tasks."""
    if create:
        new_todo(client, DATABASE_ID)
    elif update:
        update_database(client, DATABASE_ID)
    else:
        print("Please specify an action: --create or --update")

if __name__ == '__main__':
    main()