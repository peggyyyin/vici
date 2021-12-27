# The Vici Design Document
This document is organized as follows:
(1) app.py
(2) templates (i.e. html documents: dashboard, homepage, layout, login_layout, register, rewards, wish)
(3) static (i.e. css sheets: homepage, styles)

## app.py
I will discuss my implementation and design decisions in app.py by function, from top to bottom. Much of this implementation involves the creation and manipulation of SQL tables, which allowed for efficient and flexible storage of the ever-changing lists of tasks and wishes.

The SQL tables are organized as follows (each table is linked together by (user) id):

users (id INTEGER, username TEXT NOT NULL, hash TEXT NOT NULL, PRIMARY KEY (id));

tasks (id INTEGER, task TEXT, priority INTEGER, time INTEGER, urgency INTEGER, importance INTEGER, datetime DATETIME);

rewards (id INTEGER, wish TEXT);

conquered (id INTEGER, task TEXT, time_remaining INTEGER, datetime DATETIME);

users contains the login information for each user. tasks containts the backlog information for each task, as well as when the task was submitted to the form. rewards contains the wishlist. conquered contains the list of completed tasks.

These tables are organized this way such that each page/section of the web application uses one of these tables for ease of access and quicker computation time.

### login_required
The code for this function was adapted from the Finance problem set. I included this function to ensure that in order to use the web application, users would need to have an account. This would allow for information to be saved by user.

### time_left
This function calculates the time remaining between the deadline and the present date. The use of datetime.datetime.now() when implementing the function allows for dynamic calculation of time_left.

### home
The intention was for the homepage (i.e. "Now") to be as minimalistic as possible, and focused on one task. This was achieved through a dropdown menu that would force the user to select one task to focus on conquering. The black background contrasts with the neon green button and white dropdown menu to really focus the user on the task at hand.

I used this dropdown menu as a method to track tasks as they were completed, and created a table of completed (conquered) tasks. 

This dropdown menu was sorted in prioritized order using the ORDER BY priorty SQL keywords.

### login
The code for this function was adapted from the Finance problem set. This is the first page not-logged-in users see as login is required to access all other pages (except for registration).

Since I made all the form fields required, I did not need to ensure the username and password spaces were filled out. I did, hoewver, want to let the user know if they entered an incorrect username or password.

After entering a correct username/password pairing, the user would be redirected to the home page, where they can see their prioritized tasks.

### register
Register may only be accessed via the "I don't have an account yet" hyperlink in the login form. The reason for this is that users, once registered, will never need to register again, so it would not make sense for register to appear on the navbar and crowd the interface.

The code for this function was adapted from the Finance problem set. I wanted to ensure that each user was registering with a unique username, so I included the querying of the database for the desired username prior to allowing a user to register. I also made sure to store passwords in the form of hashes for added security measures.

Register directs you to login after registering, so users may then log in with their newly created acccount.

### logout
The code for this function was adapted from the Finance problem set. The logout function effectively logs the user out so their information is no longer displayed on the website.

### urgent_display and importance_display
These two functions exist for aesthetic reasons. When the task form in Dashboard is submitted, depending on which urgency and importance level was assigned to each task, the urgency and importance values will be some number 0, 1, 2, 100, which makes it easier to numerically calculate a priority score. However, if these numbers were displayed as entries in the Backlog and Editing table in Dashboard, they wouldn't have much meaning to the standard user. So we replace these numbers with exlamation points (!) corresponding to the urgency level (e.g. !! is Urgent) and smiley-face emojis corresponding to the importance level (e.g. Important is :)).

### priority and priority_display
These two functions calculate the priority score of a task (priority) and then replace that score with a more semantically-friendly version of the priority the task should be given according to the priority funciton (priority_display), respectively. This function was determined by examining a sample of my own tasks, and then changing the weights and "milestones" of the function accordingly until the priority labels corresponded to my own perception of the priority levels of the sample tasks. 

