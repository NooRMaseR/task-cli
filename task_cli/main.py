from typing import Final, Iterable
import argparse
import json
import os


class Task:

    def __init__(self) -> None:

        # CLI Configrations
        self.__data: dict[str, list[dict[str, str | int]]] = {"tasks": []}
        self.__data_file_name: Final[str] = "./data.json"
        self.__available_status: tuple[str, str, str] = ("todo", "in-progress", "done")

        self.parser = argparse.ArgumentParser(
            prog="task-cli", # name of the app to use when the script is added to env path
            description="Task Tracker CLi"
        )
        self.subparser = self.parser.add_subparsers(dest="command", help="commands")

        # list command
        self.list_command = self.subparser.add_parser("list", help="List all the tasks")
        self.list_command.add_argument("status", type=str, nargs="?", choices=self.__available_status, help="list Tasks by status (optional)")

        # add command
        self.add_command = self.subparser.add_parser("add", help="add a task")
        self.add_command.add_argument("name", type=str, help="Task Name")

        # delete command
        self.delete_command = self.subparser.add_parser("delete", help="delete a task")
        self.delete_command.add_argument("id", type=int, help="Task ID")

        # update command
        self.update_command = self.subparser.add_parser("update", help="update a task")
        self.update_command.add_argument("id", type=int, help="Task ID")
        self.update_command.add_argument("name", type=str, help="New Name for the Task")

        # mark command
        self.mark_command = self.subparser.add_parser("mark", help="mark a task")
        self.mark_command.add_argument("id", type=int, help="Task ID")
        self.mark_command.add_argument("status", type=str, choices=self.__available_status, help="Change the Task status")

        self.args = self.parser.parse_args()
        
        if self.args.command:
            self.load_data()
            self.handel_subcommands()

    def handel_subcommands(self) -> None:
        "handel the subcommands"

        match self.args.command:
            case "list":
                self.list_tasks()

            case "add":
                self.add_task()

            case "delete":
                self.delete_task()

            case "update":
                self.update_task()

            case "mark":
                self.mark_task()

    def get_task_index(self, id: int) -> int | None:
        """
        get the task index from the `__data`
        
        Args:
            id (int):
                the task id
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

    @property
    def last_id(self) -> int:
        "get the last id from the data file"
        try:
            last_id: int =  int(self.__data["tasks"][-1]["id"])
        except:
            last_id = 0

        return last_id

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
            tasks (Iterable[dict]):
                the tasks to display as Iterable that containes `dict`
        """
        for i in tasks:
            print(f"ID: {i['id']} - Task Name: {i['name']} - Status: {i['status']}")

    def save_data(self) -> None:
        "save the new data from `__data`"
        ids: list[int] = []

        # check if an id exists twice
        for i in self.__data["tasks"]:
            if i["id"] in ids:
                print("this id is already exists")
                return

            ids.append(int(i["id"]))

        with open(self.__data_file_name, "w") as f:
            json.dump(self.__data, f, indent=4)


    def load_data(self) -> None:
        "load the data from the data file and assing the data to `__data`"
        print(f"Loading data....", end=" ")

        self.check_file()
        with open(self.__data_file_name, "r") as f:
            self.__data = json.load(f)

        print("OK")

    def check_file(self) -> None:
        "check if the data file is exists, if not then create a new empty one"
        if not os.path.exists(self.__data_file_name):
            with open(self.__data_file_name, "w") as f:
                json.dump(self.__data, f, indent=4)
            print("OK")

def main():
    Task()
