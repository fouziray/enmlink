from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet, EventType
import datetime
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa.shared.core.constants import (
    USER_INTENT_OUT_OF_SCOPE,
    ACTION_LISTEN_NAME,
    ACTION_RESTART_NAME,
    ACTION_SESSION_START_NAME,
    ACTION_DEFAULT_FALLBACK_NAME,
    ACTION_DEACTIVATE_LOOP_NAME,
    ACTION_REVERT_FALLBACK_EVENTS_NAME,
    ACTION_DEFAULT_ASK_AFFIRMATION_NAME,
    ACTION_DEFAULT_ASK_REPHRASE_NAME,
    ACTION_BACK_NAME,
    REQUESTED_SLOT,
)
from .commands import path, check_2g , check_3g , check_4gFDD , check_tilt , check_4gTDD , manageCodeSite , manageCodeSiteSector , format , buildCodeSite , Command , GsmCommand ,g3rncCommand , g3NodeCommand , g4FDDCommand , g4TDDCommand ,OptimCommand , RetCommand
import pandas as pd 
import matplotlib.pyplot as plt
path =  "./store_rollback/"
import re
from os.path import exists
import os
import requests
from rasa_sdk.events import SessionStarted, ActionExecuted
from threading import Timer


file_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = 'store_rollback'



com=Command()

class manageSession(object):
    nb=0
    def __new__(cls):
        
        cls.nb+=1
        print(cls.nb)
        if not hasattr(cls, 'instance'):
             cls.instance = super(manageSession, cls).__new__(cls)
        if cls.nb==1:
            com.open(os.environ.get('URL',''),os.environ.get('USERNAME',''),os.environ.get('PASSWORD',''))
        return cls.instance
    
    @staticmethod
    def delete():
        manageSession.nb-=1
        print(manageSession.nb)
        print('Inside the destructor')
        if(manageSession.nb==0):
            com.closesession()
    @staticmethod
    def setTimeout(fn, ms, *args, **kwargs):
        t = Timer(ms / 1000, fn, args=args, kwargs=kwargs)
        t.start()
        return t
	
