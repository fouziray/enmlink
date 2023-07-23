# enmlink
this repository contains 

-an external django api to be linked with a database keeping record of users, ssv schedule, and relative information to the process.

-a rasa chatbot with scenarios relative to the ssv process, aplying custom actions that call the external api.


### How to run
the following commands are to be executed from the root directory of the project.
Use `rasa run` to run the chatbot's NLU and response selector at once, or `rasa run nlu` for intent and entity classification/ranking only.

The former requires the actions servers to be running with `rasa run actions`, along with api.

For an interactive mode with which the answers can be tweaked and adjusted with an approval or decline of actions using `rasa interactive`

## Folders and files structure:

-Entities database: data/lookup/*
-Intents and Entities extraction: data/nlu.yml
-Training stories: data/stories.yml
-Training rules: data/rules.yml
-Custom actions: actions/actions.py
-Descriptors: /json/*
-Trained model: /models/ 
NLU performance tests: /results/*

for the sake of size, models aren't uploaded to this repository, however they're generated using `rasa train`