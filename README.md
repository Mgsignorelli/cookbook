# Cookbook


This is the Data Centric Unit Milestone Project, for Code Institute's Full Stack Web Developer Course.
The objective of this project is to create a web application in which users can easily store and retrieve cooking recipes. This is constructed on a relational Database, applying the backend coding language Python, and the Flask microframework to create the frontend.

## UX

This website is designed for anyone who enjoys cooking and wishes to have access to a great variety of recipes in only one place. Recipes can easily be read in a friendly, simple and clear interphase.
The user of this web application will perform different actions such as Creating a User, Login to their Account, Search for recipes or Submit their own recipes to the cookbook. Recipes are classified in Categories such as Breakfast, Dessert or Vegan. Recipes have an Allergy indicator to
ensure safety. 

*User Stories were used for Behavior-Driven Development, such as:*
*- As a user, I am looking for a Recipe, I click on a link from the main menu and select a recipe for viewing.*


## Features

### Existing Features
- User Creation: A visitor is prompted to register a user before creating or editing a recipe, with the objective of content monitoring and enabling voting functionality.
- Login, which allows said storage of data for the user score to be displayed in the Leaderboard.
- There are currently  Recipes. 
- Submit a Recipe, where the User is allowed to add a Recipe to the game.
- Recipes also have a voting system, the User can press a thumbs up or down button, enabling sorting by the most popular recipes.

### Features Left to Implement

## Technologies Used

- Python, backend language, to create the server of the game application.

- Flask, microframework for frontend.

- PonyORM, Python Object-Relational Mapper.  
    
- Sqlite3, Database engine. 

- TravisCI (https://travis-ci.org/). for automated testing.

- HTML language, to write the web page layout. 

- CSS language to style the application.

- Font Awesome (https://fontawesome.com/)
    Font and Icon toolkit

- Font Google (https://fonts.google.com/)
    Font toolkit.

- Bootstrap 4 (https://getbootstrap.com/docs/4.0/getting-started/introduction/)
    This framework was used for responsiveness of the site 

- GitKraken (https://support.gitkraken.com/), for management of Branch and Git commits.



*- Flake (http://flake8.pycqa.org/en/latest/index.html#quickstart) 
    For validation of Python code.*

## Testing

Testing was performed through automated and manual tests. 

- Validity of Python code was tested through Flake. 

- Unittests were performed on the Recipe Repositories, 
the actions of Create, Read, Update and Delete were tested on each Repository.

- This application was extensively tested in different browsers, 
screen sizes and Operative Systems, since it was originally designed in a Mac Desktop.

- Manual Browser testing was performed through acting like a user in the webpage, 
utilizing all the features.


An example of a manual test was User creation.
1. User Creation:
    1. Go to Home page
    2. Submit a user name
    3. Submit an email address, must be valid.
    4. Submit a password and confirm it
    5. See a welcome message in the Navbar
    6. Be allowed to submit a recipe
    7. Logout with Logout link+icon in Navbar



## Deployment
This project was deployed through Heroku, 
it can be found here:

Heroku allows the user to automatically deploy the content pushed to the chosen branch.
In this case, the deployed branch is the master branch. Development was made in a development branch managed through GitKraken.

The submitted and deployed versions are identical. 

*For deployment, the configuration variables were manually set in Heroku Configuration.*




## Credits

Recipes sourced from:
*- https://www.everythingmom.com/parenting/45-riddles-and-brain-teasers-for-kids*
*- https://www.riddles.com/best-riddles*
*- https://icebreakerideas.com/riddles-for-kids/*
*- https://riddles.fyi/page/*
*- http://brainden.com/logic-riddles.htm*

### Media
- The logo image was made by me.

### Acknowledgements

I received inspiration for this project from: