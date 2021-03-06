
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Slider, Select, Paragraph, TableColumn, DataTable, Button, Panel, Tabs, LinearAxis, Range1d
from bokeh.plotting import figure, show
from bokeh.palettes import Colorblind8
import numpy as np
from scipy.interpolate import interp1d
from bokeh.tile_providers import CARTODBPOSITRON, get_provider, Vendors

time_range=list(range(0, 24))
time_range1=list(range(1,13))
initial_dims=[3, 2, 1, .3]
# [length, width, height, sand_thickness]
rh1=0.5 #needs to be updates to be based on each weather data set
materials=["Brick", "Cardboard", "Aluminum", "Concrete"]
loc_and_time=["Bethlehem, PA", "Miami, Fl", "Puerto Jiménez, Costa Rica", "Quito, Ecuador", "Nairobi, Kenya", "Lusaka, Zambia"]
time_ranges=["12 Months", "24 Hours"]

#defining lists for temperatures
beth_hourly1=[66, 65, 64, 64, 64, 64, 64, 65, 66, 67, 70, 71, 73, 73, 72, 75, 76, 76, 76, 75, 75, 73, 71, 70] #hourly bethlhem temperatures for June 18, 2020
costa_hourly_C=[24, 24, 24, 24, 24, 24, 24, 25, 26, 27, 28, 28, 28, 28, 27, 27, 28, 28, 25, 25, 25, 25, 25, 24] #hourly june 24, 2020
kenya_hourly_C=[15, 15, 15, 15, 14, 14, 14, 14, 15, 16, 18, 19, 20, 21, 21, 22, 22, 22, 21, 19, 19, 18, 17, 16]
miami_hourly_C=[29, 28, 28, 28, 28, 28, 28, 28, 29, 30, 30, 31, 31, 31, 32, 31, 31, 31, 31, 30, 29, 29, 29, 29]
ecuador_hourly_C=[11, 11, 10, 10, 9, 9, 9, 9, 12, 14, 17, 19, 20, 20, 20, 19, 18, 17, 15, 14, 13, 12, 12, 11]
zambia_hourly_C=[14, 13, 13, 13, 13, 12, 12, 12, 13, 16, 18, 19, 20, 20, 21, 21, 20, 20, 18, 17, 16, 16, 15, 14]

beth_yearly_F=[27.5, 31, 39, 50, 60, 69, 73.5, 71.5, 64, 52.5, 43, 32.5]
CostaRica_C=[26.2, 26.5, 27.7, 28, 27.3, 26.5, 26.7, 26.3, 26, 25.9, 25.6, 25.7]
miami_F=[68, 70, 72.5, 75.5, 80, 82.5, 84, 84, 82.5, 80, 75, 70.5]
Ecuador_C=[15.5, 15.55, 15.45, 15.55, 15.55, 15.5, 15.45, 15.9, 15.85, 15.65, 15.45, 15.5]
Kenya_C=[19.7, 20.2, 20.7, 20.2, 19.1, 17.8, 16.7, 17.2, 18.6, 19.8, 19.3, 19.2]
Zambia_C=[22.5, 22.4, 21.95, 20.55, 18.25, 15.8, 15.6, 17.85, 21.6, 23.95, 23.9, 22.75]

get_provider(Vendors.CARTODBPOSITRON)
tile_provider=get_provider('CARTODBPOSITRON')

# range bounds supplied in web mercator coordinates
mapp = figure(x_range=(-14000000, 7000000), y_range=(-4000000, 6060000),
           x_axis_type="mercator", y_axis_type="mercator", margin=(0, 0, 0, 20), aspect_ratio=4/3, sizing_mode='scale_both')
mapp.add_tile(tile_provider)
mapp.circle(x=-8389827.854690, y=4957234.168513, size=10, fill_color='blue', fill_alpha=0.7, legend_label="Bethlehem, PA")
mapp.circle(x=-8931102.469623, y=2972160.043550, size=10, fill_color='darkred', fill_alpha=.7, legend_label="Miami, FL")
mapp.circle(x=-9290844.007714, y=953484.087498, size=10, fill_color='darkgreen', fill_alpha=0.7, legend_label="Puerto Jiménez, Costa Rica")
mapp.circle(x=-8741967.501084, y=-22993.039835, size=10, fill_color='peru', fill_alpha=0.7, legend_label="Quito, Ecuador")
mapp.circle(x=4105174.772925, y=-145162.620135, size=10, fill_color='mediumpurple', fill_alpha=0.7, legend_label="Nairobi, Kenya")
mapp.circle(x=3564845.194234, y=-948229.994036, size=10, fill_color='navy', fill_alpha=0.7, legend_label="Lusaka, Zambia")
mapp.legend.background_fill_alpha=0.5



