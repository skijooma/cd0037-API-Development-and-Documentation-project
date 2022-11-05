# API Development and Documentation Final Project

## Trivia App

This app is Udacity class-based API Development and Documentation project that allows users to play a game where they
can add new questions, delete them and play the actual trivia game. is invested in creating bonding experiences for its
employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to
manage the trivia app and play the game. The frontend for this project was
pretty much built out as starter code, and the goal was to start up the backend, and build an API that can enable the
execution of the above-mentioned use cases below:

1. **Display questions** - both all questions and by category. Questions should show the question, category and
   difficulty rating by default and can show/hide the answer.
2. **Delete questions**.
3. **Add questions** and require that they include question and answer text.
4. **Search for questions** based on a text query string.
5. **Play the quiz game**, randomizing either all questions or within a specific category.

## Getting started

A [clone](https://github.com/skijooma/cd0037-API-Development-and-Documentation-project.git) of the repository is needed.
One can work on the project locally and push their changes to the remote repository.

### Internal documentation (Code base)

All functions added to the project require elaborate documentation.

### Coding style

We would also like to follow the [PEP8](https://www.python.org/dev/peps/pep-0008/) guidelines.

## Project technology stack

### Frontend

The frontend code base is based on [ReactJS](https://reactjs.org/) and [JQuery](https://jquery.com/) for the making
requests to the backend.
Detailed guide to starting up the frontend are provided in this dedicated [Frontend README](./frontend/README.md) for
more details.

### Backend

The [backend](./backend/README.md) is also Flask and SQLAlchemy-based server. You will work primarily in `__init__.py`to
define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in
the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> More setup details in the [Backend README](./backend/README.md).

## External API documentation.

### API endpoints and expected behavior.

The app features the following endpoints with the behavior detailed below.

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the
  category
- Request Arguments: None
- Returns: A boolean value indicating a successful request, and an object with a key, `categories`, that contains an
  object of id: category_string key:value pairs.

```json
{
  "success": "True",
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: A boolean value indicating a successful request, an object with 10 paginated questions, total questions,
  object including all categories, and current category string

```json
{
  "success": "True",
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: A boolean value indicating a successful request, and the id of the deleted question.

```
{'success': True, 'deleted': id}
```

---

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "success": "True",
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: Does not return any new data

```
{
    "success": "True", 
    "created": 1,
}
```

---

`POST '/questions/search'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: A boolean value indicating a successful request, and any array of questions, a number of totalQuestions that
  met the search term and the current category string

```json
{
  "success": "True",
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```

-----

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: A boolean value indicating a successful request, and an object with questions for the specified category,
  total questions, and current category string

```json
{
  "success": "True",
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
}
```

---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
  'previous_questions': [
    1,
    4,
    20,
    15
  ]
  quiz_category
  ': '
  current
  category
  '
}
```

- Returns: A boolean value indicating a successful request, and a new question object

```json
{
  "success": "True",
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```

### Error handling

The API returns errors as a JSON object of this kind:

```
{
  "error": 404,
  "message": "Resource not found",
  "success": false
}
```

The following errors are handled:

- 400: Bad Request
- 404: Resource not found
- 405: Method not allowed
- 422: Unprocessable entity
- 500: Internal server error

----------------

## Acknowledgments

Appreciation to the Udacity FSND team, who came up with the set up &
starter code for the whole stack.
