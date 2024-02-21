import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy import interpolate
from scipy.integrate import cumulative_trapezoid
from array import *
from tkinter import filedialog

#opening file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
numbers = pd.read_excel(file_path)
numbers = pd.DataFrame.transpose(numbers)
values = []

for line in numbers:
    values.append(round(numbers[line][0], 1))

#Histogram and Data Bins
w = .1
bins = np.arange(7.5, 9.5, w)

#Skew Fit
ae, loce, scalee = stats.skewnorm.fit(values)
y = stats.skewnorm.pdf(bins, ae, loce, scalee)

xNew = np.linspace(min(bins), max(bins), 1000)

tck1 = interpolate.splrep(bins, y, s=0, k=1)
fitLineSpline = interpolate.BSpline(*tck1)(xNew)

#Integral Caluclation
integral = cumulative_trapezoid(y, bins, initial=0)

tck2 = interpolate.splrep(bins, integral, s=0, k=3)
yFit = interpolate.BSpline(*tck2)(xNew)

#Finding 1st, 2nd, and 3rd SDs Knife Scores
yFitList = yFit.tolist()
xNewList = xNew.tolist()
lowBound3Sig = 0
lowBound2Sig = 0
lowBound1Sig = 0
median = 0
upperBound1Sig = 0
upperBound2Sig = 0
upperBound3Sig = 0

for item in yFitList:
    if item < .0015:
        lowBound3Sig += 1
    if item < .025:
        lowBound2Sig += 1
    if item < .16:
        lowBound1Sig += 1
    if item < .5:
        median += 1
    if item < .84:
        upperBound1Sig += 1
    if item < .975:
        upperBound2Sig += 1
    if item < .9985:
        upperBound3Sig += 1

#Plotting Data
n, bins, patches = plt.hist(values, facecolor='blue', density=True, edgecolor='black', alpha=.5, bins=bins)
smoothFit = plt.plot(xNew, fitLineSpline, 'r--', linewidth = 1, label = "Best Fit Line")
smoothSpline = plt.plot(xNew, yFit, color = 'orange', label = '% Of Population Below Best Fit')

#Plotting Standard Devations
plt.axvline(x=xNewList[lowBound3Sig], color = 'black', label = "3SD (.15%) = " + str(round(xNewList[lowBound3Sig], 2)))
plt.axvline(x=xNewList[lowBound2Sig], color = 'black', label = "2SD (2.5%) = " + str(round(xNewList[lowBound2Sig], 2)))
plt.axvline(x=xNewList[lowBound1Sig], color = 'black', label = "1SD (16%) = " + str(round(xNewList[lowBound1Sig], 2)))
plt.axvline(x=xNewList[median], color = 'black', label = "Median = " + str(round(xNewList[median], 2)))
plt.axvline(x=xNewList[upperBound1Sig], color = 'black', label = "1SD (84%) = " + str(round(xNewList[upperBound1Sig], 2)))
plt.axvline(x=xNewList[upperBound2Sig], color = 'black', label = "2SD (97.5%) = " + str(round(xNewList[upperBound2Sig], 2)))
plt.axvline(x=xNewList[upperBound3Sig], color = 'black', label = "3SD (99.85%) = " + str(round(xNewList[upperBound3Sig], 2)))

#Labels and Such
plt.xticks(bins)
plt.xlabel('Knife Score (Anago KS)')
plt.ylabel('Number Of Knives (Normalized)')
plt.title('Knife Scores')
plt.legend()
plt.show()
