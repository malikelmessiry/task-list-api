# Wave 1: CRUD for One Model

## Goal

Our task list API should be able to work with an entity called `Task`.

Tasks are entities that describe a task a user wants to complete. They contain a:

- title to name the task
- description to hold details about the task
- an optional datetime that the task is completed on

Our goal for this wave is to be able to create, read, update, and delete different tasks. We will create RESTful routes for these different operations.

# Requirements

## Task Model

There should be a `Task` model that lives in `app/models/task.py`.

Tasks should contain these attributes. **The tests require the following columns to be named exactly** as `title`, `description`, and `completed_at`.

- `id`: a primary key for each task
- `title`: text to name the task
- `description`: text to describe the task
- `completed_at`: a datetime that represents the date that a task is completed on. **Can be _nullable_,** and contain a null value. A task with a `null` value for `completed_at` has not been completed. When we create a new task, `completed_at` should be `null` AKA `None` in Python.

### Tips

- To work with date information, we can import the `datetime` data type with the import line `from datetime import datetime`. 
- SQLAlchemy supports optional, or _nullable_, columns with specific syntax.
- Don't forget to run:
  - `flask db init` once during setup
  - `flask db migrate` every time there's a change in models, in order to generate migrations
  - `flask db upgrade` to run all generated migrations
- We can assume that the value of each task's `completed_at` attribute will be `None`, until wave 3. (Read below for examples)
- We can assume that the API will designate `is_complete` as `false`, until wave 3. (Read below for examples)

## Model Helper Methods

We have seen that we can define instance methods in our model classes. We should practice those skills here by including model helper methods that can:

- Return a Python dictionary in the shape of the JSON our API expects to return for a model instance.
- Create a new model instance from a dictionary, typically retrieved from the JSON sent as a request body.

## Route Helper Methods

Beyond model helper methods, we should also practice creating route helper methods. Especially in this wave, we should consider creating a route helper method that can:

- Retrieve a model instance by its ID.

We might also consider creating a route helper method that can:

- Handle the creation of new instances of a model from a dictionary, returning the expected responses.

## CRUD for Tasks

### Tips

- Pay attention to the exact shape of the expected JSON. Double-check nested data structures and the names of the keys for any misspellings.
  - That said, remember that dictionaries do not have an implied order. This is still true in JSON with objects. When you make Postman requests, the order of the key/value pairings within the response JSON object does not need to match the order specified in this document. (The term "object" in JSON is analogous to "dictionary" in Python.)
  - Notice that the details for a Task in the response is shared across all the endpoints that return Task details. Rather than repeating the same literal `dict` structure in each response, we should create a helper method that returns the `dict` structure for a Task, and use it in each relevant endpoint. This will ensure that all our responses are consistent.
- Use the tests in `tests/test_wave_01.py` to guide your implementation.
- You may feel that there are missing tests and missing edge cases considered in this wave. This is intentional.
  - You have fulfilled wave 1 requirements if all of the wave 1 tests pass.
  - You are free to add additional features, as long as the wave 1 tests still pass. However, we recommend that you consider the future waves, first.
- Some tests use a fixture named `one_task` that is defined in `tests/conftest.py`. This fixture saves a specific task to the test database.

### CLI

In addition to testing your code with pytest and postman, you can play test your code with the CLI (Command Line Interface) by running `python3 cli/main.py`. 

The flask server needs to be running first before running the CLI.

### CRUD Routes

The following are required routes for wave 1. Feel free to implement the routes in any order within this wave.

#### Create a Task: Valid Task With `null` `completed_at`

As a client, I want to be able to make a `POST` request to `/tasks` with the following HTTP request body

```json
{
  "title": "A Brand New Task",
  "description": "Test Description",
  "completed_at": null
}
```

and get this response:

`201 CREATED`

```json
{
  "task": {
    "id": 1,
    "title": "A Brand New Task",
    "description": "Test Description",
    "is_complete": false
  }
}
```

so that I know I successfully created a Task that is saved in the database.

Remember that the knowledge of how to initialize a new model instance from the request dictionary is often left to the model itself, as it allows the model to control which fields are required and how they are initialized. We could add a class method to the Task model that initializes a new instance from a dictionary, and use this method in the route. If all of our models have this method, we could create a route helper method that initializes a new model instance from a dictionary, and use it in this route and any other route that creates a new model instance.

