import pandas as pd
from requests import session
from sqlalchemy import null
import enmscripting
session=null
def open(session2):
    self.session = enmscripting.open('', '', '')
    return self.session
def close(session):
    enmscripting.close(session)


def commandBuilder(dataframe):
    for row in range(len(dataframe)):
        e = str(dataframe.loc[row, '2G CODE final']) + ';' + str(dataframe.loc[row, '2G CODE T final']) + ';' + str(
        dataframe.loc[row, '3G CODE  final']) + ';' + str(dataframe.loc[row, '4G CODE  final']) + ';' + str(
        dataframe.loc[row, 'U900CODE  final']) + ';' + str(dataframe.loc[row, 'U900CODE  final 2'])

    g900c = "cmedit get * Gerancell.GeranCellId==" + str(dataframe.loc[row, '2G CODE final']) + "*,ChannelGroup.(band=='GSM900',connectedG12Tg,connectedG31Tg,state) -t"
    g1800c = "cmedit get * Gerancell.GeranCellId==" + str(dataframe.loc[row, '2G CODE final']) + "*,ChannelGroup.(band=='GSM1800',connectedG12Tg,connectedG31Tg,state) -t"
    rncu900c = "cmedit get * UtranCell.(UtranCellId==" + str(dataframe.loc[row, '3G CODE  final']) + "*,administrativeState,operationalState,uarfcnDl==3070) -t"
    rncu2100c = "cmedit get * UtranCell.(UtranCellId==" + str(dataframe.loc[row, '3G CODE  final']) + "*,administrativeState,operationalState,uarfcnDl==10563);UtranCell.(UtranCellId==" + str(data.loc[row, '3G CODE  final']) + "*,administrativeState,operationalState,uarfcnDl==10588) -t"
    nodeu900 = "cmedit get " + e + " Nodeblocalcell.operatingband==8;Rbslocalcell.operatingband==8 -t"
    nodeu2100 = "cmedit get " + e + " Nodeblocalcell.operatingband==1;Rbslocalcell.operatingband==1 -t"
    nodeL2100 = "cmedit get " + e + " EutranCellFDD.(freqBand==1,administrativeState,operationalState, availabilityStatus) -t"
    nodeL1800 = "cmedit get " + e + " EutranCellFDD.(freqBand==3,administrativeState,operationalState, availabilityStatus) -t"
    listg = [g900c, g1800c, rncu900c, rncu2100c, nodeu900, nodeu2100, nodeL2100, nodeL1800]
 
def executeCommand(command):
    cmd = session.terminal()
    datag = []
    for row2 in range(len(command)):
        response1 = cmd.execute(command[row2])
        lines1 = str(response1.get_output())
        print('******')
        print(lines1)
        print('*********final******')
        datag.append(lines1)    
   

