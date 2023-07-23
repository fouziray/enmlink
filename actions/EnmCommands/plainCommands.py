#!/usr/bin/env python
import pika, sys, os
from abc import abstractmethod
import pandas as pd
#from .enmscripting import enmscripting

#this is a first draft of enm access and not yet integrated with actions server
class Command:
    def __init__(self):
        pass

    @abstractmethod
    def get(siteId, uarfcnId, bande):
        pass

    @abstractmethod
    def set(siteId, uarfcn, bande):
        pass
    def format2g(self):
        output4=['SubNetwork,SubNetwork,MeContext,ManagedElement,BscFunction,BscM,GeranCellM,GeranCell', 'NodeId\tBscFunctionId\tBscMId\tGeranCellMId\tGeranCellId\tcSysType\tgeranCellId', 'BLDEVO2\t1\t1\t1\t09620D\tGSM1800\t09620D', 'BLDEVO2\t1\t1\t1\t09620E\tGSM1800\t09620E', 'BLDEVO2\t1\t1\t1\t09620F\tGSM1800\t09620F', 'SubNetwork,SubNetwork,MeContext,ManagedElement,BscFunction,BscM,GeranCellM,GeranCell,ChannelGroup', 'NodeId\tBscFunctionId\tBscMId\tGeranCellMId\tGeranCellId\tChannelGroupId\tconnectedG12Tg\tconnectedG31Tg\tstate', 'BLDEVO2\t1\t1\t1\t09620D\t0\tnull\tSubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1020\tACTIVE', 'BLDEVO2\t1\t1\t1\t09620E\t0\tnull\tSubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1120\tACTIVE', 'BLDEVO2\t1\t1\t1\t09620F\t0\tnull\tSubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1220\tACTIVE', '', '6 instance(s)']
        output3= ['', '0 instance(s)']
        output2=['SubNetwork,SubNetwork,SubNetwork,MeContext,ManagedElement,RncFunction,UtranCell', 'NodeId\tRncFunctionId\tUtranCellId\tadministrativeState\toperationalState\tuarfcnDl', 'RNCSTF\t1\t193020V\tUNLOCKED\tENABLED\t10563', 'RNCSTF\t1\t193020W\tUNLOCKED\tENABLED\t10563', 'RNCSTF\t1\t193020X\tUNLOCKED\tENABLED\t10588', 'RNCSTF\t1\t193020Y\tUNLOCKED\tENABLED\t10588', 'RNCSTF\t1\t193020U\tUNLOCKED\tENABLED\t10563', 'RNCSTF\t1\t193020Z\tUNLOCKED\tENABLED\t10588', '', '6 instance(s)']
        output5=['SubNetwork,SubNetwork,SubNetwork,MeContext,ManagedElement,ENodeBFunction,EUtranCellFDD', 'NodeId\tENodeBFunctionId\tEUtranCellFDDId\tadministrativeState\tavailabilityStatus\tfreqBand\toperationalState', '351012L\t1\t351012T\tUNLOCKED\tnull\t1\tENABLED', '351012L\t1\t351012R\tUNLOCKED\tnull\t1\tENABLED', '351012L\t1\t351012S\tUNLOCKED\t[FAILED]\t1\tDISABLED', '', '3 instance(s)']
        output=['SubNetwork,SubNetwork,SubNetwork,MeContext,ManagedElement,ENodeBFunction,EUtranCellTDD', 'NodeId\tENodeBFunctionId\tEUtranCellTDDId\tadministrativeState\tavailabilityStatus\toperationalState', '16601LT\t1\tL23_16601U\tUNLOCKED\tnull\tENABLED', '16601LT\t1\tL23_16601V\tUNLOCKED\tnull\tENABLED', '16601LT\t1\tL23_16601W\tUNLOCKED\tnull\tENABLED', '16601LT\t1\tL23_16601X\tUNLOCKED\tnull\tENABLED', '16601LT\t1\tL23_16601Y\tUNLOCKED\tnull\tENABLED', '16601LT\t1\tL23_16601Z\tUNLOCKED\tnull\tENABLED', '', '6 instance(s)']
        if (output[-1]!='0 instance(s)'):
            output.pop(0)
            columns_names=output[0].split('\t')
            output.pop(0)
            values_data=[ values.split('\t') for values in output ]
            final=[ valuee for valuee in values_data if ('UNLOCKED' or 'LOCKED' or 'ACTIVE') in valuee]
            values_data.insert(0,columns_names)
        else: 
            columns_names=[]
            values_data=[]
        return values_data
    def formatg(self):
        l=['SubNetwork,SubNetwork,MeContext,ManagedElement,BscFunction,BscM,GeranCellM,GeranCell', 'NodeId\tBscFunctionId\tBscMId\tGeranCellMId\tGeranCellId\tcSysType\tgeranCellId', 'BLDEVO2\t1\t1\t1\t09620D\tGSM1800\t09620D', 'BLDEVO2\t1\t1\t1\t09620E\tGSM1800\t09620E', 'BLDEVO2\t1\t1\t1\t09620F\tGSM1800\t09620F', 'SubNetwork,SubNetwork,MeContext,ManagedElement,BscFunction,BscM,GeranCellM,GeranCell,ChannelGroup', 'NodeId\tBscFunctionId\tBscMId\tGeranCellMId\tGeranCellId\tChannelGroupId\tconnectedG12Tg\tconnectedG31Tg\tstate', 'BLDEVO2\t1\t1\t1\t09620D\t0\tnull\tSubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1020\tACTIVE', 'BLDEVO2\t1\t1\t1\t09620E\t0\tnull\tSubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1120\tACTIVE', 'BLDEVO2\t1\t1\t1\t09620F\t0\tnull\tSubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1220\tACTIVE', '', '6 instance(s)']
        i = [row for row in range(len(l)) if 'SubNetwork' in l[row]]
        if '0 inst' not in l[-1]:
            print(i)
            l_core = l[i[1]+2:-1]
            l_core_2= [l_core[row].split('\t') for row in range(len(l_core)) if l_core[row]!='']
            columns = l[i[1]+1].split('\t')
            data = pd.DataFrame(l_core_2,columns=columns)
            print(data)
    
        
    def open(self, a, b, c):
      #  self.session = enmscripting.open(a, b, c)
      #  return self.session
        return True
    def closesession(self):
        #enmscripting.close(self.session)
        pass
    def execute(self, cmd):
        #cmdd = self.session.terminal()
        #return cmdd.execute(cmd).get_output()
        pass

