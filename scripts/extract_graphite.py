import requests
import pandas as pd

date_start = "10:40_20221022"
date_stop = "18:50_20221103"

variables = {
	"rackA16.PSUB.power" : "Top PSU power",
	"rackA16.PSUB.temp" : "Top PSU temp",
	"rackA16.ShelfB.power" : "Top Meter power",
	"rackA16.PSUA.power" : "Bottom PSU power",
	"rackA16.PSUA.temp" : "Bottom PSU temp",
	"rackA16.ShelfA.power" : "Bottom Meter power",
	"rackA16.sensors.flow" : "Water flow",
	"rackA16.sensors.rtd1" : "Air loop temp",
	"rackA16.sensors.t": "Hall air temperature",
	"rackA09.sensors.temperature" : "USB air temperature",
	"rackA16.sensors.rtd4" : "Outlet pipe temperature",
	"rackA16.sensors.rtd3" : "Inlet pipe temperature",
	"rackA16.ShelfA.fantray.LowerCenter" : "Bottom inlet temp center",
	"rackA16.ShelfA.fantray.LowerLeft" : "Bottom inlet temp left",
	"rackA16.ShelfA.fantray.LowerRight" : "Bottom inlet temp right",
	"rackA16.ShelfA.fantray.UpperCenter" : "Bottom outlet temp center",
	"rackA16.ShelfA.fantray.UpperLeft" : "Bottom outlet temp left",
	"rackA16.ShelfA.fantray.UpperRight" : "Bottom outlet temp right",
	"rackA16.ShelfB.fantray.LowerCenter" : "Top inlet temp center",
	"rackA16.ShelfB.fantray.LowerLeft" : "Top inlet temp left",
	"rackA16.ShelfB.fantray.LowerRight" : "Top inlet temp right",
	"rackA16.ShelfB.fantray.UpperCenter" : "Top outlet temp center",
	"rackA16.ShelfB.fantray.UpperLeft" : "Top outlet temp left",
	"rackA16.ShelfB.fantray.UpperRight" : "Top outlet temp right",
	"rackA16.ShelfA.localtemp" : "Bottom shelf manager temp",
	"rackA16.ShelfB.localtemp" : "Top shelf manager temp",
	"rackA16.ShelfA.PEMA" : "Bottom PEM A temp",
	"rackA16.ShelfA.PEMB" : "Bottom PEM B temp",
	"rackA16.ShelfB.PEMA" : "Top PEM A temp",
	"rackA16.ShelfB.PEMB" : "Top PEM B temp",
	"serenityM.IPMC.X0FPGATEMP" : "SerenityM X0 temp",
	"serenityM.IPMC.X1FPGATEMP" : "SerenityM X1 temp",
	"serenity13.IPMC.X0FPGATEMP" : "Serenity13 X0 temp",
	"serenity13.IPMC.X1FPGATEMP" : "Serenity13 X1 temp",
        "rackA09.sensors.condensation_NO" : "Condensation sensor",
        "rackA09.sensors.dew_point" : "Dew point",
	"rackA09.sensors.pressure" : "Atm pressure",
	"rackA09.sensors.RH" : "Relative humidity",
	"rackA09.cooling.valveopening" : "Valve opening",
	"rackA09.cooling.inletwatertemp" : "Inlet water temp",
	"rackA09.cooling.outletwatertemp" : "Outlet water temp",
	"rackA09.cooling.setwatertemp" : "Set water temp"
}


variable = "rackA16.PSUB.power"
rack_df = pd.DataFrame()
for variable in variables:
	base_url = f"http://localhost/render/?target=summarize({variable},'20minute','last')&from={date_start}&until={date_stop}&format=json"
	r = requests.get(base_url)
	temp = pd.DataFrame(data=r.json()[0][u'datapoints'], columns=[variables[variable],"Time"])
	if len(rack_df.index)==0 :
		rack_df = temp
	else:
		rack_df = pd.merge(temp, rack_df, on="Time")

print(rack_df[["SerenityM X0 temp","Serenity13 X0 temp","Bottom inlet temp center","Bottom inlet temp left","Bottom inlet temp right"]])
print(rack_df)
rack_df.to_pickle(f"rack_thermal_df_{date_start}_{date_stop}a.pkl")
