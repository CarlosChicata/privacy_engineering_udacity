from numpy import average
import pandas as pd
from datetime import date, timedelta, datetime
from math import floor


def age_range(x):
    multiplo = floor(x / 20)
    if multiplo <= 1:
        return "entre 0 y 20"
    else:
        x = 20*multiplo
        y = 20*(multiplo + 1)
        return "entre %s y %s" % (x,y,)

def anonymization_test_result():
    df_test = pd.read_excel("patients-by-test-results.xlsx")
    df_test["First name"] = ["****"]*df_test.shape[0]
    df_test["Last Name"] = ["***"]*df_test.shape[0]
    df_test["Test Results"] = ["*****"]*df_test.shape[0]
    df_test["City"] = ["*****"]*df_test.shape[0]
    df_test["Household Income"] = df_test["Household Income"].apply( lambda x : float(x[1:]))
    average_income = (df_test["Household Income"].max() - df_test["Household Income"].min()) / 2
    df_test["Household Income"] = df_test["Household Income"].apply( lambda x : "> %s" % (average_income,) if x > average_income else " <= %s" % (average_income,))
    df_test["Date of Birth"] = df_test["Date of Birth"].apply(lambda x : datetime.strptime(x, "%m/%d/%Y").date())
    df_test["Date of Birth"] = df_test["Date of Birth"].apply(lambda x : floor((date.today() - x)/timedelta(days=365)) )
    df_test["Date of Birth"] = df_test["Date of Birth"].apply(age_range)
    print(df_test.head(1))
    df_test.to_excel("patients-by-test-results.xlsx", index=False)

def anonymization_conditions():
    df_cond = pd.read_excel("patients-by-condition.xlsx")
    print(df_cond.head(1))
    df_cond["First name"] = ["****"]*df_cond.shape[0]
    df_cond["Last Name"] = ["***"]*df_cond.shape[0]
    df_cond["Condition"] = ["*****"]*df_cond.shape[0]
    df_cond["Zip Code"] = ["*****"]*df_cond.shape[0]
    df_cond["Age"] = df_cond["Age"].apply(int) 
    df_cond["Age"] = df_cond["Age"].apply(age_range)
    df_cond.to_excel("patients-by-condition.xlsx", index=False)
    print(df_cond.head(1))

anonymization_conditions()
anonymization_test_result()

