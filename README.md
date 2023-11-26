# JunctionX Budapest 2023

## Demo
![Demo Image](junctionx-budapest.png)


https://dashboard-xzpcu7nwvq-ew.a.run.app/

Sent email to 'allseek_admin@7w1ymt.onmicrosoft.com' for testing credentials detection.

VIDEO: https://www.youtube.com/watch?v=o6Mr95cWBhU

## GCloud Deployment

```gcloud run deploy regex-detector --image=mielverkerken/regex-detector --platform managed --port 8000 --region europe-west1

gcloud run deploy orchestrator --image=mielverkerken/orchestrator --platform managed --set-env-vars NIGHTFALL_API_KEY=NF-QAGiE0LRisoWgvohwQSTN87fM0AHg4WT,NIGHTFALL_DETECTION_RULE_UUID=4eb100fc-71fd-47ff-b10a-21f7bf008f85,REGEX_DETECTOR_URL=https://regex-detector-xzpcu7nwvq-ew.a.run.app,REGEX_DETECTOR_PORT=443 --port 80 --region europe-west1

gcloud run deploy dashboard --image=mielverkerken/dashboard --platform managed --port 80 --region europe-west1

gcloud run deploy integration-teams --image=mielverkerken/integration-teams --platform managed --port 8000 --region europe-west1
```