def FtoC(Ftemps):
    newTemps=[]
    for x in Ftemps:
        n=(x-32)*(5/9)
        newTemps.append(n)
    return newTemps

beth_yearly_C=FtoC(beth_yearly_F)
Miami_C=FtoC(miami_F)


class Weather:
    def __init__(self, temps_list, name, time_int, rh):
        self.location=name
        self.temps=temps_list
        self.time=time_int
        self.rh=rh
 
beth_yearly=Weather(beth_yearly_C, "Bethlehem, PA", "12 Months", [.691, .667, .626, .609, .656, .679, .688, .719, .74, .718, .705, .714])
CostaRica=Weather(CostaRica_C, "Puerto Jiménez, Costa Rica", "12 Months", [.592, .554, .527, .642, .743, .763, .759, .766, .768, .796, .788, .713])
Miami=Weather(Miami_C, "Miami, FL", "12 Months", [.607, .603, .558, .584, .605, .661, .662, .674, .697, .648, .617, .647])
Ecuador=Weather(Ecuador_C, "Quito, Ecuador", "12 Months", [.75, .80, .80, .80, .8, .7, .65, .6, .7, .75, .75, .8])
Kenya=Weather(Kenya_C, "Nairobi, Kenya", "12 Months", [.7, .6, .65, .8, .8, .75, .75, .7, .65, .65, .8, .75])
Zambia=Weather(Zambia_C, "Lusaka, Zambia", "12 Months", [.86, .89, .84, .66, .57, .59, .56, .45, .43, .32, .57, .71] )

beth_hourly1_C=Weather(FtoC(beth_hourly1), "Bethlehem, PA", "24 Hours", .679)
Costa_hourly=Weather(costa_hourly_C, "Puerto Jiménez, Costa Rica", "24 Hours", .763)
Kenya_hourly=Weather(kenya_hourly_C, "Nairobi, Kenya", "24 Hours", .75)
Miami_hourly=Weather(miami_hourly_C, "Miami, FL", "24 Hours", .661)
Ecuador_hourly=Weather(ecuador_hourly_C, "Quito, Ecuador", "24 Hours", .7)
Zambia_hourly=Weather(zambia_hourly_C, "Lusaka, Zambia", "24 Hours", .652)

weather_sets=[beth_yearly, CostaRica, Miami, Ecuador, Kenya, Zambia]
hourly_set=[beth_hourly1_C, Costa_hourly, Miami_hourly, Ecuador_hourly, Kenya_hourly, Zambia_hourly]

TOOLS = "pan,undo,redo,reset,save,box_zoom,tap"
diff_temps=figure(title="Average Temperature Throughout the Year", x_axis_label="Months", y_axis_label="Temperature in Celsius", tools=TOOLS, aspect_ratio=4/3, sizing_mode='scale_both')
diff_temps.title.text_font_size='14pt'
diff_temps.xaxis.ticker = list(range(1, 13))
diff_temps.xaxis.major_label_overrides={1:'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 
                                        7: "July", 8:'August', 9:'September', 10: 'October', 11: 'November', 12: 'December'}
diff_temps.xaxis.major_label_orientation=1

diff_temps.line(time_range1, beth_yearly.temps, legend_label=beth_yearly.location, line_width=2, color='blue')
diff_temps.line(time_range1, CostaRica.temps, legend_label=CostaRica.location, line_width=2, line_dash=[2,8], color='darkgreen')
diff_temps.line(time_range1, Miami.temps, legend_label=Miami.location, line_width=2, color='darkred')
diff_temps.line(time_range1, Ecuador.temps, legend_label=Ecuador.location, line_width=2, line_dash=[8,2], color='peru')
diff_temps.line(time_range1, Kenya.temps, legend_label=Kenya.location, line_width=2, line_dash=[2,2], color='mediumpurple')
diff_temps.line(time_range1, Zambia.temps, legend_label=Zambia.location, line_width=2, line_dash=[4,4], color='navy')

diff_temps.legend.click_policy="hide"
diff_temps.legend.location='bottom_left'
diff_temps.legend.background_fill_alpha=0.7

hourly_temps=figure(title="Temperatures Throughout One Day in Mid-June", x_axis_label="Time in Hours", y_axis_label="Temperature in Celsius", tools=TOOLS, aspect_ratio=4/3, sizing_mode='scale_both')
hourly_temps.title.text_font_size='14pt'
#for x in range(0, 6):
 #   hourly_temps.line(time_range, hourly_set[x].temps, legend_label=hourly_set[x].location, line_width=2, color=colors[x])
