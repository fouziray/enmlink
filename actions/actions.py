# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
from typing import Any, Text, Dict, List, TYPE_CHECKING

from langdetect import detect

# add this line in all actions : lang = detect(tracker.get_latest_message.txt or tracker.latest_message.text , tracker.latest_message.get("text"))
# if lang = 'en' : repondre en englais 
# if lang = 'fr' : repondre en englais  
# if lang = 'ar' : repondre en arabe

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
         #string = api.getMessage(tracker.latest_message['text'])
         #json_obj = json.loads(string.content)
         #dispatcher.utter_message("hello "+json_obj)
         buttons = [{"title": "Yes", "payload": "/affirm"}, {"title": "No", "payload": "/deny"}]
         dispatcher.utter_message("value of slot"+str(tracker.slots))
#         dispatcher.utter_button_message("respond please ?", buttons)

         return [SlotSet("code_site_slot", 1872)]

class ActionResetTechs(Action):

    def name(self) -> Text:
        return "action_reset_techs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("Tech2g", None), SlotSet("Tech3g", None),SlotSet("Tech4g", None)]

class ActionAvailableTech(Action):

    def name(self) -> Text:
        return "action_available_tech"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        buttons = [{"title": "2G", "payload": "/2g_required_slot"}, {"title": "3G", "payload": "/3g_required_slot"}, {"title": "4G", "payload": "/4g_required_slot"}]
        dispatcher.utter_button_message("respond please ?", buttons)
        return [SlotSet("Tech2g", None), SlotSet("Tech3g", None),SlotSet("Tech4g", None)]

class ActionAppendTechSlots(Action):

    def name(self) -> Text:
        return "action_append_tech_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message("Appending slots to required forms")

#----------------------------------------------------------------

from rasa_sdk.forms import FormValidationAction

class ValidateTechnologiesForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_technologies_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.latest_message['intent'].get('name'):
            # If the user is an existing customer,
            # do not request the `email_address` slot
            #updated_slots.remove("email_address")
            dispatcher.utter_message("intent name is here")


        return updated_slots
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

from  .EnmCommands.plainCommands import Command , GsmCommand, g3NodeCommand, g3rncCommand, g4FDDCommand, g4TDDCommand, RetCommand, OptimCommand

"""
class ActionBlock(Action):

    def name(self) -> Text:
        return "action_block"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

       # get the technologie 2g or 3g or 4g 
        com=Command()
        com.open('XXXX', 'xxxxxx', 'XXXXXXXXXX')

        siteId = tracker.get_slot('code_site_slot')
        
        dispatcher.utter_message("code site is "+str(siteId))

        if(tracker.get_slot('Tech2g') != None):
                c = GsmCommand()
                urfcn = 1000 
                tech_value2 = tracker.get_slot('Tech2g')
                if(tech_value2 == 'g900' or tech_value2 == 'G900'):
                    bande = 'GSM900'
                else : 
                    if(tech_value2 == 'g1800' or tech_value2 == 'G1800'):
                        bande = 'GSM1800'
                    else:
                        if(tech_value2 == '2g' or tech_value2 == '2G'):
                            bande = 'GSM900 , GSM1800'
                
                get_state_2G = c.get(siteId, urfcn, bande)
                print('State 2G')
                print(get_state_2G)
                a = com.execute(get_state_2G)
                dispatcher.utter_message(a)
                print('$$$$$$$',a,'$$$$$$$$')
                set_state_2G = c.set(siteId, urfcn, bande, 'INACTIVE')

        else: 
            if(tracker.get_slot('Tech3g') != None):
                c = g3rncCommand()
                tech_value3 = tracker.get_slot('Tech3g')
                if(tech_value3 == 'U900' or tech_value3 == 'u900'):
                    bande = 'U900'
                else : 
                    if(tech_value3 == 'U2100' or tech_value3 == 'u2100'):
                        bande = 'U2100'
                    else:
                        if(tech_value3 == '3g' or tech_value3 == '3G'):
                            bande = 'U900 , U2100'
                
                get_state_3G = c.get(siteId, bande)
                print('State 3G')
                print(get_state_3G)
                a = com.execute(get_state_3G)
                dispatcher.utter_message(a)
                print('$$$$$$$',a,'$$$$$$$$')
                set_state_3G = c.set(siteId, bande, 'LOCKED')

                
    
            else: 
                if(tracker.slots.get_slot['Tech4g'] != None):
                    
                    tech_value4 = tracker.get_slot('Tech4g')
                    if(tech_value4 == '4g' or tech_value4 == '4G'):
                        c = g4TDDCommand()
                        get_state_4G = c.get(siteId)
                        print('State 4G')
                        print(get_state_4G)
                        a = com.execute(get_state_4G)
                        print('$$$$$$$',a,'$$$$$$$$')
                        set_state_4G = c.set(siteId, 'LOCKED')

                    else : 
                        if(tech_value4 == 'L1800' or tech_value4 == 'l1800'):
                            bande = 'L1800'
                            c = g4FDDCommand()
                        else:
                            if(tech_value4 == 'L2100' or tech_value4 == 'l2100'):
                                bande = 'L2100'
                                c = g4FDDCommand()        
                    
                        get_state_4G = c.get(siteId, bande)
                        print('State 4G')
                        print(get_state_4G)
                        a = com.execute(get_state_4G)
                        dispatcher.utter_message(a)
                        print('$$$$$$$',a,'$$$$$$$$')
                        set_state_4G = c.set(siteId, bande, 'LOCKED')


"""







