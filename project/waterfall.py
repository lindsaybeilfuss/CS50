import openpyxl
import pandas as pd
import numpy as np
import numexpr as  ne
import sqlite3

df = pd.read_excel('SepAug18.xlsx', sheet_name='Sheet1')
df['shipdate'] = df['shipdate'].astype('datetime64[ns]')
df['completeddate'] = df['completeddate'].astype('datetime64[ns]')

print(df.info())
#print(df.head())
#gives the number of rows and columns
# grouped = df.groupby(['type','reason','shipdate','completeddate'])[' amount '].sum()
# print(grouped)
#print(df[df.type == 'SM'])
#print(df.query('type == ["SM","SM2"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]'))
print(df.loc[df['condition'].isin(['Carrier Damaged','Customer Damaged','Unknown'])])
print(df.pivot_table(index=["condition","type"],columns=["shipdate"],aggfunc=np.sum,  fill_value=0))

#Calculate the life-to-date reimbursements
SM_reimbursements = df.query('type == ["SM"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["condition","type"], columns=["shipdate"],aggfunc=np.sum, fill_value=0)
SM2_reimbursements = df.query('type == ["SM2"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["condition","type"], columns=["shipdate"],aggfunc=np.sum, fill_value=0)
PSP_reimbursements = df.query('type == ["PSP"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["condition","type"], columns=["shipdate"],aggfunc=np.sum, fill_value=0)
Non_PSP_reimbursements = df.query('type == ["Non PSP"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["condition","type"], columns=["shipdate"],aggfunc=np.sum, fill_value=0)

#Calculate the % reimbursed, mapping shipdate to completeddate, syntax is: df.loc[rows_index, cols_index]
SM_waterfall = df.query('type == ["SM"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["shipdate"], columns=["completeddate"],aggfunc=np.sum, fill_value=0, margins=True, margins_name="SM Total")
SM_waterfall = SM_waterfall.div( SM_waterfall.iloc[:,-1], axis=0 )
print(SM_waterfall)
SM2_waterfall = df.query('type == ["SM2"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["shipdate"], columns=["completeddate"],aggfunc=np.sum, fill_value=0, margins=True, margins_name="SM2 Total")
SM2_waterfall = SM2_waterfall.div( SM2_waterfall.iloc[:,-1], axis=0 )
print(SM2_waterfall)
PSP_waterfall = df.query('type == ["PSP"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["shipdate"], columns=["completeddate"],aggfunc=np.sum, fill_value=0, margins=True, margins_name="PSP Total")
PSP_waterfall = PSP_waterfall.div( PSP_waterfall.iloc[:,-1], axis=0 )
print(PSP_waterfall)
Non_PSP_waterfall = df.query('type == ["Non PSP"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["shipdate"], columns=["completeddate"],aggfunc=np.sum, fill_value=0, margins=True, margins_name="NonPSP Total")
Non_PSP_waterfall = Non_PSP_waterfall.div( Non_PSP_waterfall.iloc[:,-1], axis=0 )
print(Non_PSP_waterfall)

#to write to more than one sheet in the workbook, must specify ExcelWriter object. To set the library used to write the Excel file, pass the engine keyword "xlsxwriter"
writer = pd.ExcelWriter('waterfall.xlsx', engine='xlsxwriter')
SM_reimbursements.to_excel(writer, sheet_name='Reimbursements')
SM_waterfall.to_excel(writer, sheet_name='Reimbursements', startcol=15)
SM2_reimbursements.to_excel(writer, sheet_name='Reimbursements', startrow=10)
SM2_waterfall.to_excel(writer, sheet_name='Reimbursements', startrow=10, startcol=15)
PSP_reimbursements.to_excel(writer, sheet_name='Reimbursements', startrow=20)
PSP_waterfall.to_excel(writer, sheet_name='Reimbursements', startrow=20, startcol=15)
Non_PSP_reimbursements.to_excel(writer, sheet_name='Reimbursements', startrow=30)
Non_PSP_waterfall.to_excel(writer, sheet_name='Reimbursements', startrow=30, startcol=15)
workbook = writer.book
worksheet = writer.sheets['Reimbursements']
writer.save()




