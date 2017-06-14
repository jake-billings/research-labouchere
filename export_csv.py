# Copyright (c) 2017 [Jake Billings]
# See LICENSE for more information


# Exports each key value pair as a row in a csv file
def export_dict_as_csv(d, name='export.csv'):
    with open(name, 'w') as wfile:
        for key in d:
            wfile.write(str(key)+','+str(d[key])+'\n')


# Exports a 2D array as a csv file
def export_array_as_csv(d, name='export.csv'):
    with open(name, 'w') as wfile:
        for row in d:
            for cell in row:
                wfile.write(str(cell)+',')
            wfile.write('\n')
