<h1 style="text-align: center;">Tasks Tracker CLI</h1>
this cli made with Python

## Setup
in the same dir open the terminal and type
```bash
pip install .
```

this will install the script as a `cli` in python packages, works as cross platform

## Usage
```bash
task-cli -h
```

output:
```bash
usage: task-cli [-h] {list,add,delete,update,mark} ...

Task Tracker CLi

positional arguments:
  {list,add,delete,update,mark}
                        commands
    list                List all the tasks
    add                 add a task
    delete              delete a task
    update              update a task
    mark                mark a task

options:
  -h, --help            show this help message and exit
```

## Adding a Task
```bash
task-cli add "this is task 1"
```

output:
```bash
Loading data.... OK
Adding Task with id: 1

Added Successfully.
```

## List Tasks
```bash
task-cli list
```

output:
```bash
Loading data.... OK
Listing All tasks....

ID: 1 - Task Name: this is task 1 - Status: todo

OK
```
adding filter
```bash
task-cli list todo
```

output:
```bash
Loading data.... OK
Listing todo tasks....

ID: 1 - Task Name: this is task 1 - Status: todo

OK
```

## Update a Task
```bash
task-cli update <id> <"new name">
```

like this
```bash
task-cli update 1 "this is updated task 1"
```

output:
```bash
Loading data.... OK

Updated Successfully.
```

let's check
```bash
task-cli list
```

output
```bash
Loading data.... OK
Listing All tasks....

ID: 1 - Task Name: this is updated task 1 - Status: todo

OK
```

## Delete a Task
```bash
task-cli delete <id>
```

like this
```bash
task-cli delete 1
```

output:
```bash
Loading data.... OK

Deleted Successfully.
```

## Change The Task Mark
```bash
task-cli mark <id> <mark-name>
```

like this
```bash
task-cli mark 1 in-progress
```

output:
```bash
Loading data.... OK
No Task Found with id 1 Not Found
```
that's because we have just delete it, let's create it again

```bash
task-cli add "this is task 1"
```

then we mark it
```bash
task-cli mark 1 in-progress
```

output:
```bash
Loading data.... OK

Marked Successfully.
```

call with `-h` to see the available marks

# Summary
Task-cli is a command line tool for managing tasks. It allows you to add, delete, and mark tasks. 

You can use it to manage your tasks from the command line.

```bash
# show help
task-cli -h

# list tasks
task-cli list

# list tasks with filter
task-cli list todo

# add task
task-cli add "this is task 1"

# update task
task-cli update 1 "new task name"

# delete task
task-cli delete 1

# mark task
task-cli mark 1 in-progress
```

<h1 style="text-align: center;">That's it</h1>
for more informations vist <a href="https://roadmap.sh/projects/task-tracker">roadmap task-tracker cli</a>
