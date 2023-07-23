from abc import abstractmethod
#import pandas as pd
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
     
    def get_tilt(self , siteId, userlabel):
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
            return (cmd1 or cmd2)
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


if __name__ == '__main__':

  """  ### 2G TEST ###
    com=Command()
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