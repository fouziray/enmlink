from node import Node


class NodeOriginator():
    _state= None
    # state type is to be determined wether should be in raw format (string) or as a subnode in enmscripting system
    def __init__(self, state: str) -> None:
        self._state = state
        print(f"Originator: My initial state is: {self._state}")

    def save(self) -> Node:
        return Node(self._state)

    def restore(self, memento: Node) -> None:
        
        self._state = memento.get_state()
        print(f"Originator: My state has changed to: {self._state}")