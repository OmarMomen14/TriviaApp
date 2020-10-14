# Full Stack API Final Project

## Full Stack Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

The application can:

1) Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).
 
## About the Stack

The stack is organized on separate folders as `./backend` for Backend Server and `./frontend` for Frontend Server.

### Backend

The `./backend` directory contains a complete Flask and SQLAlchemy server. Please [View the README.md within ./backend for more details.](./backend/README.md)inside the directory for more information.

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. Please [View the README.md within ./frontend for more details.](./frontend/README.md)inside the directory for more information.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
- Errors are returned as JSON objects in the following format:

    ```
        {
            "error": 404,
            "message": "Resource Not Found",
            "success": false
        }
    ```
- Returned Errors can be one of four types as follow:
    - 400: Bad Request
    - 404: Resource Not Found
    - 405: Method Not Allowed
    - 422: Unprocessable

### Endpoints

All our endpoints in this application are configured based on the base url `http://127.0.0.1:5000/` + `api/`, e.g `http://127.0.0.1:5000/api/SOMETHING`

- `Basic` Endpoint:
    - GET `/api`
        - Purpose: To test correct connection to the server.
        - Request
            - No Query Parameters/Variables/Payload needed at all
            - Example
                ```
                    curl -X GET http://127.0.0.1:5000/api
                ```
        - Response
            - Data Type: JSON object of keys 'success' (Boolean), 'message' (String)
            - Sample response:
            ```
                {
                    "message": "Hello To Trivia API, Please Refer to the Documentation for more information",
                    "success": true
                }
            ```

- `Category` Endpoints:
    - GET `/api/categories`
        - Purpose: To get all available categories of questions recorded in the database.
        - Request
            - No Query Parameters/Variables/Payload needed at all
            - Example
                ```
                    curl -X GET http://127.0.0.1:5000/api/categories
                ```
        - Response
            - Data Type: JSON object of keys 'success' (Boolean), 'categories' (JSON object)
            - Sample response:
            ```
                {
                    "categories": {
                        "1": "Science",
                        "2": "Art",
                        "3": "Geography",
                        "4": "History",
                        "5": "Entertainment",
                        "6": "Sports"
                    },
                    "success": true
                }
            ```
    - GET `/api/categories/<int:category_id>/questions`
        - Purpose: To get all recorded questions belonging to a specific category (category_id)
        - Request
            - int variable for category id is needed in the endpoint url as shown above
            - Example
                ```
                    curl -X GET http://127.0.0.1:5000/api/categories/1/questions
                ```
        - Response
            - Data Type: JSON object of keys 'success' (Boolean), 'current_category' (String), 'questions' (List of JSON objects), 'total_questions' (Integer) 
            - Sample response:
            ```
                {
                    "current_category": "Science",
                    "questions": [
                        {
                            "answer": "The Liver",
                            "category": 1,
                            "difficulty": 4,
                            "id": 20,
                            "question": "What is the heaviest organ in the human body?"
                        },
                        {
                            "answer": "Alexander Fleming",
                            "category": 1,
                            "difficulty": 3,
                            "id": 21,
                            "question": "Who discovered penicillin?"
                        },
                        {
                            "answer": "Blood",
                            "category": 1,
                            "difficulty": 4,
                            "id": 22,
                            "question": "Hematology is a branch of medicine involving the study of what?"
                        }
                    ],
                    "success": true,
                    "total_questions": 3
                }
            ```
- `Question` Endpoints:
    - GET `/api/questions`
        - Purpose: To get ALL questions recorded in the database with pagination feature.
        - Request
            - Query Parameter `?page=X` can be added to the endpoint url to request a certain partition of the questions, default is 1 if not specified.
            - Example
                ```
                    curl -X GET http://127.0.0.1:5000/api/questions?page=2
                ```
        - Response
            - Data Type: JSON object of keys 'success' (Boolean), 'current_category' (null), 'questions' (List of JSON objects), categories (JSON object), 'total_questions' (Integer)
            - Sample response:
            ```
                {
                    "categories": {
                        "1": "Science",
                        "2": "Art",
                        "3": "Geography",
                        "4": "History",
                        "5": "Entertainment",
                        "6": "Sports"
                    },
                    "current_category": null,
                    "questions": [
                        {
                            "answer": "Tom Cruise",
                            "category": 5,
                            "difficulty": 4,
                            "id": 4,
                            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                        },
                        {
                            "answer": "Maya Angelou",
                            "category": 4,
                            "difficulty": 2,
                            "id": 5,
                            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                        },
                        {
                            "answer": "Edward Scissorhands",
                            "category": 5,
                            "difficulty": 3,
                            "id": 6,
                            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                        },
                        {
                            "answer": "Muhammad Ali",
                            "category": 4,
                            "difficulty": 1,
                            "id": 9,
                            "question": "What boxer's original name is Cassius Clay?"
                        },
                        {
                            "answer": "Brazil",
                            "category": 6,
                            "difficulty": 3,
                            "id": 10,
                            "question": "Which is the only team to play in every soccer World Cup tournament?"
                        },
                        {
                            "answer": "Uruguay",
                            "category": 6,
                            "difficulty": 4,
                            "id": 11,
                            "question": "Which country won the first ever soccer World Cup in 1930?"
                        },
                        {
                            "answer": "George Washington Carver",
                            "category": 4,
                            "difficulty": 2,
                            "id": 12,
                            "question": "Who invented Peanut Butter?"
                        },
                        {
                            "answer": "Lake Victoria",
                            "category": 3,
                            "difficulty": 2,
                            "id": 13,
                            "question": "What is the largest lake in Africa?"
                        },
                        {
                            "answer": "Agra",
                            "category": 3,
                            "difficulty": 2,
                            "id": 15,
                            "question": "The Taj Mahal is located in which Indian city?"
                        },
                        {
                            "answer": "Escher",
                            "category": 2,
                            "difficulty": 1,
                            "id": 16,
                            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
                        }
                    ],
                    "success": true,
                    "total_questions": 22
                }
            ```
    - POST `/api/questions`
        - Purpose: To create new question in the database, and to seacrh for questions already recorded in the database
        - Request
            - A JSON payload is required in the request based on the intended purpose as follow:
                - For adding new questions, the payload JSON should be structured as follow:
                    ```
                        {
                            "question": "Question Text Here",
                            "answer": "Answer Text Here",
                            "difficulty": INTEGER Value Here 1 - 5,
                            "category": INTEGER Value Here
                        }
                    ```
                - For searching of questions, the payload JSON should be structured as follow:
                    ```
                        {
                            "searchTerm": "Searching Text Here",
                        }
                    ```
            - Example
                - For adding new question:
                    ```
                        curl --location --request POST 'localhost:5000/api/questions' \
                        --header 'Content-Type: application/json' \
                        --data-raw '{
                            "question": "Who let the dogs out?",
                            "answer": "Who Who Who Who!!",
                            "difficulty": 2,
                            "category": 3
                        }'
                    ```
                - For searching for questions:
                    ```
                        curl --location --request POST 'localhost:5000/api/questions' \
                        --header 'Content-Type: application/json' \
                        --data-raw '{
                            "searchTerm": "Who"
                        }'
                    ```
        - Response
            - For Adding new question: 
                - Data Type: JSON object of keys 'success' (Boolean), 'new_question_id' (Integer)
                - Sample response:
                    ```
                        {
                            "new_question_id": 35,
                            "success": true
                        }
                    ```
            - For Searching for questions: 
                - Data Type: JSON object of keys 'success' (Boolean), 'current_category' (null), 'questions' (List of Json objects), 'total_questions' (Integer)
                - Sample response:
                    ```
                        {
                            "current_category": null,
                            "questions": [
                                {
                                    "answer": "Maya Angelou",
                                    "category": 4,
                                    "difficulty": 2,
                                    "id": 5,
                                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                                },
                                {
                                    "answer": "George Washington Carver",
                                    "category": 4,
                                    "difficulty": 2,
                                    "id": 12,
                                    "question": "Who invented Peanut Butter?"
                                },
                                {
                                    "answer": "Alexander Fleming",
                                    "category": 1,
                                    "difficulty": 3,
                                    "id": 21,
                                    "question": "Who discovered penicillin?"
                                },
                                {
                                    "answer": "Who Who Who Who!!",
                                    "category": 3,
                                    "difficulty": 2,
                                    "id": 34,
                                    "question": "Who let the dogs out?"
                                }
                            ],
                            "success": true,
                            "total_questions": 4
                        }
                    ```
    - DELETE `/api/questions/<int:question_id>`
        - Purpose: To Delete a specific question recorded in the database.
        - Request
            - int variable for question id is needed in the endpoint url as shown above.
            - Example
                ```
                    curl -X DELETE http://127.0.0.1:5000/api/questions/35
                ```
        - Response
            - Data Type: JSON object of keys 'success' (Boolean), 'deleted_question_id' (Integer)
            - Sample response:
                ```
                    {
                        "deleted_question_id": 35,
                        "success": true
                    }
                ```

- `Quiz` Endpoint:
    - POST `/api/quiz`
        - Purpose: To get a random question from a specific category with excluding a list of questions from the selection as specified in the request body.
        - Request
            - JSON Payload is needed in the request containing 'quiz_category' (JSON object), 'previous_questions' (List of integers)
            - Example
                ```
                    curl --location --request POST 'localhost:5000/api/quiz' \
                    --header 'Content-Type: application/json' \
                    --data-raw '{
                        "quiz_category": {
                            "id": 3
                        },
                        "previous_questions": [13, 15]
                    }'
                ```
        - Response
            - If there was still a pool for selection after excluding the previous_questions list:
                - Data Type: JSON object of keys 'success' (Boolean), 'question' (JSON object)
                - Sample response:
                ```
                    {
                        "question": {
                            "answer": "Who Who Who Who!!",
                            "category": 3,
                            "difficulty": 2,
                            "id": 34,
                            "question": "Who let the dogs out?"
                        },
                        "success": true
                    }
                ```

            - If there wasn't any remaining questions after excluding the previous_questions list:
                - Data Type: JSON object of keys 'success' (Boolean), 'question' (null)
                - Sample response:
                ```
                    {
                        "question": null,
                        "success": true
                    }
                ```

## Deployment N/A

## Authors
Omar Momen 

## Acknowledgements 

Udacity Instructors:
- Caryn McCarthy 
- Amy Hua

 


