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

    with open(jsonfile, "w") as f:
        json.dump(existent_data, f, indent=4)


def generate_id(jsonfile):
    with open(jsonfile, "r") as f:
        list = json.load(f)

    if len(list) == 0:
        id = 1
    else:
        id = list[-1]["id"] + 1
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

    print(f"The entered id doesn't match with any tasks loaded.")
    return


def del_task(jsonfile, task_id):
    with open(jsonfile, "r") as f:
        list = json.load(f)

    try:
        tid = int(task_id)
        list = [x for x in list if x["id"] != tid]
    except Exception as e:
        print("The entered task id is not a number!")

    with open(jsonfile, "w") as f:
        json.dump(list, f, indent=4)


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
            add_task_to_jsonfile(self.FILE, task)

    def do_del(self, task_id):
        del_task(self.FILE, task_id)

    def do_state(self, task, arg):
        pass

    def do_list(self, arg):
        pass


if __name__ == "__main__":
    TaskTrackerCLI().cmdloop()
