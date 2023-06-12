# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
from typing import Any, Text, Dict, List, TYPE_CHECKING

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .api.enm import CommandEventAPI
#from .EnmCommands.plainCommands import *

from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType

class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         
         dispatcher.utter_message(text=return_message)

         return []

class ActionGetMessage(Action):

     def name(self) -> Text:
         return "action_get_message"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         api=CommandEventAPI()
         
         return_message=tracker.get_slot("Tech2g")
         string = api.getMessage(tracker.latest_message['text'])
         json_obj = json.loads(string.content)
         dispatcher.utter_message("hello "+json_obj)
         dispatcher.utter_message("value of slot"+str(tracker.slots))

         return [tracker.slots]

#class ActionGet(Action):
#    def name(self) -> Text:
#        return "action_get_tech";
#    def run(slef,dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
#         tracker.
#         api=CommandEventAPI()
#         string = api.getMessage("this is the sent token")
#         json_obj = json.loads(string.content)
#         dispatcher.utter_message("hello "+json_obj)
#
#         return [];


""""
from rasa.shared.core.constants import ACTION_SESSION_START_NAME, ACTION_LISTEN_NAME
from rasa.shared.core.trackers import DialogueStateTracker
if TYPE_CHECKING:
    from rasa.core.nlg import NaturalLanguageGenerator
    from rasa.core.channels.channel import OutputChannel
from rasa.shared.core.domain import Domain
from rasa.shared.core.events import Event
class ActionSessionStart(Action): """
"""Applies a conversation session start.

    Takes all `SlotSet` events from the previous session and applies them to the new
    session.
    """
"""
    def name(self) -> Text:
        return ACTION_SESSION_START_NAME

    @staticmethod
    def _slot_set_events_from_tracker(
        tracker: "DialogueStateTracker",
    ) -> List["SlotSet"]: """
"""Fetch SlotSet events from tracker and carry over key, value and metadata."""
"""       carried_slots=[
            SlotSet(key=event.key, value=event.value, metadata=event.metadata)
            for event in tracker.applied_events()
            if isinstance(event, SlotSet)
        ]
        carried_slots.append(SlotSet(key="user_id",value=1))
        return  carried_slots

    async def run(
        self,
        output_channel: "OutputChannel",
        nlg: "NaturalLanguageGenerator",
        tracker: "DialogueStateTracker",
        dispatcher: "CollectingDispatcher",
        domain: "Domain",
    ) -> List[Event]: """
"""Runs action. Please see parent class for the full docstring."""
"""   _events: List[Event] = [SessionStarted()]
        tracker.slots["sample"]=1
        dispatcher.utter_message("hello "+tracker.get_slot("sample"))

        if domain.session_config.carry_over_slots:
            _events.extend(self._slot_set_events_from_tracker(tracker))

        _events.append(ActionExecuted(ACTION_LISTEN_NAME))

        return _events """
