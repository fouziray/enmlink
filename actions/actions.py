from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet  

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .commands import path, check_2g , check_3g , check_4gFDD , check_tilt , check_4gTDD , manageCodeSite , manageCodeSiteSector , format , buildCodeSite , Command , GsmCommand ,g3rncCommand , g3NodeCommand , g4FDDCommand , g4TDDCommand ,OptimCommand , RetCommand
import pandas as pd 
import matplotlib.pyplot as plt
path =  "./store_rollback/"

from os.path import exists
import os
file_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = 'store_rollback'



com=Command()

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
            path += codeSite + '/'                # chemin de sauvgarde des modifications su rle site 
            # ouverture session enm
          #  com.open('XXXX', 'xxxxxx', 'XXXXXXXXXX')
        return []





class ActionTechStatus(Action):

    def name(self) -> Text:
        return "action_status_tech"    # a function that handles , multiple and also all technologies status

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        codeSite = tracker.get_slot("code_site")
        if(codeSite == None):
            dispatcher.utter_message("you haven't entered a code site")
            return[]
        
        message = tracker.latest_message.text   
        sites = manageCodeSite(codeSite)
        site2g = sites[0]
        site3g = sites[1]
        site4g = sites[2]        
        site4gTDD = sites[3]                
        # check one or multiple techs
        if(("2" in message) and (tracker.get_slot["Tech2g"]!= None)):
            response2g = check_2g(site2g)
                #save 2G status
            path2g = path + str(site2g) + "_2g.json"
            response2g.to_json(path2g , orient = 'records') 
            SlotSet("path2g" , path2g)          # save path in slot 


        if(("3" in message) and (tracker.get_slot["Tech3g"]!= None)):
            response3g = check_3g(site3g)
                            #save 3G status
            path3g = path + str(site3g) + "_3g.json"
            response3g.to_json(path3g , orient = 'records') 
            SlotSet("path3g" , path3g)

        if(("4" in message) and (tracker.get_slot["Tech4g"]!= None)):
            response4g = check_4gFDD(site4g)
                            #save 4G status
            path4g = path + str(site4g) + "_4g.json"
            response4g.to_json(path4g , orient = 'records') 
            SlotSet("path4gFDD" , path4g)

        if(tracker.latest_message['intent'].get('check_all_techs')):
            response2g = check_2g(site2g)
            response3g = check_3g(site3g)
            response4g = check_4gFDD(site4g)
        
        
        response  = response2g + response3g + response4g

        dispatcher.utter_message(text=response)
        
        return []
       



class Action_Lock_tech(Action):
   
    def name(self) -> Text:
        return "action_lock_tech"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # recuperer la technologie 
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
                dispatcher.utter_message("technoligie 2G locked in bande " +str(bande)+block_state_2G)
       
        if(site3g):
            g3_obj = g3rncCommand()
            
            # recuperer la bande
            bande = tracker.get_slot("Tech3g")
            if(bande == None):
                dispatcher.utter_message("you haven't entered the technologie or bande for 3G")
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
            
            # recuperer la bande
            bande = tracker.get_slot("Tech4g")
            if(bande == None):
                dispatcher.utter_message("you haven't entered the technologie or bande for 4G")
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
                dispatcher.utter_message("technologie 4G bande L1800 blocked")
            if(response2_4g) : 
                dispatcher.utter_message("technoligie 4G bande L2100 blocked in bande")
            if(response_4g):
                dispatcher.utter_message("technologie 4G blocked")
       
       
        return []
       
     




