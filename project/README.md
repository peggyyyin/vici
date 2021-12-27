# Vici: Conquer your Life!
Conquer your life! Vici is a web application that aims to employ research-based methods on conscientiousness, intrinsic motivation, and implicit theories to inspire users to be proactive, productive, and passionate. The simplicity of Vici's interface ensures users not only see their goals, but also make consistent progress towards achieving them, vanquishing procrastination as easily as "veni, vidi, vici."

## Notes on the Minimum Viable Product and Vision
This edition of Vici is the minimum viable product, and features the core of Vici's functionality: task-tracking, task prioritization, a focused and clean interface, goal-oriented rewards, and goal-oriented decision-making. Currently, Vici's prioritization is based on the Eisenhower matrix method. In the future we hope to expand this metric by incorporating more productivity methods. Vici also presently depends on the user to self-regulate their rewards. In the future, Vici will automate the process by employing different reinforcement schedules (e.g. fixed-ratio, variable-ratio) to automate the reward process.

## Link to YouTube Video
https://youtu.be/shszooZySAw

# User Manual
Vici was constructed using VSCode. It may be run locally.

The order in which a user should access the pages upon first using the website is:
(1) Dashboard (to input tasks)
(2) Rewards (to input wishlist)
(3) Now (to conquer tasks)

## Software and Configuration
Vici uses Python 3.10, sqlite3, flask, flask-session, and the cs50 library. Please import these packages prior to running Vici. The web application may then be run locally from VScode via command flask run. You may need to export the flask app and set up an environment prior to flask run.

## Register/Log in
To access any of the pages, the user must first register, or log in if they already have an account. If you are a new user, please click the "I don't have an account yet" hyperlink at the bottom of the login form. Once you log in, you'll see the "Now" homepage. This is where your tasks will be listed, in prioritized order, once you enter the tasks into your Dashboard. You may log out by clicking "logout" at the bottom of every page in the site.

## Dashboard
This is where you will enter your tasks and assign an urgency and importance value to them. Urgency is defined as how much is riding on completion of the task (i.e. how much trouble you will be in if you don't complete said task), and importance is defined as the personal meaning completion of the task has to you. For example, taking out the trash may be rated as "Urgent" and "Kind of Important". Writing a philosophy paper due tomorrow that you are deeply passionate about would be rated as "AHHHHH" and "I burn with passion." You will also enter how far away the deadline is. The time left until the deadline, urgency, and importance of the task are the three metrics currently used to determine the priority ranking.

After submitting the task form for each task, you may view all your tasks in the Backlog and Editor table also on the Dashboard page. Note that in the importance column anything that you inputted as "Not Important" will have a "Why?" entry. It is recommended that you reflect on why you have this task listed on your to-do if it is not important to you. Similarly, anything inputted as "Not Urgent" will have a "push" entry. This means that you should either delegate, cancel, or reschedule this task. 

If you would like to delete a task at any time, simply select that task from the dropdown menu and delete it. 

# Now
Now when you go back to the homepage, i.e. "Now", you will see a dropdown list of all your tasks listed in prioritized order. It is highly recommended that you complete the tasks in this order. When you are done completing a task, select that task from the dropdown menu and hit the "Conquered!" button. (Optional: a happy dance to celebrate!)

## Rewards
The Rewards page features a Motivation Station, a Wishing Well (i.e. a wish granter), and a conquest log featuring how much time left you had when you completed them and the date you completed the task. At the Motivation Station, you may input as many of your wishes as you would like. These are your rewards for finishing work so choose wisely. Once you complete tasks, you may then allow yourself to grant those wishes from the dropdown menu.

The log of your conquered tasks is there for statistical purposes. You may use it to track your productivity (and procrastination).

### Note on future work
In the future, I plan to make the Wishing Well a page that will only pop up when the future reinforcement scheduler determines it is time for a reward. The time left before deadline at the point the task is completed may also be a metric towards how quickly the user is rewarded.