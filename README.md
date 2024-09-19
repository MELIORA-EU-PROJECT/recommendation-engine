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

## Files and Explanations

- `main.py` : The main file of the server. It contains the FastAPI server and the endpoints.
- `data_generator.py` : The client that generates random user profiles and sends it to the server.
- `utils.py` : Contains the logic of the steps of the recommendation engine.
  See [Recommendation Engine Paper](https://www.notion.so/A-Comprehensive-User-Modeling-Framework-and-a-Recommender-System-for-Personalizing-Well-Being-Relate-72bef7df897f4432bbf6e38fc6bac3bb?pvs=4)
  and its appendices.
- `rest of the python files` : These are scratch files used for experimentation and testing.
- `example_patient.json` : An example of the data model used for the user profiles.
- `rest of the json files` : These are incremental files showing how each stage affects the user profile.