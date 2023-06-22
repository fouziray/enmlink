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

'''ap = argparse.ArgumentParser()

ap.add_argument("-i", "--input", required=True, help="path of the data")

args = vars(ap.parse_args())'''
# access enm for alarm checking along with excel sheets generation 

def listToString(s, sn):
    str1 = ""
    for ele in s:
        str1 += str(ele) + sn
    return str1[:-1]


data = pd.read_excel('checks.xlsx')


def split_list(value, test_list):
    size = len(test_list)
    idx_list = [idx + 1 for idx, val in
                enumerate(test_list) if val == value]

    res = [test_list[i: j] for i, j in
           zip([0] + idx_list, idx_list +
               ([size] if idx_list[-1] != size else []))]
    return res


def convert_str_to_list(x, i):
    if i != -1:
        head = x[i].split('\t')
    else:
        head = []
    filee = []
    for r in range(i + 1, len(x) - 1):
        filee.append(x[r].split('\t'))
    return head, filee


pss = str(getpass())
session = enmscripting.open('https://algenm1.atmmobilis.local', "", "")
list_col = list(data.columns)
print(list_col)
poll = {}
for m in list_col:
    liste = listToString(list(data[data[m] != 'Not exist'][m]), ';')
    command2 = 'alarm get ' + str(liste) + ' -t'
    command3 = 'cmedit get ' + str(liste) + ' EutrancellTDD.(administrativeState,availabilityStatus) -t'
    command4 = 'cmedit get ' + str(
        liste) + ' RfPort.(RfPortId!=R,vswrSupervisionActive,vswrSupervisionSensitivity,vswrValue.(returnLoss)) -t'
    cmd = session.terminal()
    response2 = cmd.execute(command2)
    lines2 = str(response2.get_output())
    print('The command was successfully sent and a response received: ' + str(response2.is_command_result_available()))
    print('------------------')
    response3 = cmd.execute(command3)
    lines3 = str(response3.get_output())
    print('The command was successfully sent and a response received: ' + str(response3.is_command_result_available()))
    print('------------------')
    response4 = cmd.execute(command4)
    lines4 = str(response4.get_output())
    print('The command was successfully sent and a response received: ' + str(response4.is_command_result_available()))
    print('------------------')
    XX = ast.literal_eval(str(lines2))
    X3 = ast.literal_eval(str(lines3))
    X4 = ast.literal_eval(str(lines4))
    header_al, data_al = convert_str_to_list(XX, 0)
    _, data_al3 = convert_str_to_list(X3, 0)
    _, data_al4 = convert_str_to_list(X4, 0)
    header_al3 = ["NodeId", "ENodeBFunctionId", "EUtranCellTDDId", "administrativeState", "availabilityStatus"]
    print(data_al3)
    df_al = pd.DataFrame(data_al, columns=header_al)
    df_3 = pd.DataFrame(data_al3, columns=header_al3)[
        ["NodeId", "EUtranCellTDDId", "administrativeState", "availabilityStatus"]]
    header_al4 = ["NodeId", "EquipmentId", "FieldReplaceableUnitId", "RfPortId", "rfPortId", "vswrSupervisionActive",
                  "vswrSupervisionSensitivity", "vswrValue"]
    df_4 = pd.DataFrame(data_al4, columns=header_al4)[
        ["NodeId", "FieldReplaceableUnitId", "RfPortId", "vswrSupervisionActive",
         "vswrSupervisionSensitivity", "vswrValue"]]
    df_al = df_al[["presentSeverity", "NodeName", "specificProblem", "eventTime", "problemText"]].reset_index(drop=True)
    """if len(df_al) != 0:
        poll['Alarm list'] = df_al"""
    datagg = df_al
    data2 = df_3
    dataa3 = df_4
enmscripting.close(session)
datags = pd.read_excel('ALARMC.xlsx')
print(datags.columns)
iy = []
print('#######')
print(datagg)
for t in range(len(datagg)):
    if str(datagg.loc[t, "specificProblem"])!='None':
        e = list(datags[datags["specificProblem"] == datagg.loc[t, "specificProblem"]]['Reauired action '])
        if len(e)!=0:
            e=e[0]
        else:
            e='/'
    else:
        e = '/'
    iy.append(e)
datagg['Required action'] = iy
if len(datagg) != 0:
    poll['Alarm list'] = datagg
dataa1 = pd.read_excel('cell.xlsx')
dataa1 = dataa1.fillna('null')
dataa1['availabilityStatus'] = [str(dataa1.loc[row, 'availabilityStatus']) for row in range(len(dataa1))]
data2.drop(data2.tail(1).index, inplace=True)
data2.drop(data2.head(1).index, inplace=True)
data2 = data2.reset_index(drop=True)
# data2['availabilityStatus'] = [str(data2.loc[row, 'availabilityStatus']) for row in range(len(data2))]
data2['Comment'] = [
    list(dataa1[dataa1['availabilityStatus'] == str(data2.loc[row, 'availabilityStatus'])]['comment'])[0] for row in
    range(len(data2))]