hourly_temps.line(time_range, beth_hourly1_C.temps, legend_label=beth_hourly1_C.location, line_width=2, color='blue')
hourly_temps.line(time_range, Costa_hourly.temps, legend_label=Costa_hourly.location, line_width=2, line_dash=[2,8], color='darkgreen')
hourly_temps.line(time_range, Miami_hourly.temps, legend_label=Miami_hourly.location, line_width=2, color='darkred')
hourly_temps.line(time_range, Ecuador_hourly.temps, legend_label=Ecuador_hourly.location, line_width=2, line_dash=[8,2], color='peru')
hourly_temps.line(time_range, Kenya_hourly.temps, legend_label=Kenya_hourly.location, line_width=2, line_dash=[2,2], color='mediumpurple')
hourly_temps.line(time_range, Zambia_hourly.temps, legend_label=Zambia_hourly.location, line_width=2, line_dash=[4,4], color='navy')

hourly_temps.legend.click_policy='hide'
hourly_temps.legend.location='bottom_left'
hourly_temps.legend.background_fill_alpha=0.7

humid=figure(title="Average Humidity Throughout The Year", x_axis_label="Months", y_axis_label="Relative Humidity", x_range=diff_temps.x_range, tools=TOOLS, aspect_ratio=4/3, width=600)
humid.title.text_font_size='14pt'
humid.xaxis.ticker = list(range(1, 13))
humid.xaxis.major_label_overrides={1:'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 
                                        7: "July", 8:'August', 9:'September', 10: 'October', 11: 'November', 12: 'December'}
humid.xaxis.major_label_orientation=1

humid.line(time_range1, beth_yearly.rh, legend_label=beth_yearly.location, line_width=2, color='blue')
humid.line(time_range1, CostaRica.rh, legend_label=CostaRica.location, line_width=2, line_dash=[2,8], color='darkgreen')
humid.line(time_range1, Miami.rh, legend_label=Miami.location, line_width=2, color='darkred')
humid.line(time_range1, Ecuador.rh, legend_label=Ecuador.location, line_width=2, line_dash=[8,2], color='peru')
humid.line(time_range1, Kenya.rh, legend_label=Kenya.location, line_width=2, line_dash=[2,2], color='mediumpurple')
humid.line(time_range1, Zambia.rh, legend_label=Zambia.location, line_width=2, line_dash=[4,4], color='navy')

humid.legend.click_policy="hide"
humid.legend.location='bottom_left'
humid.legend.background_fill_alpha=0.7

def calc_HC (temps, dims, conductivity, desired_temp):
    k=conductivity
    Area=2*(dims[0]*dims[2])+ 2*(dims[1]*dims[2])
    Tcold=desired_temp
    d=dims[3]
    new_list=[]
    for i in temps:
        new_list.append(24*30*(k*Area)*(i-Tcold)/d)
    return new_list

def HC_hourly (temps, dims, conductivity, desired_temp):
    k=conductivity
    Area=2*(dims[0]*dims[2])+ 2*(dims[1]*dims[2])
    Tcold=desired_temp
    d=dims[3]
    new_list=[]
    for i in temps:
        new_list.append((k*Area)*(i-Tcold)/d)
    return new_list

k_sand = 0.27  # thermal conductivity of dry sand W/mK
k_water = 0.6  # thermal conductivity of water W/mK
k_brick = 0.72  # thermal conductivity of brick W/mK
e_sand = 0.343  # porosity of sand


out1=calc_HC(CostaRica.temps, initial_dims, k_brick, 15)
#print(out1)
source=ColumnDataSource(data=dict(time=time_range1, output=out1))
start1=np.min(source.data['output'])
end1=np.max(source.data['output'])

g1=figure(title="Heat per Time", x_axis_label="Time in Months", y_axis_label="Heat Conduction per Time", tools=TOOLS, aspect_ratio=4/3, sizing_mode='scale_both',  margin=(20, 20, 20, 10))
g1.line('time', 'output', source=source, color="purple", legend_label="Heat Conduction", line_dash=[4,4], line_width=3)
g1.y_range=Range1d(start1, end1)
g1.legend.click_policy="hide"
g1.legend.background_fill_alpha=0.5
g1.title.text_font_size='14pt'
g1.legend.location='top_left'

slide_length=Slider(title="Length of Chamber", value=initial_dims[0], start=0, end=12, step=0.5, width=450, margin=(10, 0, 5, 30))
slide_width=Slider(title="Width of Chamber", value=initial_dims[1], start=0, end=12, step=0.5, width=450, margin=(5, 0, 5, 30))
slide_height=Slider(title="Height of Chamber", value=initial_dims[2], start=0, end=5, step=0.25, width=450, margin=(5, 0, 5, 30))
slide_thick=Slider(title="Thickness of Sand Layer in Chamber Wall", value=initial_dims[3], start=0, end=1, step=0.001, width=450, margin=(5, 0, 5, 30))
select_material=Select(title="Choice of Material for Walls of the Chamber:", value="Brick", options=materials, width=400, margin=(5, 0, 5, 20))
slide_desired_temp=Slider(title="Desired Temperature for the Inner Chamber", value=20, start=2, end=50, step=0.5, width=450, margin=(5, 5, 5, 30))
location_select=Select(title="Location", value="Puerto Jiménez, Costa Rica", options=loc_and_time, width=400, margin=(10, 5, 5, 20))
time_select=Select(title="Time Interval", value="12 Months", options=time_ranges, width=400, margin=(5, 5, 5, 20))
calculate_button=Button(label="Calculate", button_type='success', background='lightblue', width=450, margin=(5, 0, 5, 20))

def latent_heat(temp):
    #Interpolating the values for latent heat of evaporation
    y = [45054, 44883,44627,44456,44200,43988,43774,43602,43345,43172,42911,42738,42475,42030,41579,41120] #latent heat of vaporization array
    x = [0,5,10,15,20,25,30,35,40,45,50,55,60,70,80,90] #water temperature array
    f1 = interp1d(x, y, kind= 'cubic')
    return f1(temp)

latent_out=latent_heat(CostaRica.temps)


def SVP(temp):
    #Interpolate the values for Saturated Vapor Pressure
    x=[.01, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
       30, 31, 32, 33, 34, 35, 36, 38, 40, 45, 50, 55, 60, 65, 70]
    y=[0.00611, 0.00813, 0.00872, 0.00935, 0.01072, 0.01228, 0.01312, 0.01402, 0.01497, 0.01598, 0.01705, 0.01818, 0.01938, 0.02064, 0.02198,
       0.02339, 0.02487, 0.02645, 0.02810, 0.02985, 0.03169, 0.03363, 0.03567, 0.03782, 0.04008, 0.04246, 0.04496, 0.04759, 0.05034, 0.05324,
       0.05628, 0.05947, 0.06632, 0.07384, 0.09593, .1235, .1576, .1994, .2503, .3119]
    vals=interp1d(x, y, kind='cubic')
    return vals(temp)

def water_needed(dims, temp, SVP, rh):
    theta=34.5 #(kg/(m^2*hr))
    SA=2*(dims[0]+dims[3]+.225)*dims[2] + 2*dims[2]*(dims[1]+dims[3]+.225)
    A = 18.3036
    B = 3816.44
    C = -46.13
    p_star=[]
    p_air=[]
    evap_rate=[]
    for i in temp:
        p_star.append(np.exp(A - B / (C + i + 273))) 
        # Antoine equation for vapor pressure at outside air
    for j in range(0, 12):
        p_air.append(rh[j]*p_star[j])
    #for j in p_star:
     #   p_air.append(rh*j) 
        # bulk pressure of air at t bulk
    for x in range(0,12):
        yy=theta*SA*((p_star[x]-p_air[x])/760) #in L/hour
        yy=yy*(24*30) #in L/month
        evap_rate.append(yy)
    return evap_rate

def water_needed_hourly(dims, temp, SVP, rh):
    theta=34.5 #(kg/(m^2*hr))
    SA=2*(dims[0]+dims[3]+.225)*dims[2] + 2*dims[2]*(dims[1]+dims[3]+.225)
    A = 18.3036
    B = 3816.44
    C = -46.13
    p_star=[]
    p_air=[]
    evap_rate=[]
    for i in temp:
        p_star.append(np.exp(A - B / (C + i + 273))) 
        # Antoine equation for vapor pressure at outside air
    for j in p_star:
        p_air.append(rh*j) 
        # bulk pressure of air at t bulk 
    for x in range(0,24):
        yy=theta*SA*((p_star[x]-p_air[x])/760) #in L/hour
       # yy=yy*(1/1000)*(3600) #in L/hour
        evap_rate.append(yy)
    return evap_rate

vap_init=[]
for p in CostaRica.temps:
    vap_init.append(SVP(p))
vap1_init=[]
for p in Costa_hourly.temps:
    vap1_init.append(SVP(p))

water_monthly=water_needed(initial_dims, CostaRica.temps, vap_init, CostaRica.rh)
water_trial=water_needed_hourly(initial_dims, Costa_hourly.temps, vap1_init, Costa_hourly.rh)
#print(sum(water_monthly))
#print(sum(water_monthly)/365)
#print(sum(water_trial))
sourceW=ColumnDataSource(data=dict(time=time_range1, temps=CostaRica.temps, water=water_monthly))

#g3=figure(title="Water Added to System For It To Function Properly", x_axis_label='Time in Months', y_axis_label='Water Added (in Liters)', tools=TOOLS)
#g3.line('time', 'water', source=sourceW, color='blue', line_width=2)
#g3.title.text_font_size='12pt'

#Evaporative Cooling Rate Q/t=mLv/t
def evap_cool(mass, latent, time):
    cooling_rate=[]
    for w in range(0,12):
        cooling_rate.append((mass[w]*latent[w])/100)
    return cooling_rate

def evap_cool_hourly(mass, latent, time):
    cooling_rate=[]
    for w in range(0,24):
        cooling_rate.append((mass[w]*latent[w])/100)
    return cooling_rate

evap_out=evap_cool(water_monthly, latent_out, time_range1)    
source3=ColumnDataSource(data=dict(time=time_range1, evap_out=evap_out))
start=int(min(source3.data['evap_out']))
end=int(max(source3.data['evap_out']))
g1.extra_y_ranges['second']=(Range1d(start, end))
g1.line('time', 'evap_out', source=source3, color='orange', legend_label="Evaporation Cooling Rate", line_width=2, y_range_name='second')
ax2 = LinearAxis(y_range_name="second", axis_label="Evaporative Cooling Heat per Time")
g1.add_layout(ax2, 'left')


def cost_calc(dims, water_amount, mat):
    #dims=[brick_length, brick_width, brick_height, sand_thickness]
    L0=dims[0] #length of inner brick chamber
    w0=dims[1] #width of inner brick chamber
    L1 = 0.1125
    L3=0.1125#thickness of brick
    L2=dims[3] #thickness of sand
    h=dims[2] #height of chamber
    w1 = w0 + 2 * L1  # width of inner brick layer
    w2 = w1 + 2 * L2  # width of sand layer
    w3 = w2 + 2 * L3  # width of outer brick layer
    A0 = L0 * w0  # area of inner chamber
    A1 = ((L0 + L1) * w1) - A0  # area of inner brick layer
    A2 = ((L0 + L1 + L2) * w2) - A1  # area of sand layer
    A3 = ((L0 + L1 + L2 + L3) * w3) - A2  # area of outer brick layer
    V0 = A0 * h  # inner chamber volume
    V1 = A1 * h  # inner brick volume
    V2 = A2 * h  # sand volume
    V3 = A3 * h  # outer brick volume
    materials_cost=0
    if mat=="Brick":
       materials_cost= 1900*0.037*V1 + 1905*.05*V2 + 1900*0.037*V3
       #Brick cost 0.037 $/Kg and density is 1900 Kg/m^3
    elif mat=="Cardboard":
        materials_cost=1905*0.5*V2 + (V1+V2)*(0.11*689)
        #Cardboard cost $0.11/Kg and desnsity is 689 Kg/m^3
    elif mat=="Aluminum":
        materials_cost=1905*0.5*V2 + (V1+V2)*(1.754*2710)
        #Aluminum cost is $1.754/Kg and density is 2710 Kg/m^3
    elif mat=="Concrete":
        materials_cost=1905*0.5*V2 +(V1+V2)*(98.425)
        #Concrete cost is $98.425/m^3
    #cost of sand 0.05 $/kg
    #Density of Sand (kg/m^3): 1905
    water_cost=water_amount*0.0001
    final_cost=materials_cost+water_cost
    return final_cost

price1=cost_calc(initial_dims, sum(water_monthly), "Brick")
#price2=cost_calc(initial_dims, sum(water_trial), "Brick")
#print(price2)
#print(price1)
sourceP=ColumnDataSource(data=dict(price=[price1]))

tableName=[CostaRica.location]
tablePriceY=["$"+str(round(price1, 2))]
tablePriceD=["$"+str(round(price1/365,2))]
tableWaterY=[str(round(sum(water_monthly), 2))+" L"]
tableWaterD=[str(round(sum(water_monthly)/365, 2)) +" L"]
tableSpace=[str(round(initial_dims[0]*initial_dims[1]*initial_dims[2], 2))+" m^3"]
tableTime=[CostaRica.time]

sourceTable=ColumnDataSource(data=dict(name=tableName, time=tableTime, Year_Price=tablePriceY, Day_Price=tablePriceD, Year_Water=tableWaterY, Day_Water=tableWaterD, space=tableSpace))
columnsT=[TableColumn(field='name', title='Location'), TableColumn(field='time', title='Time Interval'), TableColumn(field='space', title='Storage Volume Capacity (in m^3)'), 
          TableColumn(field='Day_Water', title='Daily Water Input (in Liters)'), TableColumn(field='Year_Water', title='Yearly Water Input (in L)'),
          TableColumn(field='Day_Price', title='Daily Cost in $'), TableColumn(field='Year_Price', title='Yearly Cost in $')]
data_table=DataTable(source=sourceTable, columns=columnsT, width=750, margin=(5, 0, 0, 20))