class Action_Unlock_tech(Action):
   
    def name(self) -> Text:
        return "action_unlock_tech"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # recuperer la technologie 
        codeSite = tracker.get_slot("code_site")
        if(codeSite == None):
            dispatcher.utter_message("you haven't entered the site code , please to add it")
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
                dispatcher.utter_message("you haven't entered the technologie or bande for 2G")
                return[]


            if ((bande == "2G") or (bande == "2g") or (bande == "DCS")):
                bande = 0    
            block_state_2G = g2_obj.set(site2g , bande , 'ACTIVE')
            com.execute(block_state_2G)

            SlotSet("unblocked_tech_slot" ,['2G'])

            if (bande == 0 ):
                dispatcher.utter_message("technologie 2G unblocked")
            else : 
                dispatcher.utter_message("technoligie 2G unblocked in bande " +str(bande))
       
        if(site3g):
            g3_obj = g3rncCommand()
            
            # recuperer la bande
            bande = tracker.get_slot("Tech3g")
            if(codeSite == None):
                dispatcher.utter_message("you haven't entered the technologie or bande for 3G")
                return[]


            bande1 = 'U900'
            bande2 = 'U2100'
           
            if('900' in bande):    
                block_state_3G_b1 = g3_obj.set(site3g , bande1 , 'UNLOCKED')
                response1_3g = com.execute(block_state_3G_b1)
                
                SlotSet("unblocked_tech_slot" ,[bande1])
            
            if('2100' in bande):
                block_state_3G_b2 = g3_obj.set(site3g , bande2 , 'UNLOCKED')
                response2_3g = com.execute(block_state_3G_b2)

                SlotSet("unblocked_tech_slot" ,[bande2])
            
            if (('3g' in bande)or ('3G' in bande)):     # deblocker la technologie entière
                block_state_3G_b1 = g3_obj.set(site3g , bande1 , 'UNLOCKED')   
                block_state_3G_b2 = g3_obj.set(site3g , bande2 , 'UNLOCKED')
                response1_3g = com.execute(block_state_3G_b1)
                response2_3g = com.execute(block_state_3G_b2)

                SlotSet("unblocked_tech_slot" ,[bande1 , bande2])

            if(response1_3g):
                dispatcher.utter_message("technologie 3G bande U900 Unlocked")
            if(response2_3g) : 
                dispatcher.utter_message("technoligie 3G bande U2100 Unlocked in bande ")
       


        if(site4g):
            g4_obj = g4FDDCommand()
            
            # recuperer la bande
            bande = tracker.get_slot("Tech4g")
            if(codeSite == None):
                dispatcher.utter_message("you haven't entered the technologie or bande for 4G")
                return[]
            bande1 = 'L1800'
            bande2 = 'L2100'
           
            if('1800' in bande):    
                bande1= '3'
                block_state_4G_b1 = g4_obj.set(site4g , bande1 , 'UNLOCKED')
                response1_4g = com.execute(block_state_4G_b1)

                SlotSet("unblocked_tech_slot" ,[bande1])

            if('2100' in bande):
                bande2= '1'
                block_state_4G_b2 = g4_obj.set(site4g , bande2 , 'UNLOCKED')
                response2_4g = com.execute(block_state_4G_b2)

                SlotSet("unblocked_tech_slot" ,[bande2])

            if (('4g' in bande)or ('4G' in bande)): 
                bande = 0                                                    # deblocker la technologie entière
                block_state_4G = g4_obj.set(site4g , bande , 'UNLOCKED')   
                response_4g = com.execute(block_state_4G)

                SlotSet("unblocked_tech_slot" ,['4G'])


            if(response1_4g):
                dispatcher.utter_message("technologie 4G bande L1800 Unlocked")
            if(response2_4g) : 
                dispatcher.utter_message("technoligie 4G bande L2100 Unlocked in bande")
            if(response_4g):
                dispatcher.utter_message("technologie 4G Unlocked")
       
       
        return []
       





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
        
        SlotSet("pathTilt" , path_tilt )


        dispatcher.utter_message(text = "tilt changed successfully"+path_tilt+' ')

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
            return[]

     


