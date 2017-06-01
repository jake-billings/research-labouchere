# Exports each key value pair as a row in a csv file
def export_dict_as_csv(d, name='export.csv'):
    with open(name, 'w') as wfile:
        for key in d:
            wfile.write(str(key)+','+str(d[key])+'\n')
