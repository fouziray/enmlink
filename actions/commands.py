from abc import abstractmethod
import pandas as pd
from enmscripting import enmscripting        # module privé propre au système enm 
import json
from os.path import exists


path =  ".store_rollback/"

# this is a first draft of enm access and not yet integrated with actions server
class Command(object):
    

    def __init__(self):
        #self.session=None
        pass

   

    def open(self, a, b, c):
        self.session = enmscripting.open(a, b, c)
        return self.session
        print("opened")
        pass
    def closesession(self):
        enmscripting.close(self.session)
        print("closed")
        pass
    def execute(self,command):
         if(self.session):
           cmd=self.session.command()
           cmd.execute(str(command))
         else: 
           print("command is not executed")
         print("this is executed command"+str(command))
    
         return command



def format(l, tech):
    i = [row for row in range(len(l)) if 'SubNetwork' in l[row]]
    if '0 inst' not in l[-1]:
        if tech == '2G':
            l_core = l[i[1] + 2:-1]
            columns = l[i[1] + 1].split('\t')
        else:
            l_core = l[2:-1]
            columns = l[1].split('\t')
        l_core_2 = [l_core[row].split('\t') for row in range(len(l_core)) if l_core[row] != '']
        data = pd.DataFrame(l_core_2, columns=columns)
    else: 
        data=pd.DataFrame()
    return data


def manageCodeSite(codeSite):     # permet de connaitre la technologie a tester dans le site 2G , 3G , 4G
        print("code site is c"+str(codeSite))
        site4g=None
        site3g=None
        site4gTDD=None
        site2g=None
        if ((codeSite[-1] == 'l') or (codeSite[-1] == 'L')): 
            site4g = codeSite
      
        elif((codeSite[-1] == 'u') or (codeSite[-1] == 'U')): 
            site3g = codeSite 
 
        elif((codeSite[-1] == 't') or (codeSite[-1] == 'T')): 
            site4gTDD = codeSite
        else:
            site2g = codeSite
        #print("list out of managed code site"+str([site2g , site3g , site4g , site4gTDD]))
        return[site2g , site3g , site4g , site4gTDD]

