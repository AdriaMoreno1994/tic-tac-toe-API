# Tic Tac Toe Online Game

## Overview
A scalable  Tic Tac Toe game built with Python and Flask. Users can create games, make moves, and check the game statuses.

## Installation

### Prerequisites
- Python 3.x
- Docker and Docker Compose installed. You can download them [here](https://www.docker.com/products/docker-desktop).

### Steps
1. #### Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tic-tac-toe-API.git
   cd tic-tac-toe-API
   ```

2. #### Configure the environment variables. 
  - You can copy them from .env.example and update as necessary.

3. #### Build and run with Docker:
   ```
   docker-compose build
   docker-compose up app
   ```
The application will be accessible at `http://localhost:5001`.

4. #### Run tests

- To execute the tests in a separate container, run:
- ```
  docker-compose up test
  ```
## API Documentation

### 1. Root Endpoint

**Endpoint:** `/`  
**Method:** `GET`  
**Description:** This endpoint provides a welcome message to users accessing the root of the API.

- **Response:**
  - **Success:** 
      ```json
      {
          
          "message": "Welcome to the Tic Tac Toe API!",
          "version": "1.0"
      }
      ```
      - **HTTP Status:** 200 OK
   


### 2. Create a Game
- **Endpoint:** `/create`
- **Method:** `POST`
- **Description:** Starts a new game and returns the match ID.
- **Response:**
  - **Success:** 
    ```json
    {
        "match_id": <match_id>
    }
    ```
    - **HTTP Status:** 200 OK
  - **Error:** 
    - if the required parameter is not an integer:
         ```json
         {
             "error": "Invalid request data"
         }
         ```
         - **HTTP Status:** 400 Bad Request
### 3. Make a Move
- **Endpoint:** `/move`
- **Method:** `POST`
- **Description:** Make a move in the game.
- **Request Body:**
    ```json
    {
        "match_id": <match_id>,
        "player_id": "X" | "O",
        "square": {
            "x": <x_coordinate>,
            "y": <y_coordinate>
        }
    }
    ```
- **Response:**
    - **Success:** 
        ```json
        {
            "match_id": <match_id>,
            "player_id": "X" | "O",
            "square": {
                "x": <x_coordinate>,
                "y": <y_coordinate>
            }
        }
        ```
        - **HTTP Status:** 200 OK
    - **Error:** 
        - If any of the required parameters (`match_id`, `player_id`, `square`) are missing:
        ```json
        {
            "error": "Invalid request data"
        }
        ```
        - **HTTP Status:** 400 Bad Request
        
### 4. Game Status
- **Endpoint:** `/status/<match_id>`
- **Method:** `GET`
- **Description:** Retrieves the current status of the game.
- **Response:**
    - **Success:** 
        ```json
        {
            "match_id": <match_id>,
            "current_player": "X" | "O",
            "board": [
                [" ", " ", " "],
                [" ", " ", " "],
                [" ", " ", " "]
            ],
            "status": "ongoing" | "finished",
            "winner": null | "X" | "O"
        }
        ```
        - **HTTP Status:** 200 OK
    - **Error:** 
        - If the `match_id` is not found:
        ```json
        {
            "error": "Match not found"
        }
        ```
        - **HTTP Status:** 404 Not Found
