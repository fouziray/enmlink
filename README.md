# enmlink
this repository contains 

-an external django api to be linked with a database keeping record of users, ssv schedule, and relative information to the process.

-a rasa chatbot with scenarios relative to the ssv process, aplying custom actions that call the external api.


### How to run
the following commands are to be executed from the root directory of the project.
Use `rasa run` to run the chatbot's NLU and response selector at once, or `rasa run nlu` for intent and entity classification/ranking only.

The former requires the actions servers to be running with `rasa run actions`, along with api.

For an interactive mode with which the answers can be tweaked and adjusted with an approval or decline of actions use `rasa interactive`

