'''
Generate JSON config file for relationship beetween servo motor and pulse-width modulation (PWM) from XLSX file
'''

import pandas as pd
from sklearn.cluster import KMeans
import json

xls = pd.ExcelFile("servos_pwm.xlsx")
N = 2

out = {}

for sheet in xls.sheet_names:
    data = xls.parse(sheet).to_dict()
    xy = list(zip(list(data['degree'].values()), list(data['pwm'].values())))
    kmeans = KMeans(n_clusters = N)
    kmeans.fit(xy)

    dgr = list(kmeans.cluster_centers_[:, 0])
    pwm = list(kmeans.cluster_centers_[:, 1])
    out[sheet] = {'dgr': dgr, 'pwm': pwm}

with open("servo_pwm_dgr.json", "w") as write_file:
    json.dump(out, write_file, indent=4)