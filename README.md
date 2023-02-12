# Candy crush
### Running the game
The game must be run with python 3.9

If running on Windows and not using venv make sure you have installed Visual Studio Build Tools 2019
and also included 'Desktop development with C++' workload with Visual C++ compiler<br/>
You can install Build Tools from: 
https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16

After installing the requirements.txt packages start the game from main.py

### Modifying the levels
In the levels.txt file each line represents a level in the following format:
<game_moves> <required_score> <required_tiles for each color> 

If score or any of the gems is not required write -1