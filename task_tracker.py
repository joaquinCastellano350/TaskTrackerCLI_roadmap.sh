import json
import argparse
import os
from datetime import datetime

# Making parser
parser = argparse.ArgumentParser(
    prog='Receive ADD task command',
    description='ADD command will be used for adding task in task_tracker',
    epilog='Example usage: python3 task_tracker.py filename.json -a "New Task"'
)

# Adding argument
parser.add_argument('-a', '--add', help='Fill the task to add', required=False)
parser.add_argument(
    '-l', '--list', help='type -l "todo" or "in progress" or "done" or "all" for showing tasks', required=False)
parser.add_argument('-p', '--pick', help='Pick which id', required=False)
parser.add_argument(
    '-u', '--update', help='Type new description', required=False)
parser.add_argument(
    '-m', '--mark', help='Type "in progress" or "done"', required=False)
parser.add_argument(
    '-d', '--delete', help='Just type del', required=False)


# Processing argument
args = parser.parse_args()

# Condition for pick and update

# Accessing arguments
print(f'Added: {args.add if args.add else "No task added"}')
print(f'List: {args.list if args.list else "No list choosed"}')
print(f'id: {args.pick if args.pick else "No id choosed"}')
print(f'update: {args.update if args.update else "Nothing updated"}')
print(f'mark: {args.mark if args.mark else "Nothing marked"}')
print(f'delete: {args.delete if args.delete else "Nothing marked"}')


file_path = 'test_tasks.json'

# Formatting time to dd-mm-yy HH:MM
current_time = datetime.now()
formatted_time = current_time.strftime('%H:%M %d %B %Y')


# List Tasks
def show_tasks_list(status):
    with open('test_tasks.json', 'r') as file:
        data = json.load(file)

    if status == 'all':
        # This will show all tasks
        print('This is all tasks')
        print(json.dumps(data, indent=4))

    elif status == 'todo':
        # This will show all task 'todo'
        todo_tasks = [task for task in data if task.get('status') == 'todo']
        print('This is all todo tasks')
        print(json.dumps(todo_tasks, indent=4))

    elif status == 'in progress':
        # This will show all task 'in progress'
        in_progress_tasks = [
            task for task in data if task.get('status') == 'in progress']
        print('This is all in progress tasks')
        print(json.dumps(in_progress_tasks, indent=4))

    elif status == 'done':
        # This will show all task 'done'
        tasks_done = [task for task in data if task.get('status') == 'done']
        print('This is all done tasks')
        print(json.dumps(tasks_done, indent=4))

    else:
        print('There is something wrong')
        exit()


# Get task based on 'id' and update description
def update_task_baseon_id():
    with open('test_tasks.json', 'r') as file:
        data = json.load(file)

        task_found = False
        for task in data:
            if task['id'] == int(args.pick):
                task['description'] = str(args.update)
                task['updatedAt'] = formatted_time
                task_found = True
                break

        if task_found:
            # Save update to json
            with open('test_tasks.json', 'w') as file:
                json.dump(data, file, indent=4)
            print(f'Task description from id {args.pick}')
            print(f'has been updated to {args.update}')


# Get task based on 'id' and mark task status
def mark_task_baseon_id():
    with open('test_tasks.json', 'r') as file:
        data = json.load(file)

        task_found = False
        for task in data:
            if task['id'] == int(args.pick):
                task['status'] = str(args.mark)
                task['updatedAt'] = formatted_time
                task_found = True
                break

        if task_found:
            # Save update to json
            with open('test_tasks.json', 'w') as file:
                json.dump(data, file, indent=4)
            print(f'Task status from id {args.pick}')
            print(f'has been marked {args.mark}')


# Insert arguments into a JSON file
def add_to_json():
    # value args.add into variable named tasks
    tasks = args.add
    # condition if json file not exist then make one
    if not os.path.exists(file_path):
        # turn task into a dictionary because it's a new json file
        tasks = [
            {
                'id': 1,
                'description': args.add,
                'status': 'todo',
                'createdAt': formatted_time,
                'updatedAt': formatted_time
            }
        ]
        with open(file_path, 'w') as file:
            json.dump(tasks, file, indent=4)

    # if exist, add into existing json
    else:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Getting last id from json file
            last_id = max(item['id'] for item in data) if data else 0
            new_task = {
                'id': last_id + 1,
                'description': args.add,
                'status': 'todo',
                'createdAt': formatted_time,
                'updatedAt': formatted_time
            }
            data.append(new_task)
            # data['description'] = tasks

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

# Delete base on which id picked


def delete_task_baseon_id():
    with open('test_tasks.json', 'r') as file:
        data = json.load(file)

        task_to_remove = None
        for task in data:
            if task['id'] == int(args.pick):
                task_to_remove = task
                task_found = True
                break

        if task_to_remove:
            data.remove(task_to_remove)
            # Save update to json
            with open('test_tasks.json', 'w') as file:
                json.dump(data, file, indent=4)
            print(f'Task status from id {args.pick}')
            print(f'has been deleted {args.delete}')


if args.add:
    add_to_json()

elif args.list:
    show_tasks_list(str(args.list))

elif args.pick:
    if args.update:
        update_task_baseon_id()
    elif args.mark:
        mark_task_baseon_id()
    elif args.delete:
        delete_task_baseon_id()
    else:
        parser.error('For pick, you must specify either --update or --mark')

else:
    exit()