class GsmCommand(Command):

    def get(self, siteId, uarfcnId, bande):
        if bande == "GSM900" or bande == "GSM1800":
            cmd = "cmedit get * Gerancell.GeranCellId==" + str(siteId) + "*,ChannelGroup.(band=='" + str(
                bande) + "',connectedG12Tg,connectedG31Tg,state) -t"
            return cmd
        else:
            return 'Error'

    def set(self, siteId, uarfcn, bande, state):
        cmd = "cmedit set * Gerancell.GeranCellId==" + str(siteId) + "*,ChannelGroup.(band=='" + str(
            bande) + "') state=" + state
        return cmd


class g3rncCommand(Command):
    def get(self, siteId, band):
        if band == 8:
            cmd = "cmedit get * UtranCell.(UtranCellId==" + str(
                siteId) + "*,administrativeState,operationalState,uarfcnDl==3070) -t"
        else:
            cmd = "cmedit get * UtranCell.(UtranCellId==" + str(
                siteId) + "*,administrativeState,operationalState,uarfcnDl!=3070) -t"
        return cmd

    def set(self, siteId, band, state):
        if band == 8:
            cmd = "cmedit set * UtranCell.(UtranCellId==" + str(
                siteId) + "*,uarfcnDl==3070) administrativeState=" + state
        else:
            cmd = "cmedit set * UtranCell.(UtranCellId==" + str(
                siteId) + "*,uarfcnDl!=3070) administrativeState=" + state
        return cmd


class g3NodeCommand(Command):
    def get(self, siteId, uarfcnId, bande):
        cmd = "cmedit get " + siteId + " Nodeblocalcell.operatingband==1;Rbslocalcell.operatingband==1 -t"
        return cmd

    def set(self, siteId, uarfcn, bande, state):
        cmd = "cmedit set " + siteId + " Nodeblocalcell.operatingband==8;Rbslocalcell.operatingband==8 administrativeState=" + state
        return cmd


class g4FDDCommand(Command):
    def get(self, siteId, bande):
        cmd = "cmedit get " + siteId + " EutranCellFDD.(freqBand=="+bande+",administrativeState,operationalState, availabilityStatus) -t"
        return cmd

    def set(self, siteId, bande, state):
        cmd = "cmedit set " + siteId + " EutranCellFDD.(freqBand=="+bande+") administrativeState=" + state
        return cmd


class g4TDDCommand(Command):
    def get(self, siteId):
        cmd = "cmedit get " + siteId + " EutranCellTDD.(administrativeState,operationalState, availabilityStatus) -t"
        return cmd

    def set(self, siteId, state):
        cmd = "cmedit set " + siteId + " EutranCellTDD administrativeState=" + state
        return cmd
