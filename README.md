# Math 227 Final

This is my final for Math 227: Mathematical Modeling at NJIT. The following is a list of some of the folders and files of this repository:

- [rawRetroData](rawRetroData) - folders used to store Retrosheet data. Inside each folder is the csv file containing all player events in that season. While I cannot share the raw Retrosheet data in its entirety, you can find all seasons at [https://www.retrosheet.org/](https://www.retrosheet.org/).
- [getPlayerData](getPlayerData.py) - compiles all player data and saves it to the csv viles located in [playerData](playerData).
- [compileAtBats](compileAtBats.py) - compiles all at-bats for each year and saves all the data to a pickle file for ease of use
- [simulateAtBats](simulateAtBats.py) - simulates all at-bats in the pickle file.
- [graphs](graphs.mlx) - live MATLAB script used to generate the graphs in my project
