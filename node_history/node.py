from unittest.mock import Mock

# this is the Memento Class in our case the Node dealt with by the system
# it is opaque to the caretaker (...) 

class Node:

    def __init__(self,state : str) -> None:
        self._state=state
        pass

    def getState(self):
        return self._state

