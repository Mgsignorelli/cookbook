# Cookbook


This is the Data Centric Unit Milestone Project, for Code Institute's Full Stack Web Developer Course.
The objective of this project is to create a web application in which users can easily **store and retrieve cooking recipes**. This is constructed on a relational Database, applying the backend coding language Python, and the Flask microframework to create the frontend.

## UX

This website is designed for anyone who enjoys cooking and wishes to have access to a great variety of recipes in only one place with a clear and easy interphase. 
The following wireframe was designed to represent the website skeletal framework.

![Wireframe](public/images/mock.png "Wireframe") 

Prior to the web application creation, a Relational Database was mapped with the PonyORM tools (https://editor.ponyorm.com)

![PonyORM relational database map](public/images/ponydiagram.png "Database Map")


The user of this web application will perform different actions such as Creating a User, Login to their Account and Search for Recipes.   
A user can enter a keyword, choose an ingredient or a category of meal. The resulting recipes are displayed and organized through pagination.

A regular user can only Search the database and vote in Recipes, while a user with Administration permissions can Edit and Delete Recipes, Ingredients, Categories and Allergies.

Recipes can be downvoted or upvoted. They are classified in Categories such as Breakfast, Dessert or Vegan and have an Allergy indicator to ensure safety.



## Features

### Existing Features
- User Creation and login, which allows users to vote.
- Recipe Search
- Voting system
- Admin can Create, Edit and Delete

### Features Left to Implement

## Technologies Used
- HTML language, to write the web page layout. 

- CSS and Sass language to style the application.

- Yarn, JavaScript package manager (https://yarnpkg.com/lang/en/).

- Font Awesome (https://fontawesome.com/)
    Font and Icon toolkit

- Font Google (https://fonts.google.com/)
    Font toolkit.

- Bootstrap 4 (https://getbootstrap.com/docs/4.0/getting-started/introduction/)
    Framework used to uniform the layout. Also, the spacing utils section has been creaated from the information in https://getbootstrap.com/docs/4.1/utilities/spacing/.
    
- Media Queries were used to control the responsive adjustments for smallest screens of the subtitles and paragraphs.

- Slate Bootstwatch was used as a Theme (https://bootswatch.com/3/slate).

- Python, backend language, to create the server of the game application.

- Flask, microframework for the frontend aspect of the application.

- Flask paginate, for pagination implementation.

- PonyORM, Python Object-Relational Mapper.  

- Heroku, for deployment.
    
- Sqlite3, Database engine. 

- TravisCI (https://travis-ci.org/), for automated testing.

- GitKraken (https://support.gitkraken.com/), for management of Branch and Git commits.

- WTF Form Validators (http://wtforms.simplecodes.com/docs/0.6/validators.html), verifying the form input fulfills some criterion.

- Sentry (https://sentry.io/welcome/), platform for monitoring exceptions.

- Select2, (https://select2.org/), jQuery replacement for select boxes.

## Testing

Testing was performed through automated and manual tests. 

- Unit tests were performed on the Recipe Repositories:

    The actions of Create, Read, Update and Delete were tested on each Repository using a test seeder mock database.
    After this, the code in Pony Orm models was refactored in DRY principles and test driven development was carried out.

- Travis CI integration was configured to perform automatic tests.

- 

- This application was extensively tested in different browsers, 
screen sizes and Operative Systems, since it was originally designed in a Mac Desktop.

- Manual Browser testing was performed through acting like a user in the webpage, 
utilizing all the features.

An example of a manual browser test was User creation.

A. User Creation:
  1. In home, go to Register
  2. Submit a user name, longer than three characters
  3. Submit an email address, must be valid.
  4. Submit a password and confirm it.
  5. See a welcome message in the Navbar.
  6. Be allowed to vote a recipe.
  7. Logout link in Navbar

All Create, Read, Update and Delete methods were tested in Recipes, Allergies, Ingredients and Categories. 
All exceptions were handled with Sentry platform.



## Deployment
This project was deployed through Heroku, 
it can be found here: http://winnerwinnerchickendinner.herokuapp.com/

Heroku allows the user to automatically deploy the content pushed to the chosen branch.
Travis CI integration was configured to perform automatic tests before every deployment.
In this case, the deployed branch is the master branch. Development was made in a development branch managed through GitKraken.
Use the following credentials in order to test Admin function

For deployment, the configuration variables were manually set in Heroku Configuration.




## Credits

Recipes sourced from:
- https://www.bbcgoodfood.com/recipes/
- https://itdoesnttastelikechicken.com
- https://www.delish.com



### Media
- The logo image was made by me.

### Acknowledgements

I received inspiration for this project from:
