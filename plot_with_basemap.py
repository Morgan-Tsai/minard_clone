from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

#資料庫連線
connection = sqlite3.connect("data/minard.db")
city_df = pd.read_sql("""SELECT * FROM cities;""",con=connection)
temperature_df = pd.read_sql("""SELECT * FROM temperatures;""",con=connection)
troop_df = pd.read_sql("""SELECT * FROM troops;""",con=connection)
"""
print(city_df)
print(temperature_df)
print(troop_df)
"""
connection.close()

#地圖、城市圖、軍隊圖、氣溫圖的資料
#城市圖
loncs = city_df["lonc"].values
latcs = city_df["latc"].values
city_names = city_df["city"].values

#軍隊圖
rows = troop_df.shape[0]
lonps = troop_df["lonp"].values
latps = troop_df["latp"].values
survivals = troop_df["surviv"].values
directions = troop_df["direc"].values

#氣溫圖
temp_celsius = (temperature_df["temp"]*5/4).astype(int)
lonts = temperature_df["lont"].values
annotations = temp_celsius.astype(str).str.cat(temperature_df["date"],sep="°C ") #文字說明

#畫布設定:4張放在同一張圖上
#nrows=2 : 2個垂直排列的軸物件
#figsize :畫布長寬
#gridspec_kw :兩個軸物件的高度比
fig,axes = plt.subplots(nrows=2,figsize=(25,12),gridspec_kw={"height_ratios":[4,1]})

#繪製地圖、城市圖、軍隊圖(於第0個軸物件)
#繪製地圖
"""
projection:地圖圖資映射方式
resolution:解析度(i為intermediate中階)
width和height:地圖的寬度和高度，單位為公尺
lon_0和lat_0:地圖中心的經緯度
"""
m = Basemap(projection="lcc",resolution="i",width=1000000,height=400000,
            lon_0=31,lat_0=55,ax=axes[0])
m.drawcountries() #描繪國家邊界
m.drawrivers() #描繪國家河流
#繪製緯度
#labels(左,右,上,下):顯示位置
m.drawparallels(range(54,58),labels=[True,False,False,False]) 
#繪製經度
m.drawmeridians(range(23,56,2),labels=[False,False,False,True])

#繪製城市圖
x,y = m(loncs,latcs) #轉換成映射
for xi,yi,city_name in zip(x,y,city_names):
    axes[0].annotate(text=city_name,xy=(xi,yi),fontsize=14,zorder=2) #文字描述

#繪製軍隊圖
x,y = m(lonps,latps) #轉換成映射
for i in range(rows-1): #2筆一組，最後一筆當終點
    if directions[i] == "A":
        line_color = "tan" #膚色
    else:
        line_color = "black"
    
    start_stop_lons = (x[i],x[i+1])
    start_stop_lats = (y[i],y[i+1])
    line_width = survivals[i]
    m.plot(start_stop_lons,start_stop_lats,linewidth=line_width/10000,color=line_color,zorder=1) #zorder:圖層順序

#繪製氣溫圖(於第1個軸物件)
axes[1].plot(lonts,temp_celsius,linestyle="dashed",color="black")
for lont,temp_c,annotation in zip(lonts,temp_celsius,annotations):
    axes[1].annotate(annotation,xy=(lont-0.3,temp_c-7),fontsize=16) 
#軸物件設定   
axes[1].set_ylim(-50,10)
axes[1].spines["top"].set_visible(False) #隱藏邊框
axes[1].spines["right"].set_visible(False) #隱藏邊框
axes[1].spines["left"].set_visible(False) #隱藏邊框
axes[1].spines["bottom"].set_visible(False) #隱藏邊框
axes[1].grid(True,which="major",axis="both") #顯示主要格線
axes[1].set_xticklabels([])
axes[1].set_yticklabels([])
axes[0].set_title("Napoleon's disastrous Russian campaign of 1812",loc="left",fontsize=30)
plt.tight_layout()
plt.savefig("minard_clone.png")
