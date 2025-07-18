# Rule based system Prototype

## Author : Nikos Gournakis

## Quick Start - Server

```
fastapi dev main.py
```

## Quick Start - Client

```
python data_generator.py
```

## Endpoints

- `/` :
    - `GET` : Health check, returns "Hello World"
- `/debug_recommend` :
    - `POST` : Pass a user profile in the body and response is a list of recommendations + debugging info
- `/recommend` :
    - `POST` : Pass a user profile in the body and response is a list of recommendations
- `/{user_id}/day` :
    - `GET` : Pass a user id as a path parameter. The response is the user's current day according to the active mini
      course.
- `/mini_course/{mini_course_id}/{day}` :
    - `GET` : Pass a mini course id as a path parameter. Pass a day as a query parameter. The response is the schedule
      of the mini course at the given day.
- `/mini_course`
    - `POST` : Pass a user profile and a mini course in the body and a query parameter `index`, indicating which goal in
      the mini course to recommend for. It responds with all the recommendations that match the goal of the mini course
      on the index given. Look at the file `example_endpoint_mini_course.json` for an example of the body.

## Files and Explanations

- `main.py` : The main file of the server. It contains the FastAPI server and the endpoints. This file also contains the
  `intervention library` at the top, which is a crucial part of the system.
- `data_generator.py` : The client that generates random user profiles and sends it to the server. Each user feature is
  annotated with the distribution logic it follows.
- `utils.py` : Contains the logic of the steps of the recommendation engine. Most important functions are `
  infer_integrated_data_layer`, `infer_aggregated_data_layer` and `add_ttm_stages`.
  See [Recommendation Engine Paper](https://ieeexplore.ieee.org/document/9934912)
  and its appendices.
- `rest of the python files` : These are scratch files used for experimentation and testing.
- `example_patient.json` : An example of the data model used for the user profiles.
- `rest of the json files` : These are incremental files showing how each stage affects the user profile.
