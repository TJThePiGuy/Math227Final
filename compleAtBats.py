import csv
import pickle
yearData:dict[int,dict[str,list[str]]] = dict()

for year in range(2002, 2024):
    plateAppearances:dict[str,list[str]] = dict()

    players:list[str] = []
    with open(f'playerData/{year}.csv','r') as playerFile:
        playerData = csv.DictReader(playerFile)
        for row in playerData:
            plateAppearances[(row['IDrs'])] = []

    with open(f'rawRetroData/{year}eve/{year}.csv', 'r',) as eventFile:
        eventReader = csv.reader(eventFile)
        for line in eventReader:
            if line[8] in plateAppearances.keys():
                plateAppearances[line[8]].append(line[5])
    
    yearData[year] = plateAppearances

with open('allPlayer.pickle', 'wb') as f:
    pickle.dump(yearData, f, pickle.HIGHEST_PROTOCOL)