class Action_Block_Unblock(Action):
   
    def name(self) -> Text:
        return "action_block_unblock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

       # get the technologie 2g or 3g or 4g 
        com=Command()
        com.open('XXXX', 'xxxxxx', 'XXXXXXXXXX')

        siteId = tracker.get_slot('code_site_slot')
        
        dispatcher.utter_message("code site is "+str(siteId))
       
        tech_value2 = tracker.get_slot('Tech2g')
        tech_value3 = tracker.get_slot('Tech3g')
        tech_value4 = tracker.get_slot('Tech4g')

        if(tech_value2 != None):
                c = GsmCommand()
                urfcn = 1000 
                if(tech_value2 == 'g900' or tech_value2 == 'G900'):
                    bande = 'GSM900'
                else : 
                    if(tech_value2 == 'g1800' or tech_value2 == 'G1800'):
                        bande = 'GSM1800'
                    else:
                        if(tech_value2 == '2g' or tech_value2 == '2G'):
                            bande = 'GSM900 , GSM1800'
                
                get_state_2G = c.get(siteId, urfcn, bande)
                print('State 2G')
                print(get_state_2G)
                a = com.execute(get_state_2G)
                dispatcher.utter_message(a)
                print('$$$$$$$',a,'$$$$$$$$')
                if(tracker.latest_message['intent'].get('name') == 'ask_lock'):
                    set_state_2G = c.set(siteId, urfcn, bande, 'ACTIVE')
                else:
                    if(tracker.latest_message['intent'].get('name') == 'ask_unlock'):
                        set_state_2G = c.set(siteId, urfcn, bande, 'INACTIVE')
                    

        if(tech_value3 != None):
                c = g3rncCommand()
                
                if(tech_value3 == 'U900' or tech_value3 == 'u900'):
                    bande = 'U900'
                else : 
                    if(tech_value3 == 'U2100' or tech_value3 == 'u2100'):
                        bande = 'U2100'
                    else:
                        if(tech_value3 == '3g' or tech_value3 == '3G'):
                            bande = 'U900 , U2100'
                
                get_state_3G = c.get(siteId, bande)
                print('State 3G')
                print(get_state_3G)
                a = com.execute(get_state_3G)
                dispatcher.utter_message(a)
                print('$$$$$$$',a,'$$$$$$$$')
                if(tracker.latest_message['intent'].get('name') == 'ask_lock'):
                    set_state_3G = c.set(siteId, bande, 'LOCKED')
                else:
                    if(tracker.latest_message['intent'].get('name') == 'ask_unlock'):
                         set_state_3G = c.set(siteId, bande, 'UNLOCKED')



        if(tech_value4 != None):
                    
            tech_value4 = tracker.get_slot('Tech4g')
            if(tech_value4 == '4g' or tech_value4 == '4G'):
                c = g4TDDCommand()
                get_state_4G = c.get(siteId)
                print('State 4G')
                print(get_state_4G)
                a = com.execute(get_state_4G)
                print('$$$$$$$',a,'$$$$$$$$')
                if(tracker.latest_message['intent'].get('name') == 'ask_lock'):
                    set_state_4G = c.set(siteId, 'LOCKED')
                else:
                    if(tracker.latest_message['intent'].get('name') == 'ask_unlock'):
                        set_state_4G = c.set(siteId, 'UNLOCKED')
                    else : 
                        if(tech_value4 == 'L1800' or tech_value4 == 'l1800'):
                            bande = 'L1800'
                            c = g4FDDCommand()
                        else:
                            if(tech_value4 == 'L2100' or tech_value4 == 'l2100'):
                                bande = 'L2100'
                                c = g4FDDCommand()        
                    
                        get_state_4G = c.get(siteId, bande)
                        print('State 4G')
                        print(get_state_4G)
                        a = com.execute(get_state_4G)
                        dispatcher.utter_message(a)
                        print('$$$$$$$',a,'$$$$$$$$')
                        if(tracker.latest_message['intent'].get('name') == 'ask_lock'):
                            set_state_4G = c.set(siteId, bande, 'LOCKED')
                        else:
                            if(tracker.latest_message['intent'].get('name') == 'ask_unlock'):
                                set_state_4G = c.set(siteId, bande, 'UNLOCKED')







             


class Action_Rollback(Action):

    def name(self) -> Text:
        return "action_Rollback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

    
        com=Command()
        com.open('XXXX', 'xxxxxx', 'XXXXXXXXXX')

        siteId = tracker.get_slot('code_site_slot')
        sector = tracker.get_slot('Sector')
        tech2g = tracker.get_slot('Tech2g')
        tech3g = tracker.get_slot('Tech3g')
        tech4g = tracker.get_slot('Tech4g')
    
      



class Action_Ret(Action):

    def name(self) -> Text:
        return "action_Ret"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

    
        com=Command()
        com.open('XXXX', 'xxxxxx', 'XXXXXXXXXX')

        siteId = tracker.get_slot('code_site_slot')
        sector = tracker.get_slot('Sector')
        tech2g = tracker.get_slot('Tech2g')
        tech3g = tracker.get_slot('Tech3g')
        tech4g = tracker.get_slot('Tech4g')
        userlabel = 1240 
        r = RetCommand()
        cmd_ret = r.get_tilt(siteId , userlabel)
        


class ActionUtterGreet(Action):

     def name(self) -> Text:
         return "utter_greet"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        
        mssg = tracker.get_latest_message.txt
        lan = detect(mssg)
        lan = 'en' 
        if(lan== 'en'):
            dispatcher.utter_template("utter_greet_en", tracker)
            print("en")
        elif(lan=='fr'):
            dispatcher.utter_template("utter_greet_fr", tracker)
            print("fr")
        return []