def dew_point(temps, rh, time):
    dp_out=[]
    a = 17.27
    b = 237.7
    for t in time:
        alpha = b * (((a * temps[t]) / (b + temps[t])) + np.log(rh[t]))
        gamma = a - (((a * temps[t]) / (b + temps[t])) + np.log(rh[t]))
        dp_out.append(alpha / gamma)
    return dp_out
def dew_point_hourly(temps, rh, time):
    dp_out=[]
    a = 17.27
    b = 237.7
    for t in time:
        alpha = b * (((a * temps[t]) / (b + temps[t])) + np.log(rh))
        gamma = a - (((a * temps[t]) / (b + temps[t])) + np.log(rh))
        dp_out.append(alpha / gamma)
    return dp_out
dp_Costa=dew_point(CostaRica.temps, CostaRica.rh, range(0,12))
#print(dp_Costa)
g4=figure(title="Essential Temperature Values for Selected Location", x_axis_label="Time (in Months)", y_axis_label="Temperature (in Celsius)", tools=TOOLS, margin=(20, 20, 20, 20), aspect_ratio=4/3, sizing_mode='scale_both')
g4.title.text_font_size='14pt'
sourceDP=ColumnDataSource(data=dict(time=time_range1, temps=CostaRica.temps, dp=dp_Costa, T1=range(0,12)))
g4.line('time', 'temps', source=sourceDP, color='orange', line_width=2, legend_label="Ambient Temperature")
g4.line('time', 'dp', source=sourceDP, color='darkblue', line_width=2, line_dash=[4,4], legend_label="Dew-Point Temperature")
g4.legend.background_fill_alpha=0.5
g4.legend.location='top_left'
g4.legend.click_policy='hide'

def T1_calc(dims, temps, wanted_temp, mat, time_range):
    T_bulk = temps # degrees C of air surrounding outside
    Tc = wanted_temp  # degrees C of inner chamber
    m = 907  # kg of potatoes in a metric ton
    hr = 9  # heat of respiration of potatoes in ml CO2 per kg hr
    rate = 122  # kcal per metric ton * day respiration multiplied to get rate
    k_sand = 0.27  # thermal conductivity of dry sand W/mK
    k_water = 0.6  # thermal conductivity of water W/mK
    e_sand = 0.343  # porosity of sand
    k_ws = e_sand * k_water + (1 - e_sand) * k_sand  # calculates the thermal conductivity of wet sand
    L0 = dims[0] # length of inner chamber
    L1 = .1125  # length of inner brick layer
    L2 = dims[3]  # length of sand layer
    L3 = .1125  # length of outer brick layer
    w0 = dims[1] # width of inner chamber
    h0 = dims[2]  # height of every layer in meters
    A_chamber = L0*h0*2 + w0*h0*2
    A_innerbrick = (L0+L1)*h0*2 + (w0+L1)*h0*2
    A_sand = (L0+L1+L2)*h0*2 + (w0+L1+L2)*h0*2
    h1 = 50  # convective heat transfer coefficient of inner chamber air
    h2 = 5  # convective heat transfer coefficient of outside air
    cond=0
    if mat =="Brick":
        cond=0.72
    elif mat=="Cardboard":
        cond=0.048 
    elif mat=='Aluminum':
        cond=205 
    elif mat=='Concrete':
        cond=0.8
    # calculations
    q = hr * rate * 4.18 * (1 / 24) * (1 / 3600) * m/1000 * 1000  # total respiration rate of one metric ton of potatoes - in J/sec
    #print(q)
    T4 = -((q * (1 / (h1*A_chamber))) - Tc)
    T3 = -((q * (L1 / (cond*A_innerbrick))) - T4)
    T2 = -((q * (L2 / (k_ws*A_sand))) - T3)
    T1=[]
    for i in time_range:
        abc = (((L3 * h2 * T_bulk[i]) / k_brick) + T2) / (1 + (L3 * h2) / k_brick)
        T1.append(abc)
    #print(T1)
    return T1
Costa_T1=T1_calc(initial_dims, CostaRica.temps, 18, "Brick", range(0,12))
sourceDP.data=dict(time=time_range1, temps=CostaRica.temps, dp=dp_Costa, T1=Costa_T1)
g4.line('time', 'T1', source=sourceDP, legend_label="Outer Wall Temperature", line_width=2, line_dash=[8,2], color='purple')

