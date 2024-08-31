from typing import Callable, Final, Iterable
import argparse
import json
import os

DATA_FILE_NAME: Final[str] = "./data.json"
AVAILABLE_STATUS: Final[tuple[str, str, str]] = ("todo", "in-progress", "done")

class Task:

    def __init__(self) -> None:

        # CLI Configrations
        self.__data: dict[str, list[dict[str, str | int]]] = {"tasks": []}

        parser = argparse.ArgumentParser(
            prog="task-cli", # name of the app to use when the script is added to env path
            description="Task Tracker CLi"
        )
        subparser = parser.add_subparsers(dest="command", help="commands")

        # list command
        list_command = subparser.add_parser("list", help="List all the tasks")
        list_command.add_argument("status", type=str, nargs="?", choices=AVAILABLE_STATUS, help="list Tasks by status (optional)")

        # add command
        add_command = subparser.add_parser("add", help="add a task")
        add_command.add_argument("name", type=str, help="Task Name")

        # delete command
        delete_command = subparser.add_parser("delete", help="delete a task")
        delete_command.add_argument("id", type=int, help="Task ID")

        # update command
        update_command = subparser.add_parser("update", help="update a task")
        update_command.add_argument("id", type=int, help="Task ID")
        update_command.add_argument("name", type=str, help="New Name for the Task")

        # mark command
        mark_command = subparser.add_parser("mark", help="mark a task")
        mark_command.add_argument("id", type=int, help="Task ID")
        mark_command.add_argument("status", type=str, choices=AVAILABLE_STATUS, help="Change the Task status")

        self.args = parser.parse_args()

        if self.args.command:
            self.load_data()
            self.handel_subcommands()

    def handel_subcommands(self) -> None:
        "handel the subcommands"

        commands: dict[str, Callable[[], None]] = {
            "list": self.list_tasks,
            "add": self.add_task,
            "delete": self.delete_task,
            "update": self.update_task,
            "mark": self.mark_task,
        }

        action: Callable[[], None] | None = commands.get(self.args.command)
        if action:
            action()

    def get_task_index(self, id: int) -> int | None:
        """
        get the task index from the `__data`
        
        Args:
            id (int): the task id
        """
        try:
            item = list(filter(lambda data: data["id"] == id, self.__data["tasks"]))
            if len(item) == 1:
                return self.__data["tasks"].index(item[0])
            elif len(item) > 1:
                print("Error, Found More Than 1 id!!!!!!")
            else:
                print(f"No Task Found with id {id} Not Found")
        except:
            print(f"No Task Found with id {id} Not Found")

    def mark_task(self) -> None:
        "set the task status by id with one of the available status"

        index: int | None = self.get_task_index(int(self.args.id))

        if index is None:
            return

        self.__data['tasks'][index]['status'] = self.args.status
        self.save_data()
        print("\nMarked Successfully.")

    def update_task(self) -> None:
        "update the task name by id"

        index: int | None = self.get_task_index(int(self.args.id))
        if index is None:
            return

        self.__data["tasks"][index]["name"] = self.args.name
        self.save_data()
        print("\nUpdated Successfully.")

    def delete_task(self) -> None:
        "delete task by id"

        index: int | None = self.get_task_index(int(self.args.id))
        if index is not None:
            self.__data['tasks'].pop(index)
            self.save_data()
            print("\nDeleted Successfully.")

    def add_task(self) -> None:
        """
        add a new task with the name
        
        the `id` is auto generated based on the last id in the data file
        """
        name: str = self.args.name

        id = self.last_id + 1

        self.__data["tasks"].append({"id": id, "name": name, "status": "todo"})
        print(f"Adding Task with id: {id}")
        self.save_data()
        print("\nAdded Successfully.")

    def list_tasks(self) -> None:
        "show all the exists tasks by status"

        # if no status provided then show all the tasks
        if self.args.status is None:
            print("Listing All tasks....\n")
            self.display_tasks(self.__data['tasks'])

            print("\nOK")
            return

        print(f"Listing {self.args.status} tasks....\n")
        dt = filter(lambda data: data["status"] == self.args.status, self.__data["tasks"])
        self.display_tasks(dt)
        print("\nOK")

    def display_tasks(self, tasks: Iterable[dict[str, str | int]]) -> None:
        """
        prints the tasks in a nice format
        Args:
            tasks (Iterable[dict[str, str | int]]): the tasks to display as Iterable that containes `dict`
        """
        for i in tasks:
            print(f"ID: {i['id']} - Task Name: {i['name']} - Status: {i['status']}")

    @property
    def last_id(self) -> int:
        """Return the last task ID or 0 if no tasks exist."""
        return int(self.__data["tasks"][-1]["id"]) if self.__data["tasks"] else 0

    def save_data(self) -> None:
        """Save task data to the data file."""
        with open(DATA_FILE_NAME, "w") as f:
            json.dump(self.__data, f, indent=4)

    def load_data(self) -> None:
        """Load task data from the data file."""
        if not os.path.exists(DATA_FILE_NAME):
            self.create_data_file()

        with open(DATA_FILE_NAME, "r") as f:
            self.__data = json.load(f)

    def create_data_file(self) -> None:
        """Create an empty data file if it doesn't exist."""
        with open(DATA_FILE_NAME, "w") as f:
            json.dump({"tasks": []}, f, indent=4)


def main():
    Task()
