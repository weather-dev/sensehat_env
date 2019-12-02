import pandas as pd

def data_handle_pd():
    f_name = "csvFiles/CSVfile_Gen_2019-12-02.csv"
    df = pd.read_csv(f_name)
    calc_df = df.tail(5)
    temp_df = calc_df.loc[:,"Temperature"].mean()
    return temp_df
    
print(data_handle_pd())

if data_handle_pd() < 10:
    print("Its cold here")
elif data_handle_pd() > 11:
    print("Its too warm here!")
else:
    print("The temperature is just right")