def update_data(attr, old, new):
    #Get Slider Values
    length=slide_length.value
    height=slide_height.value
    width=slide_width.value
    mat=select_material.value
    thick=slide_thick.value
    want_temp=slide_desired_temp.value
    loc=location_select.value
    time=time_select.value
    cond=0
    place=CostaRica
    #loc_and_time=["Bethlehem, PA", "Miami, Fl", "Puerto Jiménez, Costa Rica", "Quito, Ecuador", "Nairobi, Kenya", "Lusaka, Zambia"]
    
    if mat =="Brick":
        cond=0.72
    elif mat=="Cardboard":
        cond=0.048 
    elif mat=='Aluminum':
        cond=205 
    elif mat=='Concrete':
        cond=0.8
        
    if time=="12 Months":
        if loc=="Puerto Jiménez, Costa Rica":
            place=CostaRica
        elif loc=="Miami, FL":
            place=Miami
        elif loc=="Quito, Ecuador":
            place=Ecuador
        elif loc=="Nairobi, Kenya":
            place=Kenya
        elif loc=="Lusaka, Zambia":
            place=Zambia
        elif loc=="Bethlehem, PA":
            place=beth_yearly
        dims=[length, width, height, thick]
        out=calc_HC(place.temps, dims, cond, want_temp)
        vap=[]
        for p in place.temps:
            vap.append(SVP(p))
        water=water_needed(dims, place.temps, vap, place.rh)
        latent=latent_heat(place.temps)
        evap=evap_cool(water, latent, time_range1)
        dp=dew_point(place.temps, place.rh, range(0,12))
        T1=T1_calc(dims, place.temps, want_temp, mat, range(0,12))
    
        source.data=dict(time=time_range1, output=out)
        sourceW.data=dict(time=time_range1, temps=place.temps, water=water)
        source3.data=dict(time=time_range1, evap_out=evap)
        sourceDP.data=dict(time=time_range1, temps=place.temps, dp=dp, T1=T1)
        g1.extra_y_ranges['second'].start=np.min(source3.data['evap_out'])-10000
        g1.extra_y_ranges['second'].end=np.max(source3.data['evap_out'])+10000
        g1.y_range.start=np.min(source.data['output'])-10000
        g1.y_range.end=np.max(source.data['output'])+10000
        g1.xaxis.axis_label="Time (in Months)"
        #g3.xaxis.axis_label="Time (in Months)"
        g4.xaxis.axis_label="Time (in Months)"
        
    elif time=="24 Hours":
        if loc=="Puerto Jiménez, Costa Rica":
            place=Costa_hourly
        elif loc=="Miami, FL":
            place=Miami_hourly
        elif loc=="Quito, Ecuador":
            place=Ecuador_hourly
        elif loc=="Nairobi, Kenya":
            place=Kenya_hourly
        elif loc=="Lusaka, Zambia":
            place=Zambia_hourly
        elif loc=="Bethlehem, PA":
            place=beth_hourly1_C
        dims=[length, width, height, thick]
        out=HC_hourly(place.temps, dims, cond, want_temp)
        vap=[]
        for p in place.temps:
            vap.append(SVP(p))
        water=water_needed_hourly(dims, place.temps, vap, place.rh)
        latent=latent_heat(place.temps)
        evap=evap_cool_hourly(water, latent, time_range)
        T1=T1_calc(dims, place.temps, want_temp, mat, range(0,24))
        dp=dew_point_hourly(place.temps, place.rh, range(0,24))
        
        source.data=dict(time=time_range, output=out)
        sourceW.data=dict(time=time_range, temps=place.temps, water=water)
        source3.data=dict(time=time_range, evap_out=evap)
        sourceDP.data=dict(time=time_range, temps=place.temps, dp=dp, T1=T1)
        g1.extra_y_ranges['second'].start=np.min(source3.data['evap_out'])-10
        g1.extra_y_ranges['second'].end=np.max(source3.data['evap_out'])+10
        g1.y_range.start=np.min(source.data['output'])-10
        g1.y_range.end=np.max(source.data['output'])+10
        g1.xaxis.axis_label="Time (in Hours)"
        #g3.xaxis.axis_label="Time (in Hours)"
        g4.xaxis.axis_label="Time (in Hours)"