def manageCodeSiteSector(codeSite , bande , sector):
        #print("parametres"+str(codeSite)+" "+str(bande)+" "+str(sector))
        sector1_2g_b1=None
        sector2_2g_b1=None
        sector3_2g_b1=None
        sector1_2g_b2=None
        sector2_2g_b2=None
        sector3_2g_b2=None
        sector1_4g_b1=None
        sector2_4g_b1=None
        sector3_4g_b1=None
        sector1_4g_b2=None
        sector2_4g_b2=None
        sector3_4g_b2=None
        sector1_3g_b1=None
        sector2_3g_b1=None
        sector3_3g_b1=None
        sector1_3g_b2=None
        sector2_3g_b2=None
        sector3_3g_b2=None
        sites = manageCodeSite(codeSite)
        #print("list inside sectors manage"+str(sites))
        site2g = sites[0]
        site3g = sites[1]
        site4gFDD = sites[2]
        site4gTDD = sites[3]
        sector="\t".join(sector)
        #print("sector"+str(sector))
        # 1 cas site 2G
        if(site2g):
            if ('900' in bande):
                if('1' in sector): 
                    sector1_2g_b1 = site2g + 'A'
                if('2' in sector):
                    sector2_2g_b1 = site2g + 'B'
                if('3' in sector):
                    sector3_2g_b1 = site2g + 'C'
            if ('1800' in bande):
                if('1' in sector): 
                    sector1_2g_b2 = site2g + 'D'
                if('2' in sector):
                    sector2_2g_b2 = site2g + 'E'
                if('3' in sector):
                    sector3_2g_b2 = site2g + 'F'
            #print("hfhef"+str([sector1_2g_b1 , sector2_2g_b1 , sector3_2g_b1 , sector1_2g_b2 , sector2_2g_b2 , sector3_2g_b2]))
            return[sector1_2g_b1 , sector2_2g_b1 , sector3_2g_b1 , sector1_2g_b2 , sector2_2g_b2 , sector3_2g_b2]

        # 2eme cas technologie 3G
        if(site3g):
            if ('900' in bande):
                if('1' in sector): 
                    sector1_3g_b1 = site3g      # 1st sector end with 'U' by default
                if('2' in sector):
                    sector2_3g_b1 = 'V'.join(site3g.rsplit(site3g[-1:], 1)) #site3g - 'U' + 'V'
                if('3' in sector):
                    sector3_3g_b1 = 'W'.join(site3g.rsplit(site3g[-1:], 1)) #site3g - 'U' + 'W'
            if ('2100' in bande):
                if('1' in sector): 
                    sector1_3g_b2 = 'X'.join(site3g.rsplit(site3g[-1:], 1)) #site3g - 'U' + 'X'
                if('2' in sector):
                    sector2_3g_b2 = 'Y'.join(site3g.rsplit(site3g[-1:], 1))#site3g - 'U' + 'Y'
                if('3' in sector):
                    sector3_3g_b2 = 'Z'.join(site3g.rsplit(site3g[-1:], 1))#site3g - 'U' + 'Z'
            #print("hehehe"+str([sector1_3g_b1 , sector2_3g_b1 , sector3_3g_b1 , sector1_3g_b2 , sector2_3g_b2 , sector3_3g_b2]))
            return[sector1_3g_b1 , sector2_3g_b1 , sector3_3g_b1 , sector1_3g_b2 , sector2_3g_b2 , sector3_3g_b2]


        if(site4gFDD):
            if ('1800' in bande):
                if('1' in sector): 
                    sector1_4g_b1 = 'M'.join(site4gFDD.rsplit(site4gFDD[-1:], 1)) 
                if('2' in sector):
                    sector2_4g_b1 = 'N'.join(site4gFDD.rsplit(site4gFDD[-1:], 1)) 
                if('3' in sector):
                    sector3_4g_b1 = 'O'.join(site4gFDD.rsplit(site4gFDD[-1:], 1)) 
            if ('2100' in bande):
                if('1' in sector): 
                    sector1_4g_b2 = 'R'.join(site4gFDD.rsplit(site4gFDD[-1:], 1)) 
                if('2' in sector):
                    sector2_4g_b2 = 'S'.join(site4gFDD.rsplit(site4gFDD[-1:], 1))  
                if('3' in sector):
                    sector3_4g_b2 = 'T'.join(site4gFDD.rsplit(site4gFDD[-1:], 1)) 
            #print("hehee4gfdd"+str([sector1_4g_b1 , sector2_4g_b1 , sector3_4g_b1 , sector1_4g_b2 , sector2_4g_b2 , sector3_4g_b2]))
            return[sector1_4g_b1 , sector2_4g_b1 , sector3_4g_b1 , sector1_4g_b2 , sector2_4g_b2 , sector3_4g_b2]
        #print("manageCodeSiteSector"+str(sites))
        return []


       


def check_2g(site2g):
    g2_obj = GsmCommand()
    get_state_2G = g2_obj.get(site2g , 'G900 , G1800')
    output2g = g2_obj.execute(get_state_2G)
    # this is a sample output from enm
    output2g=['SubNetwork,SubNetwork,MeContext,ManagedElement,BscFunction,BscM,GeranCellM,GeranCell', 'NodeId\tBscFunctionId\tBscMId\tGeranCellMId\tGeranCellId\tcSysType\tgeranCellId', 'BLDEVO2\t1\t1\t1\t09620D\tGSM1800\t09620D', 'BLDEVO2\t1\t1\t1\t09620E\tGSM1800\t09620E', 'BLDEVO2\t1\t1\t1\t09620F\tGSM1800\t09620F', 'SubNetwork,SubNetwork,MeContext,ManagedElement,BscFunction,BscM,GeranCellM,GeranCell,ChannelGroup', 'NodeId\tBscFunctionId\tBscMId\tGeranCellMId\tGeranCellId\tChannelGroupId\tconnectedG12Tg\tconnectedG31Tg\tstate', 'BLDEVO2\t1\t1\t1\t09620D\t0\tnull\tSubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1020\tACTIVE', 'BLDEVO2\t1\t1\t1\t09620E\t0\tnull\tSubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1120\tACTIVE', 'BLDEVO2\t1\t1\t1\t09620F\t0\tnull\tSubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1220\tACTIVE', '', '6 instance(s)']
    #output2g= ['', '0 instance(s)']

    table2g = format(output2g , '2G')
    #response2g = "Status 2g\n" +' '.join((table2g[['GeranCellId','state']]).to_string(header=False , index = False).split('\n'))


    return table2g



