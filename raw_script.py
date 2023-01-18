import enmscripting
from getpass import getpass
import ast
import pandas as pd
import win32com.client as win32
import os
import xlsxwriter
from datetime import datetime
import argparse
from collections import Counter
from functools import reduce
import string
import numpy as np

dict_conf = {}


def listToString(s, sn):
    str1 = ""
    for ele in s:
        str1 += str(ele) + sn
    return str1[:-1]


def lToS(s):
    str1 = ""
    for ele in s:
        str1 += str(ele) + ','
    return str1[:-1]




def split_list(value, test_list):
    size = len(test_list)
    idx_list = [idx + 1 for idx, val in
                enumerate(test_list) if val == value]

    res = [test_list[i: j] for i, j in
           zip([0] + idx_list, idx_list +
               ([size] if idx_list[-1] != size else []))]
    return res


def convert_str_to_list(x,
i):
    if i != -1:
        head = x[i].split('\t')
    else:
        head = []
    filee = []
    for r in range(i + 1, len(x)):
        filee.append(x[r].split('\t'))
    return head, filee


data = pd.read_excel('', converters={'2G CODE final': str, '3G CODE  final': str}, sheet_name='Sheet9')

print(data)

session = enmscripting.open('', '', '')
(data):
    e = str(data.loc[row, '2G CODE final']) + ';' + str(data.loc[row, '2G CODE T final']) + ';' + str(
        data.loc[row, '3G CODE  final']) + ';' + str(data.loc[row, '4G CODE  final']) + ';' + str(
        data.loc[row, 'U900CODE  final']) + ';' + str(data.loc[row, 'U900CODE  final 2'])
    g900c = "cmedit get * Gerancell.GeranCellId==" + str(
        data.loc[row, '2G CODE final']) + "*,ChannelGroup.(band=='GSM900',connectedG12Tg,connectedG31Tg,state) -t"
    g1800c = "cmedit get * Gerancell.GeranCellId==" + str(
        data.loc[row, '2G CODE final']) + "*,ChannelGroup.(band=='GSM1800',connectedG12Tg,connectedG31Tg,state) -t"
    rncu900c = "cmedit get * UtranCell.(UtranCellId==" + str(
        data.loc[row, '3G CODE  final']) + "*,administrativeState,operationalState,uarfcnDl==3070) -t"
    rncu2100c = "cmedit get * UtranCell.(UtranCellId==" + str(data.loc[
                                                                  row, '3G CODE  final']) + "*,administrativeState,operationalState,uarfcnDl==10563);UtranCell.(UtranCellId==" + str(
        data.loc[row, '3G CODE  final']) + "*,administrativeState,operationalState,uarfcnDl==10588) -t"
    nodeu900 = "cmedit get " + e + " Nodeblocalcell.operatingband==8;Rbslocalcell.operatingband==8 -t"
    nodeu2100 = "cmedit get " + e + " Nodeblocalcell.operatingband==1;Rbslocalcell.operatingband==1 -t"
    nodeL2100 = "cmedit get " + e + " EutranCellFDD.(freqBand==1,administrativeState,operationalState, availabilityStatus) -t"
    nodeL1800 = "cmedit get " + e + " EutranCellFDD.(freqBand==3,administrativeState,operationalState, availabilityStatus) -t"
    listg = [g900c, g1800c, rncu900c, rncu2100c, nodeu900, nodeu2100, nodeL2100, nodeL1800]
    datag = []
    cmd = session.terminal()
    for row2 in range(len(listg)):
        response1 = cmd.execute(listg[row2])
        lines1 = str(response1.get_output())
        print('******')
        print(lines1)
        print('*********final******')
        datag.append(lines1)
    ### 2G check
    #### G1800 ####
    s_g18 = '/'
    g18 = ast.literal_eval(str(datag[1]))
    if '0 inst' not in g18[-1]:
        c1 = get_indexo(g18)
        g18 = g18[c1[0] + 1:c1[-1]]
        h18_al, d18_al = convert_str_to_list(g18, 0)
        df_g18 = pd.DataFrame(d18_al, columns=h18_al)
        df_g18['site'] = [df_g18.loc[i, 'GeranCellId'][:-1] for i in range(len(df_g18))]
        df_g18 = df_g18[df_g18['site'] == str(data.loc[row, '2G CODE final'])]
        df_g188 = df_g18[(df_g18['connectedG31Tg'] != 'null') | (df_g18['connectedG12Tg'] != 'null')]
        if len(df_g18) != 0:
            if len(df_g188) != 0:
                s_g18 = lToS(list(df_g18['state'].unique()))
            else:
                s_g18 = 'Not integrated but cell defined and ' + lToS(list(df_g18['state'].unique()))
        else:
            s_g18 = '/'
    print(s_g18)
    #### G900 ####
    s_g90 = '/'
    g90 = ast.literal_eval(str(datag[0]))
    if '0 inst' not in g90[-1]:
        c1 = get_indexo(g90)
        g90 = g90[c1[0] + 1:c1[-1]]
        h90_al, d90_al = convert_str_to_list(g90, 0)
        df_g90 = pd.DataFrame(d90_al, columns=h90_al)
        df_g90['site'] = [df_g90.loc[i, 'GeranCellId'][:-1] for i in range(len(df_g90))]
        df_g90 = df_g90[df_g90['site'] == str(data.loc[row, '2G CODE final'])]
        df_g900 = df_g90[(df_g90['connectedG31Tg'] != 'null') | (df_g90['connectedG12Tg'] != 'null')]
        if len(df_g90) != 0:
            if len(df_g900) != 0:
                s_g90 = lToS(list(df_g90['state'].unique()))
            else:
                s_g90 = 'Not integrated but cell defined and ' + lToS(list(df_g90['state'].unique()))

        else:
            s_g90 = '/'
    print(s_g18, s_g90)

    ### 3G check ####

    #### RNC U2100 ####
    ru21 = ast.literal_eval(str(datag[3]))
    nu21 = ast.literal_eval(str(datag[5]))
    s_r21, s_n21 = '/', '/'
    if '0 inst' not in ru21[-1]:
        u21 = ru21[1:-2]
        hu21_al, du21_al = convert_str_to_list(u21, 0)
        df_u21 = pd.DataFrame(du21_al, columns=hu21_al)
        df_u21['site'] = [df_u21.loc[i, 'UtranCellId'][:-1] for i in range(len(df_u21))]
        df_u21 = df_u21[df_u21['site'] == str(data.loc[row, '3G CODE  final'])]
        if len(df_u21) != 0:
            s_r21 = lToS(list(df_u21['administrativeState'].unique()) + list(df_u21['operationalState'].unique()))
        else:
            s_r21 = '/'
    if '0 inst' not in nu21[-1]:
        c1 = get_indexso(nu21)
        nu21 = nu21[1:-2]
        if len(c1) != 0:
            print('youuud')
            nu21 = nu21[:c1[0] - 1]
        nhu21_al, ndu21_al = convert_str_to_list(nu21, 0)
        ndf_u21 = pd.DataFrame(ndu21_al, columns=nhu21_al)
        if len(ndf_u21) != 0:
            s_n21 = 'exist'
        else:
            s_n21 = '/'
    ### RNC U900 ###
    ru90 = ast.literal_eval(str(datag[2]))
    nu90 = ast.literal_eval(str(datag[4]))
    s_r90, s_n90 = '/', '/'
    if '0 inst' not in ru90[-1]:
        u90 = ru90[1:-2]
        hu90_al, du90_al = convert_str_to_list(u90, 0)
        df_u90 = pd.DataFrame(du90_al, columns=hu90_al)
        df_u90['site'] = [df_u90.loc[i, 'UtranCellId'][:-1] for i in range(len(df_u90))]
        df_u90 = df_u90[df_u90['site'] == str(data.loc[row, '3G CODE  final'])]
        if len(df_u90) != 0:
            s_r90 = lToS(list(df_u90['administrativeState'].unique()) + list(df_u90['operationalState'].unique()))
        else:
            s_r90 = '/'

    if '0 inst' not in nu90[-1]:
        c1 = get_indexso(nu90)
        nu90 = nu90[1:-2]
        if len(c1) != 0:
            print('youuud')
            nu90 = nu90[:c1[0] - 1]
        nhu90_al, ndu90_al = convert_str_to_list(nu90, 0)
        ndf_u90 = pd.DataFrame(ndu90_al, columns=nhu90_al)
        if len(ndf_u90) != 0:
            s_n90 = 'exist'
        else:
            s_n90 = '/'
    s_u90 = g3check(s_r90, s_n90)
    s_u21 = g3check(s_r21, s_n21)

    ### 4G check ####

    L21 = ast.literal_eval(str(datag[6]))
    L18 = ast.literal_eval(str(datag[7]))
    s_L21, s_L18 = '/', '/'
    #### L2100 ####
    if '0 inst' not in L21[-1]:
        c1 = get_indexso(L21)
        l21 = L21[1:-2]
        if len(c1) != 0:
            l21 = l21[:c1[0] - 1]
        if len(l21) != 0:
            nhl21_al, ndl21_al = convert_str_to_list(l21, 0)
            ndf_l21 = pd.DataFrame(ndl21_al, columns=nhl21_al)
            if len(ndf_l21) != 0:
                s_L21 = lToS(list(ndf_l21['availabilityStatus'].unique()))
            else:
                s_L21 = '/'
        else:
            s_L21 = '/'
    #### L1800 ####
    if '0 inst' not in L18[-1]:
        c1 = get_indexso(L18)
        l18 = L18[1:-2]
        if len(c1) != 0:
            l18 = l18[:c1[0] - 1]
        if len(l18) != 0:
            nhl18_al, ndl18_al = convert_str_to_list(l18, 0)
            ndf_l18 = pd.DataFrame(ndl18_al, columns=nhl18_al)
            if len(ndf_l18) != 0:
                s_L18 = lToS(list(ndf_l18['availabilityStatus'].unique()))
            else:
                s_L18 = '/'
        else:
            s_L18 = '/'
    full.append([s_L21, s_L18, s_u21, s_u90, s_g18, s_g90])

enmscripting.close(session)
globall = pd.DataFrame(full, columns=["STATUS L2100", "STATUS L1800", "STATUS U2100", "STATUS U900", "STATUS G1800",
                                      "STATUS G900"])
data_gloabl = pd.concat([data, globall], axis=1)

poll = {'CHECK ONAIR S': data_gloabl}