def button_updates():
    #Get Slider Values
    length=slide_length.value
    height=slide_height.value
    width=slide_width.value
    mat=select_material.value
    thick=slide_thick.value
    loc=location_select.value
    interval=time_select.value
    place=CostaRica
    dims=[length, width, height, thick]
    water=0
    price=0
    #loc_and_time=["Bethlehem, PA", "Miami, Fl", "Puerto Jiménez, Costa Rica", "Quito, Ecuador", "Nairobi, Kenya", "Lusaka, Zambia"]
    if interval=="12 Months":
        if loc=="Puerto Jiménez, Costa Rica":
            place=CostaRica
        elif loc=="Miami, FL":
            place=Miami
        elif loc=="Quito, Ecuador":
            place=Ecuador
        elif loc=="Nairobi, Kenya":
            place=Kenya
        elif loc=="Lusaka, Zambia":
            place=Zambia
        elif loc=="Bethlehem, PA":
            place=beth_yearly
        vap=[]
        for p in place.temps:
            vap.append(SVP(p))
        water=water_needed(dims, place.temps, vap, place.rh)
        price=cost_calc(dims, sum(water), mat)
        tablePriceY.append("$"+str(round(price, 2)))
        tablePriceD.append("$"+str(round((price/365), 2)))
        tableWaterY.append(str(round(sum(water), 2))+" L")
        tableWaterD.append(str(round(sum(water)/365, 2))+" L")
        
    elif interval=="24 Hours":
        if loc=="Puerto Jiménez, Costa Rica":
            place=Costa_hourly
        elif loc=="Miami, FL":
            place=Miami_hourly
        elif loc=="Quito, Ecuador":
            place=Ecuador_hourly
        elif loc=="Nairobi, Kenya":
            place=Kenya_hourly
        elif loc=="Lusaka, Zambia":
            place=Zambia_hourly
        elif loc=="Bethlehem, PA":
            place==beth_hourly1_C
        vap1=[]
        for p in place.temps:
            vap1.append(SVP(p))
        water=water_needed_hourly(dims, place.temps, vap1, place.rh)
        price=cost_calc(dims, sum(water), mat)
        print(price)
        tablePriceD.append("$"+str(round(price/365,2)))
        tablePriceY.append("$"+str(round(price, 2)))
        tableWaterD.append(str(round(sum(water), 2))+" L")
        tableWaterY.append(str(round(sum(water)*365, 2))+ " L")  
    
    tableName.append(place.location)
    tableSpace.append(str(round((dims[0]*dims[1]*dims[2]), 2))+" m^3")
    tableTime.append(place.time)
    sourceTable.data=dict(name=tableName, time=tableTime, Year_Price=tablePriceY, Day_Price=tablePriceD, Day_Water=tableWaterD, Year_Water=tableWaterY, space=tableSpace)
    
    
#Information that will appear as text paragraphs 
p_Heat=Paragraph(text="Note:    Heat per Time: Displays the heat transferred (from evaporation or conduction) per unit time. The heat conducted refers to the heat transferred from the inner chamber to the water. The evaporative cooling rate refers to the rate of heat leaving the system through evaporation. Water Used: Displays the water needed to keep the system running properly, based off the amount of water evaporating at a given time. A system at steady state needs to release the same amount of what it takes in.", 
                 margin=(20, 10, 20, 10), width=700)
p_ZECC=Paragraph(text="Zero Energy Cooling: By using the principles behind perspiration, there is a way to create an eco friendly chamber for storing food in harsh conditions. The two chamber cooling system consists of two nested chambers, with sand filling the space in between. Water is set to flow in the sand layer. ", 
                 margin=(20, 10, 20, 10), width=700)
p_HT=Paragraph(text="Heat Transfer in the ZECC: The heat transfer that occurs in the zero energy cooling chamber, is a combination of all three of the heat transfer methods. The radiation from solar energy heats the chamber and the surrounding area. The ground also radiates heat. The fluid flow and the conduction of the water is what helps to cool the chamber down.",
               margin=(20, 10, 20, 10), width=700)
p_LHV=Paragraph(text="Latent Heat of Vaporization: When one mole of a substance at atmospheric pressure goes from the liquid phase to the gaseous phase, there is energy required to bring the substance to a boil and make the phase change occur. Bringing a substance to its boiling point is not enough since there is still energy required to make phase change occur. This energy required is the latent heat of vaporization. Temperature changes can’t occur without phase changes.",
                margin=(20, 10, 20, 10), width=700)
p_dp=Paragraph(text="Note:    Dew-Point temperature is critically dependent on both the design of the chamber and inputed values. If the temperature of the outer wall of the chamber becomes too low then water will begin to condense on the surface and no evaporation will occur, halting the cooling process of the inner chamber.", 
               margin=(20, 10, 20, 10), width=700)

widgets=column(location_select, time_select, select_material, slide_length, slide_height, slide_width, slide_thick, slide_desired_temp, calculate_button)
selecters=column(location_select, time_select, select_material)
sliders=column(slide_length, slide_height, slide_width, slide_thick, slide_desired_temp)

tab2=Panel(child=column(row(diff_temps, hourly_temps), row(humid, mapp)), title="Climate Data")
tab1=Panel(child=column(row(selecters, sliders), row(g4, g1), calculate_button, data_table), title="Heat Transfer & Essential Temps")
tab3=Panel(child=column(p_ZECC, p_LHV, p_HT, p_Heat, p_dp), title="Information")
tabs=Tabs(tabs=[tab1, tab2, tab3])

updates=[location_select, time_select, select_material, slide_length, slide_height, slide_width, slide_thick, slide_desired_temp]
for u in updates:
    u.on_change('value', update_data)
    
calculate_button.on_click(button_updates)

curdoc().add_root(tabs)
curdoc().title="Zero Energy Cooling Chamber"