class RetCommand(Command):
     
    def get_tilt(self , siteId):
        siteIdd = siteId.split(", ")  #  dans une liste 
        sites_codes = ','.join(siteIdd)
        # cmd1 = "cmedit get " + sites_codes + (" Retsubunit.(" +userlabel+ ",electricalAntennaTilt) ") or ("RetDevice.(" +userlabel+ ",electricalAntennaTilt)") "-t"
        cmd1 = "cmedit get " + sites_codes +" Retsubunit.(" +userlabel+ ",electricalAntennaTilt) -t"
        cmd2 = "cmedit get " + sites_codes + "RetDevice.(" +userlabel+ ",electricalAntennaTilt) -t"
        return cmd1 or cmd2

    def set_tilt(self , siteId , userlabel , tilt): 


        siteIdd = siteId.split(", ")  #  dans une liste 
        sites_codes = ','.join(siteIdd)


        if((tilt == 0) or (tilt == 100)):
            #cmd1 = "cmedit set " + sites_codes + (" Retsubunit.(userlabel==" +userlabel+ ")") ("RetDevice.(userlabel==" +userlabel+ ",) ") "electricalAntennaTilt="+tilt
            cmd1 = "cmedit set " + sites_codes + " Retsubunit.(userlabel==" +userlabel+ ") electricalAntennaTilt="+tilt
            cmd2 = "cmedit set " + sites_codes + "RetDevice.(userlabel==" +userlabel+ ",) electricalAntennaTilt="+tilt
            return cmd
        else:
            return 0

    def getGroup_tilt(self , siteId , userlabel , grpid):
        siteIdd = siteId.split(", ")  #  dans une liste

        sites_codes = ','.join(siteIdd)
        #cmd = "cmedit get " + sites_codes + ("AntennaUnitGroup.AntennaUnitGroupId=="+grpid+",AntennaNearUnit,Retsubunit.("+userlabel+",electricalAntennaTilt) ") or ("RetDevice.("+userlabel+",electricalAntennaTilt) ") "-t"
        cmd1 = "cmedit get " + sites_codes + "AntennaUnitGroup.AntennaUnitGroupId=="+grpid+",AntennaNearUnit,Retsubunit.("+userlabel+",electricalAntennaTilt) -t"
        cmd2 = "cmedit get " + sites_codes + "RetDevice.("+userlabel+",electricalAntennaTilt) -t"
        return cmd1 or cmd2

class OptimCommand(Command):

    def get_opt(self , siteId ):
        cmd = "cmedit get "+ str(siteId) + " EUtranCellFDD.pZeroNominalPucch, pZeroNominalPusch, noOfPucchSrUsers) -t"
        return cmd

    def set_opt(self , siteId ,param1 , param2 , param3):
        cmd = "cmedit set "+ str(siteId) + " EUtranCellFDD pZeroNominalPucch= "+param1+ ";cmedit set EUtranCellFDD pZeroNominalPusch= "+param2+ ";cmedit set EUtranCellFDD noOfPucchSrUsers= "+param3 
        return cmd 

    def get_Feature_State(self , siteId, Feature_state_id):
        cmd = "cmedit get "+ str(siteId) + " FeatureState.(FeatureStateID=="+Feature_state_id+",LicenceState,FeatureState) -t"
        return cmd

    def set_Feature_State(self , siteId , Feature_state_id ):
        cmd = "cmedit set "+ str(siteId) + " FeatureState.FeatureStateID=="+Feature_state_id+"  FeatureState=ACTIVE" 
        return cmd 


c5 = OptimCommand()
   
get_state_opt = c5.get_opt("16222L")
print('Get State Optime')
print(get_state_opt)


set_state_opt = c5.set_opt("16222L","-50","-60", "0")
print('Set State Optime')
print(set_state_opt)

def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello',
                        auto_ack=True,
                        on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    connection.close()
if __name__ == '__main__':


 ### 2G TEST ###
    com=Command()
    print(com.format2g())
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    #com.formatg()
    """ 
    com.open('XXXX', 'xxxxxx', 'XXXXXXXXXX')



    c = GsmCommand()
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$')
    get_state_2G = c.get('09620', 1000, 'GSM1800')
    print('State 2G')
    print(get_state_2G)
    a = com.execute(get_state_2G)
    print('$$$$$$$',a,'$$$$$$$$')
    set_state_2G = c.set('09620', 1000, 'GSM1800', 'ACTIVE')
    b = com.execute(set_state_2G)
    print('$$$$$$$', b, '$$$$$$$$')
    print(set_state_2G)
    ### 3G TEST ###
    c2 = g3rncCommand()
    get_state_3G = c2.get('094110', 8)
    print('State 3G')
    print(get_state_3G)
    set_state_3G = c2.set('094110', 8, 'LOCKED')
    print(set_state_3G)
    ### 4G FDD ###
    c3 = g4FDDCommand()
    get_state_4GFDD = c3.get('094110', '1')
    print('State 4G FDD')
    print(get_state_4GFDD)
    set_state_4GFDD = c3.set('094110','1','LOCKED')
    print(set_state_4GFDD)

    ## Tilt or Ret test ##
    
    c4 = RetCommand()
    get_state_tilt = c4.get_tilt("09620L,094620")
    print('State tilt')
    print(get_state_tilt)

    get_tilt_state = c4.get_tilt("094110")
    print('State tilt')
    print(get_state_tilt)

    set_tilt_state = c1.set_tilt("094110")
    print(set_tilt_state)


    ## Optimisation test ##   """
    
"""
    set_state_opt = c5.set_opt("","","")
    print('Set State Optime')
    print(set_state_opt)

    get_Fstate_opt = c5.get_Feature_State("","")
    print('Get Feature State Optime')
    print(get_Fstate_opt)

    set_Fstate_opt = c5.set_Feature_State("" , "","")
    print('Set Feature State Optime')
    print(set_Fstate_opt)

"""