# Regex-Detector

## Local Development 

### Run

`uvicorn src.main:app --reload`

## Docker

### Build

`docker build -t regex-detector .`

### Run

`docker network create allseek`
`docker run --rm -p8000:8000 --network=allseek --name regex-detector regex-detector`