def check_3g(site3g):
    g3_obj = g3rncCommand()
    get_state_3G = g3_obj.get(site3g , 'U900')
    output3g = g3_obj.execute(get_state_3G)
    #get_state_3G = g3_obj.get(site3g , 'U2100')
    #output3g = g3_obj.execute(get_state_3G)
    output3g=['SubNetwork,SubNetwork,SubNetwork,MeContext,ManagedElement,RncFunction,UtranCell', 'NodeId\tRncFunctionId\tUtranCellId\tadministrativeState\toperationalState\tuarfcnDl', 'RNCSTF\t1\t193020V\tUNLOCKED\tENABLED\t10563', 'RNCSTF\t1\t193020W\tUNLOCKED\tENABLED\t10563', 'RNCSTF\t1\t193020X\tUNLOCKED\tENABLED\t10588', 'RNCSTF\t1\t193020Y\tUNLOCKED\tENABLED\t10588', 'RNCSTF\t1\t193020U\tUNLOCKED\tENABLED\t10563', 'RNCSTF\t1\t193020Z\tUNLOCKED\tENABLED\t10588', '', '6 instance(s)']
    #output3g= ['', '0 instance(s)']

    table3g = format(output3g , '3G')
    #response3g = "\nStatus 3g\n" +' '.join((table3g[['UtranCellId','administrativeState']]).to_string(header=False , index = False).split('\n'))
    

    
    return table3g                    


def check_4gFDD(site4g):
    g4_obj = g4FDDCommand()
    get_state_4GFDD = g4_obj.get(site4g, '1')

    output4g =g4_obj.execute(get_state_4GFDD)
    output4g= ['SubNetwork,SubNetwork,SubNetwork,MeContext,ManagedElement,ENodeBFunction,EUtranCellFDD', 'NodeId\tENodeBFunctionId\tEUtranCellFDDId\tadministrativeState\tavailabilityStatus\tfreqBand\toperationalState', '351012L\t1\t351012T\tUNLOCKED\tnull\t1\tENABLED', '351012L\t1\t351012R\tUNLOCKED\tnull\t1\tENABLED', '351012L\t1\t351012S\tUNLOCKED\t[FAILED]\t1\tDISABLED', '', '3 instance(s)']

    table4g = format(output4g , '4G')
    
    #response4g = "\nStatus 4g FDD\n" +' '.join((table4g[['EUtranCellFDDId','administrativeState']]).to_string(header=False , index = False).split('\n'))
    
    return table4g

def check_4gTDD(site4gTDD):
    g4TDD_obj = g4TDDCommand()
    get_state_4GTDD = g4TDD_obj.get(site4gTDD)

    output4g_TDD =g4TDD_obj.execute(get_state_4GTDD)
    
    table4gTDD = format(output4g_TDD , '4G')
    response4gTDD = "\nStatus 4g TDD\n" + ' '.join((table4gTDD[['EUtranCellFDDId','administrativeState']]).to_string(header=False , index = False).split('\n'))
   

    return response4gTDD


