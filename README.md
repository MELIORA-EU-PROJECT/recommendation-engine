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
    - `POST` : Pass a user profile in the body and response is a recommendation + debugging info

## Files and Explanations

- `main.py` : The main file of the server. It contains the FastAPI server and the endpoints. This file also contains the
  `intervention library` at the top, which is a crucial part of the system.
- `data_generator.py` : The client that generates random user profiles and sends it to the server. Each user feature is
  annotated with the distribution logic it follows.
- `utils.py` : Contains the logic of the steps of the recommendation engine. Most important functions are `
  infer_integrated_data_layer`, `infer_aggregated_data_layer` and `add_ttm_stages`.
  See [Recommendation Engine Paper](https://www.notion.so/A-Comprehensive-User-Modeling-Framework-and-a-Recommender-System-for-Personalizing-Well-Being-Relate-72bef7df897f4432bbf6e38fc6bac3bb?pvs=4)
  and its appendices.
- `rest of the python files` : These are scratch files used for experimentation and testing.
- `example_patient.json` : An example of the data model used for the user profiles.
- `rest of the json files` : These are incremental files showing how each stage affects the user profile.