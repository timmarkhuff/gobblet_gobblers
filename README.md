# Gobblet Gobblers

Based on the game Gobblet Gobblers: https://themindcafe.com.sg/wp-content/uploads/2018/07/Gobblet-Gobblers.pdf

A short video introduction to this project is available here: https://youtu.be/0lpivm_qItg

My version of Gobblers has six unique piece sizes, whereas the traditional version only has 3. 

* logic.py: contains a Game object that tracks the game state and logic
* cli.py: playable version of the game at the command line interface. Can be played human vs human, human vs bot and bot vs bot
* gui.py: playable version of the game with a graphical user interface. Human players only. Requires OpenCV
* tests.py: some unit tests written with the unittest module
* app.py: uses Flask and Jinja to run the game in a browser locally

<img src="https://user-images.githubusercontent.com/89954856/201192702-ecb25f19-eb86-4cc8-a422-227e1c84f882.png" width="450">
<img src="https://user-images.githubusercontent.com/89954856/201192715-bf97b770-e953-4255-a592-850f30be8ca9.png" width="450">

## Updates for Week 10 - Lab Submission 
* added app.py to run the game in a browser via Flask
<img src="https://user-images.githubusercontent.com/89954856/208316396-a86602b3-da86-4ba7-874a-b5a7e6657180.png" width="450">
<img src="https://user-images.githubusercontent.com/89954856/208316573-15a6b6f8-0d47-4fed-bedc-66e3cc767ba4.png" width="450">
<img src="https://user-images.githubusercontent.com/89954856/208316991-68d65501-2e95-4acb-98f8-abc50367ec56.png" width="450">

## Updates for Week 9 - Lab Submission 
* added index.html as the homepage of the game
* added play.html as the UI for an online playable version of the game
* added stats.html to show some game stats at the end of each game
* added styles.css to add styling to the aforementioned html pages
<img src="https://user-images.githubusercontent.com/89954856/206042749-9f4dca6f-fb8b-4e12-a3a6-dbbc2e653409.png" width="450">
<img src="https://user-images.githubusercontent.com/89954856/206042832-9694c475-a1a1-42f5-85c5-77d0a3e1abda.png" width="450">
<img src="https://user-images.githubusercontent.com/89954856/206042916-1ae898b0-a64d-4859-ba7b-f3755e87b45a.png" width="450">

## Updates for Week 8 - Lab Submission 
* In logic.py, GameStats class was added to keep track of statistics
* In gui.py, several methods were added to Board class to generate charts from statistics generated by GameStats class
* Pandas and Matplotlib are used to handle stats and produce charts. The final GUI is generated with OpenCV
* Run gui.py to see the results

<img src="https://user-images.githubusercontent.com/89954856/204674269-c66fdf71-ed73-4e59-a353-b3589366e4c8.png" width="450">
<img src="https://user-images.githubusercontent.com/89954856/204674294-b47e57db-6e77-495f-b8db-2f9f40336bf0.png" width="450">
<img src="https://user-images.githubusercontent.com/89954856/204676337-83b04674-3f97-47c8-9262-e84a5f9c4ab0.png" width="450">