def check_tilt(codeSite):
    tilt_com = RetCommand()
    get_tilt_values = tilt_com.get_tilt(codeSite) 
    outputTilt = tilt_com.execute(get_tilt_values)
    # here we put a fake object for mocking an enm response 
    output5=['SubNetwork,SubNetwork,SubNetwork,MeContext,ManagedElement,Equipment,AntennaUnitGroup,AntennaNearUnit,RetSubUnit', 'NodeId\tEquipmentId\tAntennaUnitGroupId\tAntennaNearUnitId\tRetSubUnitId\telectricalAntennaTilt\tuserLabel', '09620L\t1\t3\t7\t1\t55\tY6_LTE4X4_U2100_G1800', '09620L\t1\t3\t1\t1\t80\tR1_G900_U900', '09620L\t1\t3\t2\t1\t55\tY1_UNUSED', '09620L\t1\t3\t3\t1\t55\tY2_LTE4X4_U2100_G1800', '09620L\t1\t3\t4\t1\t60\tY3_TDD4X4', '09620L\t1\t3\t5\t1\t60\tY4_TDD4X4', '09620L\t1\t3\t6\t1\t55\tY5_UNUSED', '09620L\t1\t1\t1\t1\t70\tR1_G900_U900', '09620L\t1\t1\t2\t1\t70\tY1_UNUSED', '09620L\t1\t1\t3\t1\t70\tY2_LTE4X4_U2100_G1800', '09620L\t1\t1\t4\t1\t70\tY3_TDD4X4', '09620L\t1\t1\t5\t1\t70\tY4_TDD4X4', '09620L\t1\t1\t6\t1\t70\tY5_UNUSED', '09620L\t1\t1\t7\t1\t70\tY6_LTE4X4_U2100_G1800', '09620L\t1\t2\t1\t1\t70\tR1_G900_U900', '09620L\t1\t2\t2\t1\t75\tY1_UNUSED', '09620L\t1\t2\t3\t1\t75\tY2_LTE4X4_U2100_G1800', '09620L\t1\t2\t4\t1\t75\tY3_TDD4X4', '09620L\t1\t2\t5\t1\t75\tY4_TDD4X4', '09620L\t1\t2\t6\t1\t75\tY5_UNUSED', '09620L\t1\t2\t7\t1\t75\tY6_LTE4X4_U2100_G1800', '', '21 instance(s)']
    tableTilt = format(output5, 'tilt')
    responseTilt = "\nStatus tilt\n" + ' '.join((tableTilt[['electricalAntennaTilt', 'userLabel']]).to_string(header=False , index = False).split('\n'))
   
    return tableTilt



def buildCodeSite(codeSite) :
        if ((codeSite[-1] == 'l') or (codeSite[-1] == 'L')): 
            site2g = codeSite - codeSite[-1]
            site3g = codeSite - codeSite[-1] + 'U'
            site4g = codeSite
            site4gTDD = codeSite + 'T'
      
        elif((codeSite[-1] == 'u') or (codeSite[-1] == 'U')): 
            site2g = codeSite - codeSite[-1]
            site3g = codeSite 
            site4g = codeSite - codeSite[-1] + 'L'
            site4gTDD = codeSite - codeSite[-1] + 'T'
        elif((codeSite[-1] == 't') or (codeSite[-1] == 'T')): 
            site2g = codeSite - codeSite[-2]
            site3g = codeSite - codeSite[-2] + 'U'
            site4g = codeSite - codeSite[-1]
            site4gTDD = codeSite
        else:
            site2g = codeSite
            site3g = codeSite + 'U'
            site4g = codeSite + 'L'  
            site4gTDD = codeSite + 'LT'
        return[site2g , site3g , site4g , site4gTDD]

class GsmCommand(Command):

    def get(self, siteId, bande):
        if "900" in bande   or "1800" in bande:
            cmd = "cmedit get * Gerancell.(GeranCellId==" + str(siteId) + "*,cSysType=='" + str(
                bande) + "'),ChannelGroup.(connectedG12Tg,connectedG31Tg,state) -t"
            return cmd
        else:
            return 'Error'

    def set(self, siteId, bande, state):
        if bande!='0':
            cmd = "cmedit set * GeranCell.(GeranCellId==" + str(siteId) + "*,cSysType=='" + str(bande) + "'),ChannelGroup state=" + state
        else:
            cmd = "cmedit set * GeranCell.GeranCellId==" + str(siteId) + ",ChannelGroup state=" + state

        return cmd

    def rollback_2g(self, path2g):
        f = open(path2g)
        g2_data_json = json.load(f)
        f_l = []
        for row in g2_data_json:
            command = self.set(row['GeranCellId'], row['BscFunctionId'] , row['state'])
            f_l.append(command)
        return f_l