The label "just do it" indicates the user should perform the associated task as soon as possible. The label "up next" indicates the task will become "just do it" after the "just do it" tasks have been completed. The "radar" label is there to help users know when they should keep tasks on their radar but not prioritize them so they can complete their more urgent and important tasks first.

#### Note on future work for the priority function
Different users may have different preferences for the relative weights of the urgency, importance, and time-left-until-deadline metrics. This should be taken into account via a more flexible priority funciton unique to each user's preferences. I would also like to include more metrics in future priority functions, e.g. time estimates for how long the task may take.

### dashboard
The Dashboard receives the user's tasks input and displays a table of their inputted tasks. This keeps all editing and task-logging in one place. Any time a task is inserted into the SQL table, the task name is added to the dropdown menu under the Backlog and Ediitng section; that way users can quickly delete and modify the backlog themselves.

### rewards
The rewards function receives the user's wishlist, allows the user to grant themselves their wishes, and displays the log of the user's completed tasks. This is accomplished through two separate SQL tables: one that tracks rewards and one that tracks completed tasks. The decision to separate the tables from each other and from tasks was fueled by the visualization consideration. I wanted to visualize a table of unfinished tasks in Dashboard, a table of completed (conquered) tasks in rewards, and a wishlist in a dropdown menu. These three separate visualizations were more easily accomplished by three separate tables than one (or even two) mega-table(s).

#### Note on future work for the rewards function
In the future, I plan to make the Wishing Well a page that will only pop up when the future reinforcement scheduler determines it is time for a reward.

### future functions
In the future I hope to define reinforcement schedule functions that will determine when the user is rewarded with one wish granted (e.g. granting a wish once every three completed tasks would be a fixed-ratio reinforcement schedule).

## templates
Inside the /templates directory are html documents dashboard, homepage, layout, login_layout, register, rewards, and wish. layout.html and login_layout.html are both templates for the rest of the documents; layout.html is the template for dashboard.html, rewards.html, wish.html; login_layout is the template for login.html and register.html. Homepage.html does not use a template.

The reason for these page-template pairings is aesthetic. I wanted login and register to look almost the same (the difference being login would have a login button and register a register button). I wanted the dashboard, rewards, and wish to look similar because of the already similar structure in design elements (e.g. dropdown menus, tasks). Grouping the templates the way I did allowed for those aesthetic choices to happen.

Both templates were designed with simplicity in mind. The login_layout template focused the user's attention on filling out the login/register form since there was nothing else to look at on the page. Similarly, the Vici interface templated on layout.html only includes necessary design elements.

The pages and their design elements also were chosen in a way that allowed the user to fill out forms in a natural order from top to bottom. For example, in order to delete tasks, users had to enter tasks first. Thus, the entering tasks portion of the Dashboard was above the deleting tasks portion.

### Note on wish.html
wish.html is an example of what the future secret (i.e. hidden) Wishing Well page would look like. The page would automatically "vanish" (i.e. redirect) to /rewards after the user grants themselves one wish based on a reinforcement schedule.

## static
Inside the /static directory are the css style sheets homepage.css and styles.css. homepage.css is the stylesheet for homepage.html and layout.html (which, through templating, means it is also the stylesheet for dashboard.html, rewards.html, wish.html). styles.css is the stylesheet for login_layout.html (which, through templating, means it is also the stylesheet for login.html and register.html).

The splitting of style sheets made sense because the login and register pages are supposed to be transitory screens—"gateways"—to the actual site. So therefore they have a slightly different aesthetic from the site itself. The uniform css of the pages other than login and register also made sense because they were all part of a single, uniform site experience. Therefore, it follows that the color scheme, hover effects, text color, etc. should stay consistent.

The color scheme of black/black-ish gradent as a background color, greenyellow as an accent, and white as the text color was deliberately chosen so that all the colors would stand in stark contrast with each other, yet look clean and minimalist together. The dark background ensures that the focus is on the text and buttons. The white text against the black ensures that tasks are easy to read. The greenyellow accents add a flair to entering tasks, completing them, and then having a wish granted. The green is also present to symbolize good productivity. 