Further, notice that the data nested under the `"task"` key is a dictionary representation of the task that was created. Creating a model helper method to return this dictionary, which we can then use to help build this route response, will improve the consistency of our endpoints.

#### Get Tasks: Getting Saved Tasks

As a client, I want to be able to make a `GET` request to `/tasks` when there is at least one saved task and get this response:

`200 OK`

```json
[
  {
    "id": 1,
    "title": "Example Task Title 1",
    "description": "Example Task Description 1",
    "is_complete": false
  },
  {
    "id": 2,
    "title": "Example Task Title 2",
    "description": "Example Task Description 2",
    "is_complete": false
  }
]
```

Notice that each data item in the list is a dictionary representation of a task. Creating a model helper method to return this dictionary, which we can then use to help build this route response, will improve the consistency of our endpoints.

#### Get Tasks: No Saved Tasks

As a client, I want to be able to make a `GET` request to `/tasks` when there are zero saved tasks and get this response:

`200 OK`

```json
[]
```

#### Get One Task: One Saved Task

As a client, I want to be able to make a `GET` request to `/tasks/1` when there is at least one saved task and get this response:

`200 OK`

```json
{
  "task": {
    "id": 1,
    "title": "Example Task Title 1",
    "description": "Example Task Description 1",
    "is_complete": false
  }
}
```

Notice that the data nested under the `"task"` key is a dictionary representation of the task that was retrieved. Creating a model helper method to return this dictionary, which we can then use to help build this route response, will improve the consistency of our endpoints.

Further, we should remember that retrieving a model by its ID is a common operation. We should consider creating a route helper method that can retrieve a model by its ID, and use it in this route. This method could start out only working for Task models. But knowing that we'll be working with Goal models later on, it might be worth generalizing this method to work with any model.

#### Update Task

As a client, I want to be able to make a `PUT` request to `/tasks/1` when there is at least one saved task with this request body:

```json
{
  "title": "Updated Task Title",
  "description": "Updated Test Description"
}
```

and get this response:

`204 No Content`

The response should have a mimetype of "application/json" to keep our API response type consistent.

Note that the update endpoint does update the `completed_at` attribute. This will be updated with custom endpoints implemented in Wave 3.

We should remember that retrieving a model by its ID is a common operation. We should consider creating a route helper method that can retrieve a model by its ID, and use it in this route. This method could start out only working for Task models. But knowing that we'll be working with Goal models later on, it might be worth generalizing this method to work with any model.

#### Delete Task: Deleting a Task

As a client, I want to be able to make a `DELETE` request to `/tasks/1` when there is at least one saved task and get this response:

`204 No Content`

The response should have a mimetype of "application/json" to keep our API response type consistent.

We should remember that retrieving a model by its ID is a common operation. We should consider creating a route helper method that can retrieve a model by its ID, and use it in this route. This method could start out only working for Task models. But knowing that we'll be working with Goal models later on, it might be worth generalizing this method to work with any model.

#### No Matching Task: Get, Update, and Delete

As a client, if I make any of the following requests:

  * `GET` `/tasks/<task_id>`
  * `UPDATE` `/tasks/<task_id>`
  * `DELETE` `/tasks/<task_id>`

and there is no existing task with an `id` of `task_id`

The response code should be `404`.

You may choose the response body.

Make sure to complete the tests for non-existing tasks to check that the correct response body is returned.

By using a helper method to retrieve a model by its ID, we could ensure that the response for a non-existing model is consistent across all these routes.

#### Create a Task: Invalid Task With Missing Data

##### Missing `title`

As a client, I want to be able to make a `POST` request to `/tasks` with the following HTTP request body

```json
{
  "description": "Test Description",
  "completed_at": null
}
```

and get this response:

`400 Bad Request`

```json
{
  "details": "Invalid data"
}
```

so that I know I did not create a Task that is saved in the database.

##### Missing `description`

If the HTTP request is missing `description`, we should also get this response:

`400 Bad Request`

```json
{
  "details": "Invalid data"
}
```