class g3rncCommand(Command):
    def get(self, siteId, band):
        cmd=None
        if band == 'U900':
            cmd = "cmedit get * UtranCell.(UtranCellId==" + str(
                siteId) + "*,administrativeState,operationalState,uarfcnDl==3070) -t"
        elif(band == 'U2100'):
            cmd = "cmedit get * UtranCell.(UtranCellId==" + str(
                siteId) + "*,administrativeState,operationalState,uarfcnDl!=3070) -t"
        return cmd

    def set(self, siteId, band, state, file=None):
        if band == 'U900':
            cmd = "cmedit set * UtranCell.(UtranCellId==" + str(
                siteId) + "*,uarfcnDl==3070) administrativeState=" + str(state)
        elif band == 'U2100':
            cmd = "cmedit set * UtranCell.(UtranCellId==" + str(
                siteId) + "*,uarfcnDl!=3070) administrativeState=" + str(state) 
       # if (file != None):
       #     listcmd = []
       #     f1 = open(file)
       #     g3_data_json = json.load(f1)
       #     for row in g3_data_json:
       #         cmd = "cmedit set * UtranCell.(UtranCellId==" + row['UtranCellId'] + "*,uarfcnDl!=3070) administrativeState=" + row['administrativeState']
       #         listcmd.append(cmd)
       #     return listcmd
        return cmd
    

    def rollback_3g(self, path3g):
        f = open(path3g)
        g3_data_json = json.load(f)
        listcmd = []
        for row in g3_data_json:
            band="U900"
            if (row['uarfcnDl'] != "3070"):
                band="U2100"
            command = self.set(row['UtranCellId'],band,row['administrativeState'])
            listcmd.append(command)
        return listcmd
            #print(command)
      
            





    def Check_set_cmnd(set_result):
        if (set_result[-1] != '0 instance(s) updated'):
            return True
        else:
            return False


class g3NodeCommand(Command):
    def get(self, siteId, uarfcnId, bande):
        cmd = "cmedit get " + str(siteId) + " Nodeblocalcell.operatingband==1;Rbslocalcell.operatingband==1 -t"
        return cmd

    def set(self, siteId, uarfcn, bande, state):
        cmd = "cmedit set " + str(siteId) + " Nodeblocalcell.operatingband==8;Rbslocalcell.operatingband==8 administrativeState=" + str(state)
        return cmd


class g4FDDCommand(Command):
    def get(self, siteId, bande):
        cmd = "cmedit get " + str(siteId) + " EutranCellFDD.(freqBand==" + str(bande) + ",administrativeState,operationalState, availabilityStatus) -t"
        return cmd

    def set(self, siteId, bande, state):
        if bande!=0:
            cmd = "cmedit set " + str(siteId) + " EutranCellFDD.(freqBand==" + str(bande) + ") administrativeState=" + str(state)
        else:
            cmd = "cmedit set * EutranCellFDD.(EutranCellFDDId=="+ str(siteId) +") administrativeState=" + str(state)
        return cmd

    def rollback_4g(self, path4g):
        f = open(path4g)
        g4_data_json = json.load(f)
        f1_l = []
        for row in g4_data_json:
            command = self.set(row['EUtranCellFDDId'], row['freqBand'], row['administrativeState'])
            f1_l.append(command)
        return f1_l

class g4TDDCommand(Command):
    def get(self, siteId):
        cmd = "cmedit get " + siteId + " EutranCellTDD.(administrativeState,operationalState, availabilityStatus) -t"
        return cmd

    def set(self, siteId, state):
        cmd = "cmedit set " + siteId + " EutranCellTDD administrativeState=" + state
        return cmd


