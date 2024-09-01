import os
import pandas as pd
import numpy as np
from datetime import datetime

def cut_data(dataframe, time, timecolumn):
    dataframe = pd.DataFrame(dataframe)
    minutes = time * 60
    split_dataframes = []
    start_index = 0
    for index, row in dataframe.iterrows():
        if row[timecolumn] > minutes:
            split_dataframes.append(dataframe.iloc[start_index:index])
            start_index = index

    # Append the remaining part of the DataFrame
    split_dataframes.append(dataframe.iloc[start_index:])

    return split_dataframes

def field_counter(dataf, min_number, exclude_words=None):
    dataf=pd.DataFrame(dataf)
    field_counts = {}
    split_dfs = []
    start_index = 0
    index2=None
    row=None
    if len(dataf)<min_number:
        pass
    else:
        index2=0
        counter=0
        lastcounter=0
        for index, row in dataf.iterrows():
            counter=counter+1
            index2=index2+1
            names = [name for name in row['Terrains'].split() if name not in (exclude_words or [])]
            for name in names:
                field_counts[name] = field_counts.get(name, 0) + 1

            most_common_fields = sorted(field_counts, key=field_counts.get, reverse=True)
            if len(most_common_fields)==0:
                most_common_fields.append("Foo")
            if (most_common_fields[0] not in names):
                if index2>min_number:
                    #print("index2:",index2)
                    #print("Last:",lastcounter)
                    #print("Counter:",counter)
                    splitted=dataf.iloc[lastcounter:(counter-1)]
                    lastcounter=counter
                    index2=0
                    lendf=len(splitted)
                    dfterr = pd.DataFrame({f'PrevTerrain': pd.Series([most_common_fields[0]] * lendf)})
                    dfterr=dfterr.reset_index(drop=True)
                    splitted=splitted.reset_index(drop=True)
                    splitted = pd.concat([splitted, dfterr], axis=1)
                    #splitted.loc[:,"PrevTerrain"]=most_common_fields[0]
                    split_dfs.append(splitted)
                    #print("len:",len(splitted))
                    field_counts = {}
                else:
                    index2=0
                    #field_counts=0
                    lastcounter=counter
                    field_counts = {}
        #final=dataf.iloc[lastcounter:]
        #if len(final)>min_number:
        #    split_dfs.append(final)
        #    field_counts = {}
    return split_dfs

def get_summary_stats(df, columns=None):
    # Default columns if not provided
    default_columns = ["Time", "EngineCoolantTemperature", "EngineOilTemp",
                        "RelativeEngineTorque", "WheelSpeed", "AmbientTemperature",
                        "RearPTOSpeed", "ActualEngineTorque","PrevTerrain"]

    # Use default columns if not provided
    if columns is None:
        columns = default_columns

    # Make sure that the specified columns exist in the DataFrame
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the DataFrame.")

    # Calculate the requested statistics
    #print(df["Time"])
    time_value_start = df["Time"].iloc[0]
    time_value_end = df["Time"].iloc[-1]
    
    format_without_seconds = "%m/%d/%Y %H:%M"
    
    try:
        start_time = datetime.strptime(time_value_start, "%m/%d/%Y %H:%M:%S")
    except ValueError:
        start_time = datetime.strptime(time_value_start, format_without_seconds)

    try:
        end_time = datetime.strptime(time_value_end, "%m/%d/%Y %H:%M:%S")
    except ValueError:
        end_time = datetime.strptime(time_value_end, format_without_seconds)

    start_day = start_time.day
    start_month = start_time.month
    start_year = start_time.year
    
    time_difference = (end_time - start_time).total_seconds()
    time_difference = round((time_difference/60),2)
    
    PrevTerrain=df["PrevTerrain"].iloc[0]
    #print(PrevTerrain)
    coolant_temp_avg = df["EngineCoolantTemperature"].mean()
    coolant_temp_avg = coolant_temp_avg.round(2)
    oil_temp_avg = df["EngineOilTemp"].mean()
    oil_temp_avg = oil_temp_avg.round(2)
    
    rel_engine_torque_rounded = df["RelativeEngineTorque"].round(1)
    rel_engine_torque_mode = rel_engine_torque_rounded.mode().iloc[0]

    wheel_speed_rounded = df["WheelSpeed"].round(1)
    #wheel_speed_mode = wheel_speed_rounded.mode().iloc[0]
    modes = wheel_speed_rounded.mode()

    try:
        wheel_speed_rounded = df["WheelSpeed"].round(1)
        modes = wheel_speed_rounded.mode()
    
        if modes.iloc[0] == 0:
            wheel_speed_mode = modes.iloc[1] if len(modes) > 1 else None
        else:
            wheel_speed_mode = modes.iloc[0]

    except Exception as e:
        wheel_speed_mode = 0

    
    ambient_temp_avg = df["AmbientTemperature"].mean()
    ambient_temp_avg = ambient_temp_avg.round(2)
    
    rear_pto_speed_mode = df["RearPTOSpeed"].mode().iloc[0]
    engine_speed_mode = df["EngineSpeed"].mode().iloc[0]
    
    actual_engine_torque_rounded = df["ActualEngineTorque"].round(1)
    actual_engine_torque_mode = actual_engine_torque_rounded.mode().iloc[0]

    num_zeros = ((df["WheelSpeed"] == 0) | (df["WheelSpeed"] == "0")).sum()
    total_entries = len(df)
    idle_time_ratio = (num_zeros / total_entries).round(4)

    return(time_value_start,
           start_day,
           start_month,
           start_year,
           time_difference,
           idle_time_ratio,
           coolant_temp_avg,
           oil_temp_avg,
           rel_engine_torque_mode,
           wheel_speed_mode,
           ambient_temp_avg,
           rear_pto_speed_mode,
           engine_speed_mode,
           actual_engine_torque_mode,
           PrevTerrain)


