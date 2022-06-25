Table of Contents
- [Final Project - Distributed Computing](#final-project---distributed-computing)
  * [Objective](#objective)
  * [A Word of Caution](#a-word-of-caution)
  * [Overview and Terminology](#overview-and-terminology)
  * [What Do You Need in order to Participate as One of the Different Roles?](#what-do-you-need-in-order-to-participate-as-one-of-the-different-roles-)
  * [The Server](#the-server)
    + [Installation and Running the Server](#installation-and-running-the-server)
    + [Methods](#methods)
    + [Safeguards](#safeguards)
  * [The Library - "yahavdc"](#the-library----yahavdc-)
    + [Instalation](#instalation)
    + [How to Use "yahavdc"](#how-to-use--yahavdc-)
      - [The Class Decorator Factory - Distribute](#the-class-decorator-factory---distribute)
        * [The Special Functions](#the-special-functions)
        * [The Attributes](#the-attributes)
      - [Initiate the Project](#initiate-the-project)
      - [Results and Statistics](#results-and-statistics)
  * [The Client Side Application](#the-client-side-application)
    + [Installation and Running the Client Side Application](#installation-and-running-the-client-side-application)
    + [Actions](#actions)
      - [Tasks](#tasks)
      - [Users](#users)
    + [How to Use](#how-to-use)

# Final Project - Distributed Computing

This repository contains my finale project in computer science for the Ministry of Education.

## Objective

The objective of this project is to create a platform which allows anyone to create and execute programs in a parallel and distributed form, using the computational power of their own or a group's devices.

## A Word of Caution

Please note that security was not a major concern in the development of this project. As such, it may not be secure.  
Additionally, running untrusted code from an untrusted or unknown source may pose a security risk and is not recommended. Therefore, it is recommended to allow access to the server exclusively for trusted devices.  
Yahav Reuven is not liable for any damages caused by or from the use of this code by anyone.

## Overview and Terminology

In order to achieve the objective of this project, three basic abilities are needed:

1. Create a project.
2. Execute tasks (part of a project).
3. Manage the communication.
Therefore, there are three parts to this project:

* A server which manages the communication between all of the clients.  
* A client side application which allows the connection with the server and to execute different tasks (such clients are called "Workers").
* A python library called `yahavdc` which allows the creation of distributed projects (such clients are called "Creators")

## What Do You Need in order to Participate as One of the Different Roles?

A server - needs only the server application installed.  
A worker - needs only the client side application installed.  
A creator - needs both the client side application and the library `yahavdc` installed.  

## The Server

The server handles all of the communication between all of the clients.

### Installation and Running the Server

To install and run the server:

```shell
git clone https://github.com/YahavReuven/Final-Project.git
cd ./Final-Project/Server
pip install -r requirements.txt
python server.py
```

###### Note

The server listens on port 8080.

### Methods

The server uses the [FastAPI](https://fastapi.tiangolo.com) python library and communicates with HTTP.
The server provides its services through the following URI's:

1. Handle clients:
    * `/register_device` - Used to register a new client to the server and allow it to perform as a "Creator" or a "Worker". Returns a unique string id used to identify the client.

2. Handle projects:
    * `/upload_new_project` - Used by a creator to upload a new project to be distributed to the workers and executed. Receives the JSON object representation of `NewProject`. Returns a unique string id used to identify the project.
    * `/get_project_results` - Used by a creator to receive the results of a project. Receives the id of the creator and the project's id./ Returns a JSON object representation of `ReturnedProject`. If the project is not finished yet, will return an appropriate response.

3. Handle Tasks:
    * `/get_new_task` - Used by a worker to receive a new task to execute. Receives the worker's id. Returns the JSON object representation of `SentTask`.
    * `/upload_task_results` - Used by a worker to upload the results and statistics generated from the execution of the task. Receives the JSON object representation of `ReturnedTask`.

<!-- 
maybe add block, unblock and view permissions
s-->

### Safeguards

In case a worker takes too long to execute the task, there is a safeguard which frees the task to bu executed again. The delay before freeing the task is global and set in `SENT_TASK_VALIDITY`.

## The Library - "yahavdc"

`yahavdc` is a python library which enables the clients to create distributed projects and become a creator.

### Instalation

To install "yahavdc":

```shell
git clone https://github.com/YahavReuven/Final-Project.git
cd ./Final-Project/yahavdc
pip install -r requirements.txt
```

###### Note

There isn't a `setup.py` file. you may install the library yourself, or install the library in the same directory as your project.

### How to Use "yahavdc"

Here is a visual representation of a general use of the library:

```python
from yahavdc import Distribute

@Distribute(...)
class Project:

    @staticmethod  # or @classmethod
    def parallel_function(...):
        ...

    # def other_functions(...):
    #   ...

project = Project()
# Do something
results = project.get_results()

```

Explanation of the code:
    1. First import all of the needed abilities from the library.
    2. Create a project class and decorate it with `Distribute`.
        * The class should include the special functions as discussed below.
    3. Initiate the project.
    4. Claim the results when needed.

###### Note

Claiming the results will block until the results are returned. Thus, it should be called only when the results are absolutely necessary. It is encouraged to write any piece of code you can in between the initialization of the project and claiming the results.

#### The Class Decorator Factory - Distribute

`Distribute` is the heart of the `yahavdc` library. It handles the project in the client side. As shown before, it should decorate the project class.

##### The Special Functions

Inside of the project there may be a special functions which hold more responsibilities.

* **"parallel" function** - A parallel function is the first function which the worker execute, every time with a different value from the sliced iterator. This is the main function and thus is mandatory to implement. The default name for this function is `parallel_func`. The function should receives only the iterator value as a parameter (except `cls` or known values).
* **"stop" function** - A stop function is an optional special function. It allows to stop the project if a certain requirement is met. If it is implemented, it is called after the parallel function and checks its return value. If by python truthfulness, the return value is `True` the server will stop the execution of the project and mark it as finished. It should receive only the return value ot the parallel function as a parameter (except `cls` or known values).

###### Note

If this function is implemented the project results will consist solely of the iteration which
met the function's requirement.

* **"only if" function** - An only if function is also an optional special function. It allows to return only the results which met a certain requirement. If it is implemented, it is called after the parallel function and checks its return value. If by python truthfulness, the return value is `True`, the result will be returned to the server, otherwise it will be discarded. It should receive only the return value ot the parallel function as a parameter (except `cls` or known values).

###### Note

The use of both the "parallel function" and the "only if function" is **not** supported, and will raise an error.

##### The Attributes

* **`user_name`** - The name which ids the server.
* **`iterator`** - The full iterator which holds the values with which to execute the project.  
* **`tak_size`** - The size of each task.
* **`results_path`** - The path in which to save the results.
* **`parallel_func`** - The name of the parallel function. The default name is `parallel_func`.
* **`stop_func`** - Optional. The name of the stop function
* **`only_if_func`** - Optional. The name of the only if function.
* **`modules`** - Optional. A list of all of the needed modules in order to execute the project. Currently supports only built-in python modules.

#### Initiate the Project

When initiating the project it will be sent to the server and the workers will be able to execute it. The object should be saved in order to receive the results.

#### Results and Statistics

When a project is finished it will return its results and statistics.

The statistics include different information regarding the timing of the project. They will be saved as a JSON in a file named `stats.json` in the results directory `results_path` specified in Distribute.

There are 2 kinds of results:
    * **regular** - A dict object containing the results from the execution of the project such that the key is the iteration value and the value is the return value from the parallel function.
    * **additional results** - Any additional files that were created in the execution of the project. In order to use this feature you must create the files in the path specified in `ADDITIONAL_RESULTS` during the execution of the project.

When the results are needed, call the `.get_reslts()` method. It will block until the results are returned and you will not ba able to run additional commands in the same thread.

## The Client Side Application

The client side application allows the clients to connect to the server and to allow the execution of tasks by the workers.
It is required in order to be both a creator or a worker.

### Installation and Running the Client Side Application

To install and run the client side application:

```shell
git clone https://github.com/YahavReuven/Final-Project.git
cd ./Final-Project/Client
pip install -r requirements.txt
python app.py
```

### Actions

The application provides 2 basic functions:
    * Execution of tasks.
    * Creation of users.

#### Tasks

This is the main purpose of the client side application.  

A task is a part of the overall project which needs to be executed. Essentially it is made from the project's code and a part of the full iterator. The execution of a task means "To execute the parallel function and the other special functions (if implemented) described in the project's code, on every value in the sliced iterator".  

The workers can not choose what task to execute, however, they can choose how many tasks the wish to run in a session.  
This is allowed since the point of this project is to create a distributed system from home computers which are not used solely for the execution of tasks.

#### Users

The second function of the client side application is the creation and use of "Users".

In this project, a "User" is the connection of the client to a specific server. Essentially it is a name which identifies the ip of a server.

Users were created in order to allow clients the ability to connect to different servers, and thus to donate their resources to different projects or use the recourses of different servers, depending on their needs. Additionally, names are used in order to help the clients to connect to the servers without the need to remember their ip's.

It is possible to create different users with the same server ip.

### How to Use

Upon starting the application, you will be asked to enter a user - which is a connection to a server. You may choose the name of an existing user or write a new name - which will allow you to create a new user.

<!-- maybe gif -->

After you chose your user, you will be presented with the main menu.
    * Type "help" to see the help menu.
    * Type "user" to switch to a different user or create a new one.
    * Type "task" to execute tasks.
    * Type "exit" to exit the program.

If you choose "task" you will be presented with the task menu, in which you will be able to choose how many tasks you wish to execute.

<!-- maybe gif -->
