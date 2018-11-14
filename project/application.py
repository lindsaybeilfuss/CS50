import openpyxl
import pandas as pd
import numpy as np
import numexpr as  ne
import sqlite3
from flask import Flask, render_template, request, url_for


# Import the Flask class and create instance of the class ie. Configure application
# The first argument is the name of the applications module
# To run the application use $ export FLASK_APP=XXXX.py $ flask run
app = Flask(__name__)

connection=sqlite3.connect('reimbursement.db')

# Use the @app.route() decorator to tell Flask what URL should trigger function in Flask app
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate")
def waterfallcalc():
    df=pd.read_sql_query("SELECT * FROM rawrms", connection)
    SM_reimbursements = df.query('type == ["SM"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["condition","type"], columns=["shipdate"],aggfunc=np.sum, fill_value=0)
    SM2_reimbursements = df.query('type == ["SM2"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["condition","type"], columns=["shipdate"],aggfunc=np.sum, fill_value=0)
    PSP_reimbursements = df.query('type == ["PSP"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["condition","type"], columns=["shipdate"],aggfunc=np.sum, fill_value=0)
    Non_PSP_reimbursements = df.query('type == ["Non PSP"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["condition","type"], columns=["shipdate"],aggfunc=np.sum, fill_value=0)
    return render_template("calculate.html", data1=SM_reimbursements.to_html(), data2=SM2_reimbursements.to_html(), data3=PSP_reimbursements.to_html(), data4=Non_PSP_reimbursements.to_html())

@app.route("/reimbursementrate")
def reimburserate():
   #Calculate the % reimbursed, mapping shipdate to completeddate, syntax is: df.loc[rows_index, cols_index]
    df=pd.read_sql_query("SELECT * FROM rawrms", connection)
    SM_waterfall = df.query('type == ["SM"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["shipdate"], columns=["completeddate"],aggfunc=np.sum, fill_value=0, margins=True, margins_name="SM Total")
    SM_waterfall = SM_waterfall.div( SM_waterfall.iloc[:,-1], axis=0 )
    SM2_waterfall = df.query('type == ["SM2"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["shipdate"], columns=["completeddate"],aggfunc=np.sum, fill_value=0, margins=True, margins_name="SM2 Total")
    SM2_waterfall = SM2_waterfall.div( SM2_waterfall.iloc[:,-1], axis=0 )
    PSP_waterfall = df.query('type == ["PSP"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["shipdate"], columns=["completeddate"],aggfunc=np.sum, fill_value=0, margins=True, margins_name="PSP Total")
    PSP_waterfall = PSP_waterfall.div( PSP_waterfall.iloc[:,-1], axis=0 )
    Non_PSP_waterfall = df.query('type == ["Non PSP"] & condition == ["Carrier Damaged","Customer Damaged","Unknown"]').pivot_table(index=["shipdate"], columns=["completeddate"],aggfunc=np.sum, fill_value=0, margins=True, margins_name="NonPSP Total")
    Non_PSP_waterfall = Non_PSP_waterfall.div( Non_PSP_waterfall.iloc[:,-1], axis=0 )
    return render_template("calculate2.html", rate1=SM_waterfall.to_html(), rate2=SM2_waterfall.to_html(), rate3=PSP_waterfall.to_html(), rate4=Non_PSP_waterfall.to_html())

if __name__ == "__main__":
    app.run()