import csv
import numpy as np
import pandas as pd
import seaborn as sns
import simplejson as json
import matplotlib.pyplot as plt

# Load data
xls_file = pd.ExcelFile('./data/GDP.xls')
table = xls_file.parse('Sheet1').T

# Exclude country aggregates
table.pop('Euro area')
table.pop('OECD total')

# Compute the correlation matrix
corr = table.corr(method='pearson')
countries = corr.shape[0]
countryList = corr.index

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(12, 12))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(10, 220, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, cmap=cmap, vmax=1, square=True, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
plt.title('Correlations of annual GDP growth in percent 1991-2004', fontsize=16)
plt.savefig('correlations.png', bbox_inches='tight')

# Save correlations for Javascript visualization
f = f = open('correlations.json', 'w')
f.write('[\n')
for country in range(countries):
    f.write('{"name":"' + corr.index[country].replace(' ', '_') + '","connections":{')
    for c in range(countries):
        if c == country: continue
        f.write('"' + countryList[c].replace(' ', '_') + '":"' + str(corr[countryList[country]][countryList[c]]) + '"')
        if c < countries - 1 and country < countries - 1:
            f.write(',')
        elif c < countries - 2 and country == countries - 1:
            f.write(',')
    endStr = '}}'
    if country < countries - 1:
        f.write(endStr + ',\n')
    else:
        f.write(endStr)
f.write('\n]\n')
f.close()
