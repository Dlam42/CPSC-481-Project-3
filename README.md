# CPSC-481-Project  Disappearing Tic-Tac-Toe
This project is a modern twist on the classic Tic-Tac-Toe game, developed as part of the CPSC 481 course. In this version, player's mark Black Puppy and AI's mark Orange Cat disappear three turns after being placed, starting once that player has made their fourth move. This mechanic introduces a dynamic and strategic element to the traditional game.

## Features

- Classic 3x3 Tic-Tac-Toe grid
- Disappearing marks: Each mark vanishes three turns after placement, post the player's third move
- Turn tracking and win detection ( No draw in this game)
- Reset functionality to start a new game
- Web-based interface accessible via browser


## Setup Instructions

1. Clone the repository:
```bash
git clone (https://github.com/Dlam42/CPSC-481-Project-3.git)
cd src
```

2. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source ./venv/Scripts/activate
     ```
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python app.py
```


The application should now be accessible at http://localhost:5000.

## Deployemnt
The application is deployed on 
https://cpsc-481-project-3.onrender.com/

## Future Enhancements
- Animations: Add visual effects for disappearing marks.

- Responsive Design: Enhance UI for better experience on various devices.

- User Authentication: Allow users to log in and track their game history.

## License
This project is open-source and available under the MIT License.

