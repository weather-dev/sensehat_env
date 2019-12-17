import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import datetime as dt

file_date = "2019-12-15"

file_name = "csvFiles/CSVfile_{}.csv".format(file_date)
df = pd.read_csv(file_name)
df["Timing"] = pd.to_datetime(df["Unix"], unit="s")
#analysed = pd.DataFrame.describe(df[["Average temp", "Pressure", "Humidity"]])
#print(analysed)

plt.style.use("ggplot")

def plot_timeseries(axes, x, y, color, marker, xlabel, ylabel, linestyle = "-"):
    axes.plot(x, y, color=color, marker=marker, linestyle=linestyle)
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel, color=color)
    axes.tick_params("y", colors=color)
    for label in axes.xaxis.get_ticklabels():
        label.set_rotation(50)
    
def plot_all():
    fig, ax = plt.subplots(3,1, sharex=True)
    print(pd.DataFrame.mean(df[["Average temp", "Pressure", "Humidity"]]))
    plot_timeseries(ax[0], df["Timing"], df["Humidity"], "blue", "v", None, "Humidity (%)",  "None")
    plot_timeseries(ax[1], df["Timing"], df["Average temp"], "red", ".", None, "Temperature (C)", "None")
    plot_timeseries(ax[2], df["Timing"], df["Pressure"], "black", "x", "Time (MM-DD HH)", "Pressure (hPa)", "None")
    plt.tight_layout()
    fig.show()

def plot_all_temperature():
    fig1, ax1 = plt.subplots()
    print(pd.DataFrame.mean(df[["Average temp"]]))
    plot_timeseries(ax1, df["Timing"], df["Average temp"], "red", ".", "Time (MM-DD HH)", "Temperature (C)", "None")
    plt.tight_layout()
    fig1.savefig("./figures/Temperature_{}.png".format(file_date), dpi=600)

def plot_all_Rhumidity():
    fig2, ax2 = plt.subplots()
    print(pd.DataFrame.mean(df[["Humidity"]]))
    plot_timeseries(ax2, df["Timing"], df["Humidity"], "red", ".", "Time (MM-DD HH)", "Humidity (%)", "None")
    plt.tight_layout()
    fig2.savefig("./figures/Humidity_{}.png".format(file_date), dpi=600)

def plot_all_pressure():
    fig3, ax3 = plt.subplots()
    print(pd.DataFrame.mean(df[["Pressure"]]))
    plot_timeseries(ax3, df["Timing"], df["Pressure"], "red", ".", "Time (MM-DD HH)", "Pressure (hPa)", "None")
    plt.tight_layout()
    fig3.savefig("./figures/Pressure_{}.png".format(file_date), dpi=600)

def plot_save_all():
    plot_all_Rhumidity()
    plot_all_temperature()
    plot_all_pressure()

plot_save_all()