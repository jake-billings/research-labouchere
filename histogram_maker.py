# This utility script helps generate histogram data based on the contents of a CSV
# It is intended as a post-processing tool from CSV data dumped from strategy_bankroll.py.


INPUT_FILE = 'export_2.csv'
OUTPUT_FILE = 'export_histogram.csv'

data = []
with open(INPUT_FILE, 'r') as file:
    lines = file.readlines(10000000)
    for line in lines:
        data.append(float(line.split('\n')[0]))

data_min = min(data)
data_max = max(data)

print "min", data_min
print "max", data_max
print "length", len(data)

intervals=10
interval_size=(data_max-data_min)/intervals

print "interval size", interval_size

output = [['min','max','count']]

for i in range(0,intervals):
    data_in_interval = []

    interval_min = i * interval_size + data_min
    interval_max = (i+1) * (interval_size) + data_min
    count = 0

    for datum in data:
        if datum > interval_min and datum < interval_max:
            count += 1

    output.append([interval_min, interval_max, count])

print output

with open(OUTPUT_FILE, 'w') as wfile:
    for row in output:
        for cell in row:
            wfile.write(str(cell)+', ')
        wfile.write('\n')