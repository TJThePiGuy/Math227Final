import csv
import pickle
import random as r
import statistics as stats
import tqdm


def swingingPitch(zone, zSwing, swing):
    return r.random() < zone * zSwing / swing


def pitchInZone(zone) -> bool:
    return r.random() < zone


def simulateAtBat(sequence: str, oSwing, zSwing, swing, zone) -> bool:
    balls = 0
    strikes = 0
    for pitch in sequence:
        if pitch == "H":
            return True
        if pitch in "BIPVY":
            balls += 1
        elif pitch in "AC":
            strikes += 1
        elif pitch in "UK":
            if pitchInZone(zone):
                strikes += 1
            else:
                balls += 1
        elif pitch in "FLMOQRSTX":
            if swingingPitch(zone, zSwing, swing):
                strikes += 1
            else:
                balls += 1

        if balls >= 4:
            return True
        elif strikes >= 3:
            return False

    while True:
        if pitchInZone(zone):
            strikes += 1
        else:
            balls += 1

        if balls >= 4:
            return True
        elif strikes >= 3:
            return False


with open("allPlayer.pickle", "rb") as playerFile:
    allYearData = pickle.load(playerFile)

maxSims = 1000

headers = [
    "Year",
    "Name",
    "IDrs",
    "At-Bats",
    "AVG",
    "OBP",
    "SLG",
    "Mean Sim OBP",
    "Max Sim OBP",
    "Min Sim OBP",
    "Sim OBP Std. Dev",
    "Mean Change",
]

with open("sims\\allSims.csv", "w", newline="\n") as everyYearFile:
    everyYearWriter = csv.DictWriter(everyYearFile, headers, dialect=csv.excel_tab)
    everyYearWriter.writeheader()
    for YEAR in range(2002, 2024):
        if YEAR == 2020:
            continue
        currentYearData = allYearData[YEAR]

        with open(f"playerData\\{YEAR}.csv", "r") as playerFile, open(
            f"sims\\{YEAR}.csv", "w", newline="\n"
        ) as simsFile:
            playerDataReader = csv.DictReader(playerFile)
            simsDataWriter = csv.DictWriter(simsFile, headers, dialect=csv.excel_tab)
            playerDataList = list(playerDataReader)
            allYearDicts = []

            for playerData in tqdm.tqdm((playerDataList)):
                IDrs = playerData["IDrs"]

                actualOBP = playerData["OBP"]
                avg = playerData["AVG"]
                slg = playerData["SLG"]

                oSwing = float(playerData["O-Swing%"])
                zSwing = float(playerData["Z-Swing%"])
                swing = float(playerData["Swing%"])
                zone = float(playerData["Zone%"])
                name = playerData["Name"]

                playerData = dict()
                playerData["Year"] = YEAR
                playerData["Name"] = name
                playerData["IDrs"] = IDrs
                playerData["OBP"] = actualOBP
                playerData["AVG"] = avg
                playerData["SLG"] = slg

                sequences = currentYearData[IDrs]
                atBats = len(sequences)
                sims = []
                for sim in range(maxSims):
                    walks = 0
                    for sequence in sequences:
                        walks += int(
                            simulateAtBat(sequence, oSwing, zSwing, swing, zone)
                        )
                    sims.append(walks)

                avgWalks = stats.mean(sims)
                maxWalks = max(sims)
                minWalks = min(sims)
                playerData["At-Bats"] = atBats

                avgOBP = avgWalks / atBats
                maxOBP = maxWalks / atBats
                minOBP = minWalks / atBats

                playerData["Mean Sim OBP"] = avgOBP
                playerData["Max Sim OBP"] = maxOBP
                playerData["Min Sim OBP"] = minOBP
                playerData["Mean Change"] = avgOBP - float(actualOBP)
                playerData["Sim OBP Std. Dev"] = stats.stdev(sims) / atBats
                # print(YEAR, name)
                allYearDicts.append(playerData)
            simsDataWriter.writeheader()
            simsDataWriter.writerows(allYearDicts)
            everyYearWriter.writerows(allYearDicts)
