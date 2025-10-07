import pandas as pd
import sqlite3

class CreateMinardDB:
    def __init__(self):
        with open("data/minard.txt") as f:
            lines = f.readlines()
        #載入欄位資料
        column_names = lines[2].split()

        patterns_to_be_replaced = {"(",")","$",","}
        adjusted_column_names = []
        for column_name in column_names:
            for pattern in patterns_to_be_replaced:
                if pattern in column_name:
                    column_name = column_name.replace(pattern,"")
            adjusted_column_names.append(column_name)    
        self.lines = lines
        self.column_name_city = adjusted_column_names[:3]
        self.column_name_temperature = adjusted_column_names[3:7]
        self.column_name_troop = adjusted_column_names[7:]

    def create_city_dataframes(self):
        #載入城市資料
        #檔案7~26列、1~3欄(python的6~25列、0~2欄)
        i = 6
        longitudes,latitudes,cities = [],[],[] #經度,緯度,城市名
        while i <= 25:
            long,lat,city = self.lines[i].split()[:3]
            longitudes.append(float(long))
            latitudes.append(float(lat))
            cities.append(city)
            i += 1

        city_data = (longitudes,latitudes,cities) #轉成turple

        #轉成dataframes
        city_df = pd.DataFrame()
        for column_name,data in zip(self.column_name_city,city_data):
            city_df[column_name] = data 
        return city_df 

    def create_temperature_dataframe(self):    
        #載入溫度資料
        """     
        檔案7~15列、4~7欄(python的6~14列、3~6欄)
        注意:第11列(python的第10列)為遺漏值
        """
        i = 6
        longitudes,temperatures,days,dates = [],[],[],[] #經度,氣溫,天數,日期
        while i <= 14:
            lines_split = self.lines[i].split()
            longitudes.append(float(lines_split[3]))
            temperatures.append(int(lines_split[4]))
            days.append(int(lines_split[5]))
            if i == 10:
                dates.append("NOV 24")
            else:
                date_str = lines_split[6] + " " + lines_split[7]
                dates.append(date_str)
            i += 1

        temperature_data = (longitudes,temperatures,days,dates) #轉成turple

        #轉成dataframes
        temperature_df = pd.DataFrame()
        for column_name,data in zip(self.column_name_temperature,temperature_data):
            temperature_df[column_name] = data
        return temperature_df
    
    def create_troop_dataframe(self):
        #載入軍隊資料
        #檔案7~54列、倒數1~5欄(python的6~53列、倒數1~5欄)
        i = 6 
        #經度,緯度,存活軍隊數,方向,分區
        longitudes,latitudes,survivals,directions,divisions = [],[],[],[],[]
        while i <= 53:
            lines_split = self.lines[i].split()
            divisions.append(int(lines_split[-1]))
            directions.append(lines_split[-2])
            survivals.append(int(lines_split[-3]))
            latitudes.append(float(lines_split[-4]))
            longitudes.append(float(lines_split[-5]))
            i += 1

        troop_data = (longitudes,latitudes,survivals,directions,divisions) #轉成turple

        #轉成dataframes
        troop_df = pd.DataFrame()
        for column_name,data in zip(self.column_name_troop,troop_data):
            troop_df[column_name] = data
        return troop_df

    def create_database(self):
        #建立資料庫
        connection = sqlite3.connect("data/minard.db")
        city_df = self.create_city_dataframes()
        temperature_df = self.create_temperature_dataframe()
        troop_df = self.create_troop_dataframe()
        df_dict = {
            "cities":city_df,
            "temperatures":temperature_df,
            "troops":troop_df
        }
        for k,v in df_dict.items():
            v.to_sql(name=k,con=connection,index=False,if_exists="replace")
        connection.close()

create_minard_db = CreateMinardDB()
create_minard_db.create_database()