class ActionRollback(Action):

    def name(self) -> Text:
        return "action_rollback"    

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        codeSite = tracker.get_slot("code_site")
        if(codeSite == None):
            dispatcher.utter_message("you haven't entered a code site")
            return[]
         
        path2g = tracker.get_slot("path2g")
        path3g = tracker.get_slot("path3g")
        path4gFDD = tracker.get_slot("path4gFDD")
        pathTilt = tracker.get_slot("pathTilt")
        
        if(path2g):
            com2g = GsmCommand()
            com.execute(com2g.rollback_2g(path2g))
            dispatcher.utter_message(text= "rollback 2g done!")

        if(path3g):
            com3g = g3rncCommand()
            com.execute(com3g.rollback_3g(path3g))

            dispatcher.utter_message(text= "rollback 3g done!")


        if(path4gFDD):
            com4gFDD = g4FDDCommand()
            com.execute(com4gFDD.rollback_4g(path4gFDD))

            dispatcher.utter_message(text= "rollback 4g done!")

        
        if(pathTilt):
            comTilt = RetCommand()
            com.execute(comTilt.rollback_tilt(pathTilt))

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
        else:
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
        bande2g = tracker.get_slot("Tech2g")
        bande3g = tracker.get_slot("Tech3g")
        bande4g = tracker.get_slot("Tech4g")
      

        if(('900' in bande2g) or ('1800' in bande2g)):
            sectors = manageCodeSiteSector(codeSite , bande2g ,sector_to_block)
            obj2g = GsmCommand()
            if(sectors[0]):
                get_s1 = obj2g.get(sectors[0])
                com.execute(get_s1)
                set_s1 = obj2g.set(sectors[0] , bande2g , 'UNACTIVE')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 bande "+bande2g+" for 2G is now INACTIVE") 

            if(sectors[1]):
                get_s2 = obj2g.get(sectors[1])
                com.execute(get_s2)
                set_s2 = obj2g.set(sectors[1] , bande2g , 'UNACTIVE')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 bande "+bande2g+" for 2G is now INACTIVE") 

            if(sectors[2]):
                get_s3 = obj2g.get(sectors[2])
                com.execute(get_s3)
                set_s3 = obj2g.set(sectors[2] , bande2g , 'UNACTIVE')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 bande "+bande2g+" for 2G is now INACTIVE") 
            
            SlotSet("blocked_sector_slot" , sector_to_block)
            return[]
            
        elif(('900' in bande3g) or ('2100' in bande3g)):
            manageCodeSiteSector(codeSite , bande3g ,sector_to_block)
            obj3g = g3rncCommand()
            if(sectors[0]):
                get_s1 = obj3g.get(sectors[0])
                com.execute(get_s1)
                set_s1 = obj3g.set(sectors[0] , bande3g , 'BLOCKED')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 bande "+bande3g+" for 3G is now BLOCKED") 

            if(sectors[1]):
                get_s2 = obj3g.get(sectors[1])
                com.execute(get_s2)
                set_s2 = obj3g.set(sectors[1] , bande3g , 'BLOCKED')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 bande "+bande3g+" for 3G is now BLOCKED") 

            if(sectors[2]):
                get_s3 = obj3g.get(sectors[2])
                com.execute(get_s3)
                set_s3 = obj3g.set(sectors[2] , bande3g , 'BLOCKED')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 bande "+bande3g+" for 2G is now BLOCKED") 

            SlotSet("blocked_sector_slot" , sector_to_block)
            return[]

        elif(('1800' in bande4g) or ('2100' in bande4g)):
            manageCodeSiteSector(codeSite , bande4g ,sector_to_block)
            obj4gFDD = g4FDDCommand()
            if(sectors[0]):
                get_s1 = obj4gFDD.get(sectors[0])
                com.execute(get_s1)
                set_s1 = obj4gFDD.set(sectors[0] , bande4g , 'BLOCKED')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 bande "+bande4g+" for 4G is now BLOCKED") 

            if(sectors[1]):
                get_s2 = obj4gFDD.get(sectors[1])
                com.execute(get_s2)
                set_s2 = obj4gFDD.set(sectors[1] , bande4g , 'BLOCKED')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 bande "+bande4g+" for 4G is now BLOCKED") 

            if(sectors[2]):
                get_s3 = obj4gFDD.get(sectors[2])
                com.execute(get_s3)
                set_s3 = obj4gFDD.set(sectors[2] , bande4g , 'BLOCKED')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 bande "+bande4g+" for 4G is now BLOCKED") 
            
            SlotSet("blocked_sector_slot" , sector_to_block)
            return[]

        else: 
            dispatcher.utter_message(text= "Sorry but i didn't recognize the band for the sector you want to lock")
            return[]
            
        
#class ActionLockSectorAll(): # to implement but not priority 

