# Importing needed modules
import cmd
import os
import json
import datetime

# Functions


def add_task_to_jsonfile(jsonfile, obj):
    with open(jsonfile, "r") as f:
        existent_data = json.load(f)

    existent_data.append(obj)
    if len(existent_data) != 0:
        existent_data.sort(key=lambda x: x["id"])
    with open(jsonfile, "w") as f:
        json.dump(existent_data, f, indent=4)


def generate_id(jsonfile):
    with open(jsonfile, "r") as f:
        list = json.load(f)

    if len(list) > 0:
        id = list[-1]["id"] + 1
    else:
        id = 1
    return id


def search_task(jsonfile, task_id):
    with open(jsonfile, "r") as f:
        list = json.load(f)
    try:
        tid = int(task_id)
    except Exception as e:
        print("The entered task id is not a number!")
    for task in list:
        if task["id"] == tid:
            return task

    print(f"The entered id doesn't match with any loaded task.")
    return


def del_task(jsonfile, task_id):
    with open(jsonfile, "r") as f:
        list_req = json.load(f)

    try:
        tid = int(task_id)
        list = [x for x in list_req if x["id"] != tid]
        if list == list_req:
            print("There is no task with entered id")
    except Exception as e:
        print("The entered task id is not a number!")

    with open(jsonfile, "w") as f:
        json.dump(list, f, indent=4)


def list_tasks(jsonfile, status):
    with open(jsonfile, "r") as f:
        task_list = json.load(f)

    shown_tasks = [x for x in task_list if status in x["status"]]
    for task in shown_tasks:
        print(task)
        print(f"\n")


# CMD Functionality


class TaskTrackerCLI(cmd.Cmd):
    prompt = "TaskTracker>> "
    intro = 'Welcome to TaskTracker CLI. Type "help" for available commands.'
    FILE = "task_tracker.json"

    def do_add(self, task):
        """Add a task to the list"""
        obj = {
            "id": generate_id(self.FILE),
            "description": task,
            "status": "todo",
            "createdAt": datetime.datetime.now().strftime("%c"),
            "updatedAt": datetime.datetime.now().strftime("%c"),
        }

        add_task_to_jsonfile(self.FILE, obj)
        print("Task added correctly")

    def do_update(self, args):
        """Update the description of an existent task"""
        splitted_args = args.split()
        if len(splitted_args) < 2:
            print("Invalid amount of arguments.")
            return

        task_id = splitted_args[0]
        new_task = " ".join(splitted_args[1:])

        task = search_task(self.FILE, task_id)
        if task != None:
            del_task(self.FILE, task_id)
            task["description"] = new_task
            task["updatedAt"] = datetime.datetime.now().strftime("%c")
            add_task_to_jsonfile(self.FILE, task)
            print("Task updated correctly")

    def do_del(self, task_id):
        """Delete an existent task with its id"""
        del_task(self.FILE, task_id)

    def do_mark(self, args):
        """Set the status of an existent task to in-progress, done or todo"""
        splitted_args = args.split()
        if len(splitted_args) != 2:
            print("Invalid amount of arguments.")
            return

        task_id = splitted_args[0]
        state = splitted_args[1]

        if state == "in-progress" or state == "done" or state == "todo":
            task = search_task(self.FILE, task_id)
            if task != None:
                del_task(self.FILE, task_id)
                task["status"] = state
                task["updatedAt"] = datetime.datetime.now().strftime("%c")
                add_task_to_jsonfile(self.FILE, task)
                print("Task status modified correctly")
        else:
            print(
                "The entered status is not valid. Try using 'in-progress', 'done' or 'todo'"
            )

    def do_list(self, args):
        splitted_args = args.split()
        if len(splitted_args) > 1:
            print("Invalid amount of arguments.")
            return

        list_tasks(self.FILE, args)


if __name__ == "__main__":
    TaskTrackerCLI().cmdloop()