class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"
    @staticmethod
    def fun( ):
        manageSession.delete()
    @staticmethod
    def fetch_slots(tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        """Collect slots that contain the user's infos."""

        slots = []
        for key in list(domain['slots'].keys()):
            value = tracker.get_slot(key)
            if value is not None:
                slots.append(SlotSet(key=key, value=value))
                print(key,value)
        return slots
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        events = [SessionStarted()]
        metadata = tracker.get_slot("session_started_metadata")
    
        events.extend(self.fetch_slots(tracker,domain))


        
        url = "http://localhost:8000/dtsession/" # api @


        try:
            response = requests.get(url+str(tracker.current_state()['sender_id']  ))

            if response.status_code == 200:
                print(response.text)
                encodedRes=json.loads(response.text)
                print(encodedRes["endDate"])
                now=datetime.datetime.now()
                currentdatetime=datetime.datetime.strptime(encodedRes["endDate"], '%Y-%m-%dT%H:%M:%SZ')
                difference=(currentdatetime - now).total_seconds()
                if( difference > 0):
                    print(difference)
                    c=manageSession()
                    c.setTimeout(self.fun, 5000) # 5 seconds for testing / change with difference for real deployment
                else:
                    print("session is already done since "+str(difference)+" seconds")
            else:
                print(f"POST request failed with status code: {response.status_code}")
        except Exception as exp:
           print(f"An error occurred: {str(exp)}")
       
        print(tracker.get_slot("pathTilt"))
        # the session should begin with a `session_started` event and an `action_listen`
        # as a user message follows
        events.append(ActionExecuted("action_listen"))
        return events

class ActionGreet(Action):

    def name(self) -> Text:
        return "action_utter_greet"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        person = tracker.get_slot("Person")
        if person:
            reponse = "Hello , " +str(person) 
            dispatcher.utter_message(text=reponse)
        else : 
            reponse = "Hello"
            dispatcher.utter_message(text=reponse)
            # ouverture session enm
          #  com.open('XXXX', 'xxxxxx', 'XXXXXXXXXX')
        return []

class ActionConnectionTroubleshoot(Action):

    def name(self) -> Text:
        return "action_connection_troubleshoot"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        codeSite = tracker.get_slot("code_site")
        if(codeSite == None):
            dispatcher.utter_message("you haven't entered a code site")
            return[]
        else:
            o=OptimCommand()
            com.execute(o.ping_issue())
            dispatcher.utter_message(text="ping should be working now")
            # ouverture session enm
          #  com.open('XXXX', 'xxxxxx', 'XXXXXXXXXX')
        return []


class ActionInform(Action):

    def name(self) -> Text:
        return "action_inform_site"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global path
        codeSite = tracker.get_slot("code_site")
        if(codeSite == None):
            dispatcher.utter_message("you haven't entered a code site")
            return[]
        else:
            dispatcher.utter_message("Got it, "+codeSite+" it is !")

            path += codeSite + '/'                # chemin de sauvgarde des modifications su rle site 
            # ouverture session enm
          #  com.open('XXXX', 'xxxxxx', 'XXXXXXXXXX')
        return []





class ActionTechStatus(Action):

    def name(self) -> Text:
        return "action_status_tech"    # a function that handles , multiple and also all technologies status

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response2g=''
        response3g=''
        response4g=''
        codeSite = tracker.get_slot("code_site")
        if(codeSite == None):
            dispatcher.utter_message("you haven't entered a code site")
            return[]
        
        message = (tracker.latest_message)['text']  
         
        sites = manageCodeSite(codeSite)
        site2g = sites[0]
        site3g = sites[1]
        site4g = sites[2]        
        site4gTDD = sites[3] 
        print(str(sites)+"__________________________")               
        # check one or multiple techs
        if(("2" in message) and (tracker.get_slot("Tech2g")!= None)):
            if(site2g == None):
                if(codeSite[-1].lower()=='l'  or codeSite[-1].lower()=='u' ):
                    site2g=codeSite[:-1]
                else:
                    site2g=codeSite
            response2g = check_2g(site2g)
            if(response2g.empty ):
                dispatcher.utter_message(text="2G technology doesn't exist")  
            else:
                #save 2G status
                path2g = path + str(site2g) + "_2g.json"
                file_path = os.path.join(file_dir, csv_folder,  str(codeSite) + "_2g.json")
                if( not exists(file_path) ):
                    response2g.to_json(file_path , orient = 'records') 
                dispatcher.utter_message(text="status for 2G: "+' ,'.join(response2g[["GeranCellId", "state"]].to_string(header=False , index = False).split('\n')))


        if(("3" in message) and (tracker.get_slot("Tech3g")!= None)):
            if( site3g == None):
                if(codeSite[-1].lower()=='l'):
                    site3g='U'.join(codeSite.rsplit(codeSite[-1:], 1))
                else:
                    site3g=codeSite+'U'
            print(site3g)  
            response3g = check_3g(site3g)
                            #save 3G status
            if(response3g.empty):
                dispatcher.utter_message(text="3G technology doesn't exist")  
            else:
                path3g = path + str(site3g) + "_3g.json"
                file_path = os.path.join(file_dir, csv_folder,  str(codeSite) + "_3g.json")
                if( not exists(file_path) ):
                    response3g.to_json(file_path , orient = 'records') 
                dispatcher.utter_message(text="status for 3G: "+' ,'.join(response3g[["UtranCellId", "operationalState"]].to_string(header=False , index = False).split('\n')))

        if(("4" in message) and (tracker.get_slot("Tech4g")!= None) ):
            if(site4g == None):
                if(codeSite[-1].lower()=='u'):
                    site4g='L'.join(codeSite.rsplit(codeSite[-1:], 1))
                else:
                    site4g=codeSite+'L'
            response4g = check_4gFDD(site4g)
            if(response4g.empty):
                dispatcher.utter_message(text="4G technology doesn't exist")  
            else:
                            #save 4G status
                path4g = path + str(site4g) + "_4g.json"
                file_path = os.path.join(file_dir, csv_folder,  str(codeSite) + "_4g.json")
                if( not exists(file_path) ):
                    response4g.to_json(file_path , orient = 'records') 
                dispatcher.utter_message(text="status for 4G: "+' ,'.join(response4g[["EUtranCellFDDId", "administrativeState"]].to_string(header=False , index = False).split('\n')))

        if(tracker.latest_message['intent'].get('check_all_techs')):

            response2g = check_2g(site2g)
            response3g = check_3g(site3g)
            response4g = check_4gFDD(site4g)
        
        
#        response  = response2g + response3g + response4g

#        dispatcher.utter_message(text=response)
        
        return []
       



class Action_Lock_tech(Action):
   
    def name(self) -> Text:
        return "action_lock_tech"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response1_3g=None
        response2_3g=None
        response2_3g=None
        # recuperer le code du site 
        codeSite = tracker.get_slot("code_site")
        
        if(codeSite == None):
            dispatcher.utter_message("you haven't entered site code")
            return[]

        sites = manageCodeSite(codeSite)
        
        site2g = sites[0]
        site3g = sites[1]
        site4g = sites[2]

        if(site2g):
            g2_obj = GsmCommand()
            
            # recuperer la bande
            bande = tracker.get_slot("Tech2g")
            if(bande == None):
                dispatcher.utter_message("you haven't entered which bands to lock for 2G")
                return[]


            if ((bande.upper() == "2G") or (bande.upper() == "DCS")):
                bande = 0    
            block_state_2G = g2_obj.set(site2g , bande , 'INACTIVE')
            
            com.execute(block_state_2G)
            SlotSet("blocked_tech_slot" ,['2G'])
            
            if (bande == 0 ):
                dispatcher.utter_message("technologie 2G locked"+block_state_2G)
            else : 
                dispatcher.utter_message("technologie 2G locked in bande " +str(bande)+block_state_2G)
       
        if(site3g):
            g3_obj = g3rncCommand()
            
            # recuperer la bande
            bande = tracker.get_slot("Tech3g")
            if(bande == None):
                dispatcher.utter_message("You need to specify which 3G band, or both")
                return[]
            
            bande1 = 'U900'
            bande2 = 'U2100'
           
            if('900' in bande):    
                block_state_3G_b1 = g3_obj.set(site3g , bande1 , 'LOCKED')
                response1_3g = com.execute(block_state_3G_b1)         #g3_obj.execute(block_state_3G_b1)
                
                SlotSet("blocked_tech_slot" ,[bande1])

            if('2100' in bande):
                block_state_3G_b2 = g3_obj.set(site3g , bande2 , 'LOCKED')
                response2_3g =  com.execute(block_state_3G_b2)                         #g3_obj.execute(block_state_3G_b2)
                
                SlotSet("blocked_tech_slot" ,[bande2])

            if (('3g' in bande)or ('3G' in bande)):     # blocker la technologie entière
                block_state_3G_b1 = g3_obj.set(site3g , bande1 , 'LOCKED')   
                block_state_3G_b2 = g3_obj.set(site3g , bande2 , 'LOCKED')
                response1_3g = com.execute(block_state_3G_b1)     #g3_obj.execute(block_state_3G_b1)
                response2_3g = com.execute(block_state_3G_b2)     #g3_obj.execute(block_state_3G_b2)
            
                SlotSet("blocked_tech_slot" ,[bande1 , bande2])

            if(response1_3g):
                dispatcher.utter_message("technologie 3G bande U900 blocked")
            if(response2_3g) : 
                dispatcher.utter_message("technoligie 3G bande U2100 blocked in bande ")
       


        if(site4g):
            g4_obj = g4FDDCommand()
            response1_4g=None
            response_4g=None
            response2_4g=None
            # recuperer la bande
            bande = tracker.get_slot("Tech4g")
            if(bande == None):
                dispatcher.utter_message("You need to specify which 4G frequency band, or both")
                return[]
            bande1 = 'L1800'
            bande2 = 'L2100'
           
            if('1800' in bande):    
                bande1= '3'
                block_state_4G_b1 = g4_obj.set(site4g , bande1 , 'LOCKED')
                response1_4g = com.execute(block_state_4G_b1)

                SlotSet("blocked_tech_slot" ,[bande1])

            if('2100' in bande):
                bande2= '1'
                block_state_4G_b2 = g4_obj.set(site4g , bande2 , 'LOCKED')
                response2_4g = com.execute(block_state_4G_b2)

                SlotSet("blocked_tech_slot" ,[bande2])

            if (('4g' in bande)or ('4G' in bande)): 
                bande = 0                                                    # blocker la technologie entière
                block_state_4G = g4_obj.set(site4g , bande , 'LOCKED')   
                
                response_4g = com.execute(block_state_4G)
               
                SlotSet("blocked_tech_slot" ,['4G'])
            

            if(response1_4g):
                dispatcher.utter_message("technology 4G bande L1800 blocked"+response1_4g)
             
            if(response2_4g) : 
                dispatcher.utter_message("technology 4G bande L2100 blocked in bande"+response2_4g)
    
            if(response_4g):
                dispatcher.utter_message("technology 4G blocked"+response_4g)
               

        return [SlotSet("Tech4g",None)]
       
     



class Action_UnLock_tech(Action):
   
    def name(self) -> Text:
        return "action_unlock_tech"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response1_3g=None
        response2_3g=None
        response2_3g=None
        # recuperer le code du site 
        codeSite = tracker.get_slot("code_site")
        
        if(codeSite == None):
            dispatcher.utter_message("you haven't entered site code")
            return[]

        sites = manageCodeSite(codeSite)
        
        site2g = sites[0]
        site3g = sites[1]
        site4g = sites[2]

        if(site2g):
            g2_obj = GsmCommand()
            
            # recuperer la bande
            bande = tracker.get_slot("Tech2g")
            if(bande == None):
                dispatcher.utter_message("you haven't entered which bands to unlock for 2G")
                return[]


            if ((bande.upper() == "2G") or (bande.upper() == "DCS")):
                bande = 0    
            unblock_state_2G = g2_obj.set(site2g , bande , 'ACTIVE')
            
            com.execute(unblock_state_2G)
            SlotSet("unblocked_tech_slot" ,['2G'])
            
            if (bande == 0 ):
                dispatcher.utter_message("technologie 2G unlocked"+unblock_state_2G)
            else : 
                dispatcher.utter_message("technologie 2G unlocked in bande " +str(bande)+unblock_state_2G)
       
        if(site3g):
            g3_obj = g3rncCommand()
            
            # recuperer la ba}}nde
            bande = tracker.get_slot("Tech3g")
            if(bande == None):
                dispatcher.utter_message("You need to specify which 3G band, or both")
                return[]
            
            bande1 = 'U900'
            bande2 = 'U2100'
           
            if('900' in bande):    
                unblock_state_3G_b1 = g3_obj.set(site3g , bande1 , 'UNLOCKED')
                response1_3g = com.execute(unblock_state_3G_b1)         #g3_obj.execute(block_state_3G_b1)
                
                SlotSet("unblocked_tech_slot" ,[bande1])

            if('2100' in bande):
                unblock_state_3G_b2 = g3_obj.set(site3g , bande2 , 'UNLOCKED')
                response2_3g =  com.execute(unblock_state_3G_b2)                         #g3_obj.execute(block_state_3G_b2)
                
                SlotSet("unblocked_tech_slot" ,[bande2])

            if (('3g' in bande)or ('3G' in bande)):     # blocker la technologie entière
                unblock_state_3G_b1 = g3_obj.set(site3g , bande1 , 'UNLOCKED')   
                unblock_state_3G_b2 = g3_obj.set(site3g , bande2 , 'UNLOCKED')
                response1_3g = com.execute(unblock_state_3G_b1)     #g3_obj.execute(block_state_3G_b1)
                response2_3g = com.execute(unblock_state_3G_b2)     #g3_obj.execute(block_state_3G_b2)
            
                SlotSet("unblocked_tech_slot" ,[bande1 , bande2])

            if(response1_3g):
                dispatcher.utter_message("technologie 3G bande U900 unblocked")
            if(response2_3g) : 
                dispatcher.utter_message("technoligie 3G bande U2100 unblocked in bande ")
       


        if(site4g):
            g4_obj = g4FDDCommand()
            response1_4g=None
            response_4g=None
            response2_4g=None
            # recuperer la bande
            bande = tracker.get_slot("Tech4g")
            if(bande == None):
                dispatcher.utter_message("You need to specify which 4G frequency band, or both")
                return[]
            bande1 = 'L1800'
            bande2 = 'L2100'
           
            if('1800' in bande):    
                bande1= '3'
                unblock_state_4G_b1 = g4_obj.set(site4g , bande1 , 'UNLOCKED')
                response1_4g = com.execute(unblock_state_4G_b1)

                SlotSet("unblocked_tech_slot" ,[bande1])

            if('2100' in bande):
                bande2= '1'
                unblock_state_4G_b2 = g4_obj.set(site4g , bande2 , 'UNLOCKED')
                response2_4g = com.execute(unblock_state_4G_b2)

                SlotSet("unblocked_tech_slot" ,[bande2])

            if (('4g' in bande)or ('4G' in bande)): 
                bande = 0                                                    # blocker la technologie entière
                unblock_state_4G = g4_obj.set(site4g , bande , 'UNLOCKED')   
                
                response_4g = com.execute(unblock_state_4G)
               
                SlotSet("unblocked_tech_slot" ,['4G'])
            

            if(response1_4g):
                dispatcher.utter_message("technology 4G bande L1800 unblocked"+response1_4g)
             
            if(response2_4g) : 
                dispatcher.utter_message("technology 4G bande L2100 unblocked in bande"+response2_4g)
    
            if(response_4g):
                dispatcher.utter_message("technology 4G unblocked"+response_4g)
               

        return [SlotSet("Tech4g",None)]
       


class ActionTilt(Action):

    def name(self) -> Text:
        return "action_set_tilt"    

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        codeSite = tracker.get_slot("code_site")
        if(codeSite == None):
            dispatcher.utter_message("you haven't entered a code site")
            return[]
           
        tech = tracker.get_slot("Tech4g")
        tilt_com = RetCommand()
        # get a list of tilt values   
        responseTilt = check_tilt(codeSite)

                #save tilt status
        path_tilt = path + str(codeSite) + "_tilt.json"
        file_path = os.path.join(file_dir, csv_folder,  str(codeSite) + "_tilt.json")

        responseTilt.to_json(file_path , orient = 'records') 
        
        dispatcher.utter_message(text = "tilt changed successfully "+file_path+' ')

        tilt_request = (tracker.latest_message)['text']
        
        #check_tilt(codeSite) # check initial values and save it in path : .store_rollback/$(codeSite)_tilt.json

        if (("max" in tilt_request) or ("up" in tilt_request)):
            # uptilt or maxtilt
            com.execute(tilt_com.set_tilt(codeSite , 0))  # le plus haut possible 

            dispatcher.utter_message(text="Maxtilt is successfully done")
            return[]

        elif(("min" in  tilt_request) or ("down" in tilt_request)):
            # downtilt 
            com.execute(tilt_com.set_tilt(codeSite , 100)) # le plus bas possible 
            dispatcher.utter_message(text="Downtilt is successfully done")
            return[SlotSet("pathTilt" , file_path )]
        
        return[]

     


class ActionRollback(Action):

    def name(self) -> Text:
        return "action_rollback"    

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        codeSite = tracker.get_slot("code_site")

        if(codeSite == None):
            dispatcher.utter_message("you haven't entered a code site")
            return[]
        caslot=tracker.get_slot("Tech4g")

        if(caslot!=None):
            print("jejejejaaaaaaaa"+caslot)
        path2g = os.path.join(file_dir, csv_folder,  str(codeSite) + "_2g.json")
        path3g = os.path.join(file_dir, csv_folder,  str(codeSite) + "_3g.json")
        path4gFDD = os.path.join(file_dir, csv_folder,  str(codeSite) + "_4g.json")
        pathTilt = tracker.get_slot("pathTilt")
        file_path = os.path.join(file_dir, csv_folder,  str(codeSite) + "_tilt.json")
        if( pathTilt != None):
            print(pathTilt)
        
        if(exists(path2g)):
            com2g = GsmCommand()
            listcmd=com2g.rollback_2g(path2g)
        
            for val in listcmd:
                com.execute(val)
            os.remove(path2g)
            dispatcher.utter_message(text= "rollback 2g done!")

        if(exists(path3g)):
            com3g = g3rncCommand()
            listcmd=com3g.rollback_3g(path3g)
            for val in listcmd:
                com.execute(val)
            os.remove(path3g)

            dispatcher.utter_message(text= "rollback 3g done!")


        if(exists(path4gFDD)):
            com4gFDD = g4FDDCommand()
            listcmd=com4gFDD.rollback_4g(path4gFDD)
            for val in listcmd:
                com.execute(val)
            os.remove(path4gFDD)

            dispatcher.utter_message(text= "rollback 4g done!")

        
        comTilt = RetCommand()
        reverseCommands=comTilt.rollback_tilt(file_path)
        if(reverseCommands != None):
            for val in reverseCommands:
                com.execute(val)
            os.remove(path4gFDD)
        else:
            dispatcher.utter_message(text= "rollback tilt done!")

        return[]
        


class ActionThroughput(Action):

    def name(self) -> Text:
        return "action_throughput_info"    

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        codeSite = tracker.get_slot("code_site")
        if(codeSite == None):
            dispatcher.utter_message("you haven't entered a code site")
            return[]
        
        throughput = tracker.get_slot("throughput_slot")
        if(throughput == None):
            dispatcher.utter_message("what is the value of the throughput you 've got ?")
            return[]
        
        throughput=[ int(s) for s in  re.findall(r'\d+', throughput)]
        if (len(throughput)>0):
            throughput=throughput[0]

            if (throughput < 50):
                dispatcher.utter_message("the throughput is bad")
            if (50<=throughput<75):
                dispatcher.utter_message("the throughput is Average")
            if (75<=throughput):
                dispatcher.utter_message("the throughput is good")
        return[]


        





class ActionLockSector(Action):
   
    def name(self) -> Text:
        return "action_lock_sector"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # recuperer la technologie 
        codeSite = tracker.get_slot("code_site")
        
        if(codeSite is None):
            dispatcher.utter_message("you haven't entered site code")
            return[]
      
        sector_to_block = tracker.get_slot("Sector_slot")
        if(sector_to_block == None):
            dispatcher.utter_message("i didn't get the sector to block")
            return[]

        bande2g=''
        bande3g=''
        bande4g=''        
        if (tracker.get_slot("Tech2g") is not None):
            bande2g = tracker.get_slot("Tech2g")
        if (tracker.get_slot("Tech3g") is not None):
            bande3g = tracker.get_slot("Tech3g")
        if (tracker.get_slot("Tech4g") is not None):
            bande4g = tracker.get_slot("Tech4g")

        
            
        if(('900' in bande2g) or ('1800' in bande2g)):
            sectors = manageCodeSiteSector(codeSite , bande2g ,sector_to_block)
            dispatcher.utter_message(text="this is site "+str(sectors)) 
            obj2g = GsmCommand()
            if(sectors[0] or sectors[3]):
                sectors[0]= sectors[0] or sectors[3]
                get_s1 = obj2g.get(sectors[0],bande2g)
                com.execute(get_s1)
                set_s1 = obj2g.set(sectors[0] , bande2g , 'UNACTIVE')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 bande "+bande2g+" for 2G is now INACTIVE") 

            if(sectors[1] or sectors[4]):
                sectors[1]=sectors[1] or sectors[4]
                get_s2 = obj2g.get(sectors[1],bande2g)
                com.execute(get_s2)
                set_s2 = obj2g.set(sectors[1] , bande2g , 'UNACTIVE')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 bande "+bande2g+" for 2G is now INACTIVE") 

            if(sectors[2]):
                get_s3 = obj2g.get(sectors[2],bande2g)
                com.execute(get_s3)
                set_s3 = obj2g.set(sectors[2] , bande2g , 'UNACTIVE')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 bande "+bande2g+" for 2G is now INACTIVE") 
            
            SlotSet("blocked_sector_slot" , sector_to_block)
            return[]
            
        elif(('900' in bande3g) or ('2100' in bande3g)):
            sectors=manageCodeSiteSector(codeSite , bande3g ,sector_to_block)
            dispatcher.utter_message(text="this is site 3"+str(sectors)) 
            if ('900' in bande3g ):
                bande3g="U900"
            else:
                bande3g="U2100"
            obj3g = g3rncCommand()
            if(sectors[0] or sectors[3]):
                if(sectors[1]):
                    sec=sectors[0]
                else:
                    sec=sectors[3]
                get_s1 = obj3g.get(sec,bande3g)
                com.execute(get_s1)
                set_s1 = obj3g.set(sec, bande3g , 'BLOCKED')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 bande "+str(bande3g)+" for 3G is now BLOCKED") 

            if(sectors[1] or sectors[4]):
                if(sectors[1]):
                    sec=sectors[1]
                else:
                    sec=sectors[4]
                
                get_s2 = obj3g.get(sec,bande3g)
                com.execute(get_s2)
                set_s2 = obj3g.set(sec , bande3g , 'BLOCKED')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 bande "+str(bande3g)+" for 3G is now BLOCKED") 

            if(sectors[2] or sectors[5]):
                if(sectors[1]):
                    sec=sectors[2]
                else:
                    sec=sectors[5]
                get_s3 = obj3g.get(sec,bande3g)
                com.execute(get_s3)
                set_s3 = obj3g.set(sec, bande3g , 'BLOCKED')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 bande "+str(bande3g)+" for 2G is now BLOCKED") 

            SlotSet("blocked_sector_slot" , sector_to_block)
            return[]

        elif(('1800' in bande4g) or ('2100' in bande4g)):
            sectors= manageCodeSiteSector(codeSite , bande4g ,sector_to_block)
            #dispatcher.utter_message(text="this is site 4 "+str(sectors)) 
            if ('1800' in bande4g ):
                bande4g=0
            else:
                bande4g=1

            obj4gFDD = g4FDDCommand()
            if(sectors[0]):
                get_s1 = obj4gFDD.get(sectors[0],bande4g)
                com.execute(get_s1)
                set_s1 = obj4gFDD.set(sectors[0] , bande4g , 'BLOCKED')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 bande "+str(bande4g)+" for 4G is now BLOCKED") 

            if(sectors[1]):
                get_s2 = obj4gFDD.get(sectors[1],bande4g)
                com.execute(get_s2)
                set_s2 = obj4gFDD.set(sectors[1] , bande4g , 'BLOCKED')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 bande "+str(bande4g)+" for 4G is now BLOCKED") 

            if(sectors[2]):
                get_s3 = obj4gFDD.get(sectors[2],bande4g)
                com.execute(get_s3)
                set_s3 = obj4gFDD.set(sectors[2] , bande4g , 'BLOCKED')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 bande "+str(bande4g)+" for 4G is now BLOCKED") 
            if(sectors[3]):
                get23 = obj4gFDD.get(sectors[3],bande4g)
                com.execute(get23)
              
                com.execute(obj4gFDD.set(sectors[3] , bande4g , 'BLOCKED'))
                dispatcher.utter_message(text="Sector S1 band "+str(bande4g)+" in 4G is now BLOCKED") 
            if(sectors[4]):
                get23 = obj4gFDD.get(sectors[4],bande4g)
                com.execute(get23)
              
                com.execute(obj4gFDD.set(sectors[4] , bande4g , 'BLOCKED'))
                dispatcher.utter_message(text="Sector S2 band "+str(bande4g)+" in 4G is now BLOCKED") 
            if(sectors[5]):
                get23 = obj4gFDD.get(sectors[5],bande4g)
                com.execute(get23)
              
                com.execute(obj4gFDD.set(sectors[5] , bande4g , 'BLOCKED'))
                dispatcher.utter_message(text="Sector S3 band "+str(bande4g)+" in 4G is now BLOCKED") 

            SlotSet("blocked_sector_slot" , sector_to_block)
            return[]

        else: 
            dispatcher.utter_message(text= "Sorry but i didn't recognize the band for the sector you want to lock")
            return[]
            
            








class ActionUnLockSector(Action):
   
    def name(self) -> Text:
        return "action_unlock_sector"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # recuperer la technologie 
        codeSite = tracker.get_slot("code_site")
        
        if(codeSite is None):
            dispatcher.utter_message("you haven't entered site code")
            return[]
      
        sector_to_unblock = tracker.get_slot("Sector_slot")
        if(sector_to_unblock == None):
            dispatcher.utter_message("i didn't get the sector to unblock")
            return[]

        bande2g=''
        bande3g=''
        bande4g=''        
        if (tracker.get_slot("Tech2g") is not None):
            bande2g = tracker.get_slot("Tech2g")
        if (tracker.get_slot("Tech3g") is not None ):
            bande3g = tracker.get_slot("Tech3g")
        if (tracker.get_slot("Tech4g") is not None ):
            bande4g = tracker.get_slot("Tech4g")

        
            
        if(('900' in bande2g) or ('1800' in bande2g)):
            sectors = manageCodeSiteSector(codeSite , bande2g ,sector_to_unblock)
            dispatcher.utter_message(text="this is site "+str(sectors)) 
            obj2g = GsmCommand()
            if(sectors[0] or sectors[3]):
                sectors[0]=sectors[0] or sectors[3]
                get_s1 = obj2g.get(sectors[0],"GSM900")
                com.execute(get_s1)
                set_s1 = obj2g.set(sectors[0] , bande2g , 'ACTIVE')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 bande "+bande2g+" for 2G is now ACTIVE") 

            if(sectors[1] or sectors[4]):
                sectors[1]=sectors[1] or sectors[4]
                get_s2 = obj2g.get(sectors[1],"GSM900")
                com.execute(get_s2)
                set_s2 = obj2g.set(sectors[1] , bande2g , 'ACTIVE')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 bande "+bande2g+" for 2G is now ACTIVE") 

            if(sectors[2] or sectors[5]):
                sectors[2]= sectors[2] or sectors[5]
                get_s3 = obj2g.get(sectors[2],"GSM900")
                com.execute(get_s3)
                set_s3 = obj2g.set(sectors[2] , bande2g , 'ACTIVE')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 bande "+bande2g+" for 2G is now ACTIVE") 
            
            SlotSet("unblocked_sector_slot" , sector_to_unblock)
            return[]
            
        elif(('900' in bande3g) or ('2100' in bande3g)):
            sectors=manageCodeSiteSector(codeSite , bande3g ,sector_to_unblock)
            dispatcher.utter_message(text="this is site 3"+str(sectors)) 
            if ('900' in bande3g ):
                bande3g="U900"
            else:
                bande3g="U2100"
            obj3g = g3rncCommand()
            if(sectors[0] or sectors[3]):
                sectors[0]=sectors[0] or sectors[3]
                get_s1 = obj3g.get(sectors[0],bande3g)
                com.execute(get_s1)
                set_s1 = obj3g.set(sectors[0] , bande3g , 'UNBLOCKED')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 bande "+bande3g+" for 3G is now UNBLOCKED") 

            if(sectors[1] or sectors[4] ):
                sectors[1]=sectors[1] or sectors[4]                
                get_s2 = obj3g.get(sectors[1],bande3g)
                com.execute(get_s2)
                set_s2 = obj3g.set(sectors[1] , bande3g , 'UNBLOCKED')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 bande "+bande3g+" for 3G is now UNBLOCKED") 

            if(sectors[2] or sectors[5] ):
                sectors[2]=sectors[2] or sectors[5]                
                get_s3 = obj3g.get(sectors[2],bande3g)
                com.execute(get_s3)
                set_s3 = obj3g.set(sectors[2] , bande3g , 'UNBLOCKED')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 bande "+bande3g+" for 2G is now UNBLOCKED") 

            SlotSet("unblocked_sector_slot" , sector_to_unblock)
            return[]

        elif(('1800' in bande4g) or ('2100' in bande4g)):
            sectors= manageCodeSiteSector(codeSite , bande4g ,sector_to_unblock)
            dispatcher.utter_message(text="this is site 4 "+str(sectors)) 
            if ('1800' in bande4g ):
                bande4g=0
            else:
                bande4g=1
            
            obj4gFDD = g4FDDCommand()
            
            if(sectors[0] or sectors[3]):
                sectors[0]=sectors[0] or sectors[3]
                get_s1 = obj4gFDD.get(sectors[0],bande4g)
                com.execute(get_s1)
                set_s1 = obj4gFDD.set(sectors[0] , bande4g , 'UNBLOCKED')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 band "+str(bande4g)+" for 4G is now UNBLOCKED") 

            if(sectors[1] or sectors[4]):
                sectors[1]=sectors[1] or sectors[4]
                get_s2 = obj4gFDD.get(sectors[1],bande4g)
                com.execute(get_s2)
                set_s2 = obj4gFDD.set(sectors[1] , bande4g , 'UNBLOCKED')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 band "+str(bande4g)+" for 4G is now UNBLOCKED") 

            if(sectors[2] or sectors[5]):
                sectors[2]=sectors[2] or sectors[5]
                get_s3 = obj4gFDD.get(sectors[2],bande4g)
                com.execute(get_s3)
                set_s3 = obj4gFDD.set(sectors[2] , bande4g , 'UNBLOCKED')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 band "+str(bande4g)+" for 4G is now UNBLOCKED") 
            
            SlotSet("unblocked_sector_slot" , sector_to_unblock)
            return[]

        else: 
            dispatcher.utter_message(text= "Sorry but i didn't recognize the band for the sector you want to unlock")
            return[]
               
#class ActionLockSectorAll(): # to implement but not priority 



class ActionExtend(Action): #executed each time the session is new due to it no being included in stories and being a mapping source for slot duration

    def find_con(self,n, s):
        result = re.search('\d{%s}'%n, s)
        return result.group(0) if result else result
    
    def strr(self,s):
        return [int(s) for s in re.findall(r'-?\d+\.?\d*',s)]
    def name(self) -> Text:
        return "action_extend_session"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        url = "http://localhost:8000/extendSession/" # api @
        

        codeSite = tracker.get_slot("code_site")
        
        #if(codeSite is None):
        #    dispatcher.utter_message("you haven't entered site code")
        #    return[]
        #dispatcher.utter_message("this is sender"+str(tracker.current_state()['sender_id']  ))
        
        time = tracker.get_slot("duration")
        if(time is None or time >30 ):
        

            time = 15

            dispatcher.utter_message("Your session is extended by 15 mins")
        
        else:
            
            dispatcher.utter_message("Your session is extended by "+str(time)+ " mins")
        
        data ={
	"session_id":2,
	"time": time 
}
       


        try:
            response = requests.post(url, json=data)

            if response.status_code == 200:
                return["POST request was successful!"]
            else:
                return[f"POST request failed with status code: {response.status_code}"]
        except Exception as exp:
            return[f"An error occurred: {str(exp)}"]


            