class ActionUnlockSector(Action):
   
    def name(self) -> Text:
        return "action_unlock_sector"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # recuperer la technologie 
        codeSite = tracker.get_slot("code_site")
        
        if(codeSite == None):
            dispatcher.utter_message("you haven't entered site code")
            return[]

     
       
        sector_to_unblock = tracker.get_slot("Sector_slot")
        if(sector_to_unblock == None):
            dispatcher.utter_message("i didn't get the sector to Unblock")
            return[]
            
        bande2g = tracker.get_slot("Tech2g")
        bande3g = tracker.get_slot("Tech3g")
        bande4g = tracker.get_slot("Tech4g")
        if (bande2g is None ) :
            bande2g=''
        if (bande3g is None) :
            bande3g=''
        if (bande4g is None) : 
            bande4g=''
        if(('900' in bande2g) or ('1800' in bande2g)):
            sectors = manageCodeSiteSector(codeSite , bande2g ,sector_to_unblock)
            obj2g = GsmCommand()
            if(sectors[0]):
                get_s1 = obj2g.get(sectors[0])
                com.execute(get_s1)
                set_s1 = obj2g.set(sectors[0] , bande2g , 'ACTIVE')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 bande "+bande2g+" for 2G is now ACTIVE") 

            if(sectors[1]):
                get_s2 = obj2g.get(sectors[1])
                com.execute(get_s2)
                set_s2 = obj2g.set(sectors[1] , bande2g , 'ACTIVE')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 bande "+bande2g+" for 2G is now ACTIVE") 

            if(sectors[2]):
                get_s3 = obj2g.get(sectors[2])
                com.execute(get_s3)
                set_s3 = obj2g.set(sectors[2] , bande2g , 'ACTIVE')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 bande "+bande2g+" for 2G is now ACTIVE") 
            
            SlotSet("unblocked_sector_slot" , sector_to_unblock)
            return[]
            
        elif(('900' in bande3g) or ('2100' in bande3g)):
            manageCodeSiteSector(codeSite , bande3g ,sector_to_unblock)
            obj3g = g3rncCommand()
            if(sectors[0]):
                get_s1 = obj3g.get(sectors[0])
                com.execute(get_s1)
                set_s1 = obj3g.set(sectors[0] , bande3g , 'UNBLOCKED')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 bande "+bande3g+" for 3G is now UNBLOCKED") 

            if(sectors[1]):
                get_s2 = obj3g.get(sectors[1])
                com.execute(get_s2)
                set_s2 = obj3g.set(sectors[1] , bande3g , 'UNBLOCKED')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 bande "+bande3g+" for 3G is now UNBLOCKED") 

            if(sectors[2]):
                get_s3 = obj3g.get(sectors[2])
                com.execute(get_s3)
                set_s3 = obj3g.set(sectors[2] , bande3g , 'UNBLOCKED')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 bande "+bande3g+" for 2G is now UNBLOCKED") 

            SlotSet("unblocked_sector_slot" , sector_to_unblock)
            return[]


        elif(('1800' in bande4g) or ('2100' in bande4g)):
            manageCodeSiteSector(codeSite , bande4g ,sector_to_unblock)
            obj4gFDD = g4FDDCommand()
            if(sectors[0]):
                get_s1 = obj4gFDD.get(sectors[0])
                com.execute(get_s1)
                set_s1 = obj4gFDD.set(sectors[0] , bande4g , 'UNBLOCKED')
                com.execute(set_s1)
                dispatcher.utter_message(text="Sector S1 bande "+bande4g+" for 4G is now UNBLOCKED") 

            if(sectors[1]):
                get_s2 = obj4gFDD.get(sectors[1])
                com.execute(get_s2)
                set_s2 = obj4gFDD.set(sectors[1] , bande4g , 'UNBLOCKED')
                com.execute(set_s2)
                dispatcher.utter_message(text="Sector S2 bande "+bande4g+" for 4G is now UNBLOCKED") 

            if(sectors[2]):
                get_s3 = obj4gFDD.get(sectors[2])
                com.execute(get_s3)
                set_s3 = obj4gFDD.set(sectors[2] , bande4g , 'UNBLOCKED')
                com.execute(set_s3)
                dispatcher.utter_message(text="Sector S3 bande "+bande4g+" for 4G is now UNBLOCKED") 
           
            SlotSet("undeblocked_sector_slot" , sector_to_unblock)   
            return[]

        else: 
            dispatcher.utter_message(text= "Sorry but i didn't recognize the band for the sector you want to Unlock")
            return[]