class RetCommand(Command):

    def get_tilt(self, siteId):
        siteIdd = siteId.split(", ")  # dans une liste
        sites_codes = ';'.join(siteIdd)
        cmd1 = "cmedit get " + sites_codes + " Retsubunit.(userlabel , electricalAntennaTilt);RetDevice.(userlabel ,electricalAntennaTilt) -t"
        return cmd1

    def set_tilt(self, siteId, tilt):

        siteIdd = siteId.split(", ")  # dans une liste
        sites_codes = ';'.join(siteIdd)
        if ((tilt == 0) or (tilt == 100)):
            cmd1 = "cmedit set " + sites_codes + " Retsubunit;RetDevice electricalAntennaTilt=" + str(tilt)
            return cmd1
        else:
            return 0

    def getGroup_tilt(self, siteId, userlabel, grpid):
        siteIdd = siteId.split(", ")  # dans une liste

        sites_codes = ','.join(siteIdd)
        # cmd = "cmedit get " + sites_codes + ("AntennaUnitGroup.AntennaUnitGroupId=="+grpid+",AntennaNearUnit,Retsubunit.("+userlabel+",electricalAntennaTilt) ") or ("RetDevice.("+userlabel+",electricalAntennaTilt) ") "-t"
        cmd1 = "cmedit get " + sites_codes + "AntennaUnitGroup.AntennaUnitGroupId==" + grpid + ",AntennaNearUnit,Retsubunit.(" + userlabel + ",electricalAntennaTilt) -t"
        cmd2 = "cmedit get " + sites_codes + "RetDevice.(" + userlabel + ",electricalAntennaTilt) -t"
        return cmd1 or cmd2

    def tiltCOmmand(self, nodeid, AntennaUnitGroupId, AntennaNearUnitId, RetSubUnitId, electricalAntennaTilt):
        commandSetTilt = 'cmedit set ' + nodeid + ' AntennaUnitGroup.AntennaUnitGroupId==' + AntennaUnitGroupId + ',AntennaNearUnit.AntennaNearUnitId==' + AntennaNearUnitId + ',RetSubUnit.RetSubUnitId==' + RetSubUnitId + '   electricalAntennaTilt=' + electricalAntennaTilt
        return commandSetTilt

    def rollback_tilt(self, path):
        if( exists(path)):
            f = open(path)
            f1 = []
            tilt_data_json = json.load(f)
            for row in tilt_data_json:
                command = self.tiltCOmmand(row['NodeId'], row['AntennaUnitGroupId'], row['AntennaNearUnitId'],
                                        row['RetSubUnitId'], row['electricalAntennaTilt'])
                f1.append(command)
                #print(command)
            return f1
        else:
            return None


class OptimCommand(Command):

    def get_opt(self, siteId):
        cmd = "cmedit get " + str(siteId) + " EUtranCellFDD.pZeroNominalPucch, pZeroNominalPusch, noOfPucchSrUsers) -t"
        return cmd

    def set_opt(self, siteId, param1, param2, param3):
        cmd=[]
        cmd.append( "cmedit set " + str(siteId) + " EUtranCellFDD pZeroNominalPucch= " + param1 )
        cmd.append("cmedit set EUtranCellFDD pZeroNominalPusch= " + param2) 
        cmd.append("cmedit set EUtranCellFDD noOfPucchSrUsers= " + param3)
        return cmd

    def get_Feature_State(self, siteId, Feature_state_id):
        Feature_state_id="CXC4011955"
        cmd = "cmedit get " + str(
            siteId) + " FeatureState.(FeatureStateID==" + Feature_state_id + ",LicenceState,FeatureState) -t"
        return cmd

    def set_Feature_State(self, siteId, Feature_state_id):
        Feature_state_id="CXC4011955"
        cmd = "cmedit set " + str(
            siteId) + " FeatureState.FeatureStateID==" + Feature_state_id + "  FeatureState=ACTIVE"
        return cmd
    
    def ping_issue(self):
        return 'Deactivate CXC4010912'

    def format(l,tech):
        i = [row for row in range(len(l)) if 'SubNetwork' in l[row]]
        if '0 inst' not in l[-1]:
            if tech=='2G':
                l_core = l[i[1]+2:-1]
                columns = l[i[1]+1].split('\t')
            else:
                l_core = l[2:-1]
                columns = l[1].split('\t')
                l_core_2= [l_core[row].split('\t') for row in range(len(l_core)) if l_core[row]!='']
                data = pd.DataFrame(l_core_2,columns=columns)
        else:
            data = tech+" technology doens't exists for this site"
        return (data)