list_full = list(data2['NodeId'].unique())
fullio = []
for row in list_full:
    bb = list(data2[data2['NodeId'] == row]['Comment'].unique())
    if len(bb) == 1:
        ds = pd.DataFrame({'Node': [row], 'Comment': [bb[0]]})
    elif len(bb) == 0:
        ds = pd.DataFrame({'Node': [row], 'Comment': ['/']})
    else:
        cu = Counter(list(data2[data2['NodeId'] == row]['Comment']))
        cuu = listToString([str(cu[r]) + ' cell ' + r for r in list(cu.keys())], ',')
        ds = pd.DataFrame({'Node': [row], 'Comment': [cuu]})
    fullio.append(ds)

dat = pd.concat(fullio)
if len(dat) != 0:
    poll['Cell status'] = dat

ff, ff2 = [], []
dataa3.drop(dataa3.tail(1).index, inplace=True)
dataa3.drop(dataa3.head(1).index, inplace=True)
dataa3 = dataa3.reset_index(drop=True)
for row in range(len(dataa3)):
    if dataa3.loc[row, 'vswrValue'].split('=')[-1] == '}':
        ff.append('/')
        ff2.append('check config vswr supervision')
    else:
        vswr = (1 + 10 ** ((-1 * float(dataa3.loc[row, 'vswrValue'].split('=')[-1][:-1])) / 20)) / (
                    1 - 10 ** ((-1 * float(dataa3.loc[row, 'vswrValue'].split('=')[-1][:-1])) / 20))
        ff.append(vswr)
        if vswr > 1.4:
            ff2.append('need to check VSWR on site  RFPort ' + dataa3.loc[row, 'rfPortId'] + ' for the ' + dataa3.loc[
                row, 'FieldReplaceableUnitId'])
        else:
            ff2.append('clean')

dataa3['VSWR'] = ff
dataa3['comment'] = ff2

dataa3_f = dataa3[['NodeId', "FieldReplaceableUnitId", "RfPortId", 'VSWR', 'comment']]

if len(dataa3_f) != 0:
    poll['VSWR CHECK'] = dataa3_f
import string

alphabet_string = string.ascii_uppercase
alphabet_list = list(alphabet_string) + ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM',
                                         'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                                         'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM',
                                         'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ',
                                         'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM',
                                         'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ',
                                         'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM',
                                         'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ']


def sheet_saving(df):
    name_file = 'Alarm_TDD_site' + str(datetime.now().date()) + '.xlsx'
    workbook = xlsxwriter.Workbook(name_file)
    for mm in list(df.keys()):
        list_c2 = list(df[mm].columns)
        df2 = df[mm].fillna('')
        data_x = df2.values.tolist()
        d = list(df[mm].columns)
        worksheet = workbook.add_worksheet(name=mm)
        for m in alphabet_list:
            n = m + ':' + m
            worksheet.set_column(n, 25)
        cell_format = workbook.add_format(
            {'bold': True, 'font': 'Verdana', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_format.set_font_size(8)
        cell_format.set_fg_color('#DBE5F1')
        cell_format.set_font_color('#1F497D')
        # 'ERBS','MOs', 'MOClass', 'Parameter', 'CurrentValue', 'BaselineValue','MO'
        for b, q in zip(list_c2, alphabet_list):
            worksheet.write(q + str(1), b, cell_format)
        cell_format2 = workbook.add_format(
            {'bold': False, 'font': 'Verdana', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_format2.set_font_size(8)
        # cell_format2.set_fg_color('#DBE5F1')
        cell_format2.set_font_color('#1F497D')
        cell_format2t = workbook.add_format(
            {'bold': False, 'font': 'Verdana', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_format2t.set_font_size(8)
        # cell_format2.set_fg_color('#DBE5F1')
        cell_format2t.set_text_wrap()
        cell_format2t.set_font_color('#1F497D')

        l, d1 = 1, data_x
        for ii in range(len(d1)):
            for m in range(len(d1[ii])):
                if m in [0, 9]:
                    worksheet.write(l + ii, m, d1[ii][m], cell_format)
                else:
                    worksheet.write(l + ii, m, d1[ii][m], cell_format2)

        format1c = workbook.add_format({'bg_color': '#00B0F0',
                                        'font_color': '#9C0006'})
        format1 = workbook.add_format({'bg_color': '#FFC7CE',
                                       'font_color': '#9C0006'})
        format2 = workbook.add_format({'bg_color': '#FFC000',
                                       'font_color': '#E26B0A'})
        format22 = workbook.add_format({'bg_color': '#C6EFCE',
                                        'font_color': '#006100'})
        str1 = 'A1:I' + str(len(d1) + 4)
        worksheet.conditional_format(str1, {'type': 'cell',
                                            'criteria': '==',
                                            'value': '"MAJOR"',
                                            'format': format1})
        worksheet.conditional_format(str1, {'type': 'cell',
                                            'criteria': '==',
                                            'value': '"CRITICAL"',
                                            'format': format1})
        worksheet.conditional_format(str1, {'type': 'cell',
                                            'criteria': '==',
                                            'value': '"MINOR"',
                                            'format': format2})
        worksheet.conditional_format(str1, {'type': 'cell',
                                            'criteria': '==',
                                            'value': '"WARNING"',
                                            'format': format2})
        worksheet.conditional_format(str1, {'type': 'cell',
                                            'criteria': '==',
                                            'value': '"INDETERMINATE"',
                                            'format': format2})
        worksheet.conditional_format(str1, {'type': 'cell',
                                            'criteria': '==',
                                            'value': '"UP"',
                                            'format': format22})

    workbook.close()
    return name_file


sheeexcel_name = sheet_saving(poll)