## How to start
### Development environment
 * Docker (version 19.03.5, build 633a0ea838)
 * Docker-compose (version 1.23.2, build 1110ad0)
### Running the application
After setting up docker and docker compose, clone this repo and run the following: </br>
``` docker-compose build ```
</br>
Then initialize the db from migrations and fixtures:</br>
``` docker-compose up init ``` </br>
Finally start the APIs and Celery's worker/beat: </br>
``` docker-compose up apis celery-beat celery-worker ```
</br>
### Running tests
``` docker-compose up test ```
### API Endpoints
1) Get the current + 5 day forecast weather for a given location: http://localhost:8000/weather/temperature/?lat=22&long=22
2) Get the south american capitals weather with a 4-Range classification: http://localhost:8000/weather/south-america/
3) Get available tours for a given danger score between two dates: http://localhost:8000/tour/?start=2020-10-02&end=2020-10-31&danger_score=3

## Todo
- [ ] Add more tests
- [ ] Add prod settings



