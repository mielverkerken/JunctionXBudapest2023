# Orchestrator

## Local Development 

### Run

`uvicorn src.main:app --reload --env-file dev.env`

## Docker

### Build

`docker build -t orchestrator .`

### Run

`docker run --rm -p80:80 --env-file dev.env orchestrator`