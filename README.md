# Restaurant Kitchen Service

## Table of contents
- [Description](#description)
    - [Features](#features)
    - [Database structure](#database-structure)
    - [Web pages](#web-pages)
      - [Accounts pages](#accounts-pages)
      - [Error pages](#error-pages)
      - [Dish type pages](#dish-type-pages)
      - [Ingredient pages](#ingredient-pages)
      - [Dish pages](#dish-pages)
      - [Cook pages](#cook-pages)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

## Description
This project is designed using Flask and its extensions to manage all information related to dishes.
### Features:
- Create and update dish types, ingredients, dishes and cooks (as moderator/admin);
- Delete dish types, ingredients, dishes and cooks (as admin);
- View list with dish types, ingredients, dishes and cooks with pagination and search (as user/moderator/admin);
- View detail with dishes and cooks;
- Adding and deletion current user from dish;
- Custom admin panel - via `/admin/` (as admin);
- User registration and log in simultaneously;
- Log in and log out;
- Change current user password;
- Custom cli commands - `create_admin` and `change_password`.

### Database structure:
Below is illustrated the project database structure (for more details follow this [link](https://dbdiagram.io/e/6af63ae94fa75117f678aa3b/6af70bd14e0bad6598a5a954)):
![Database structure](./documentation/restaurant_kitchen_db.png)

### Web pages
Below are pictures of web pages:

#### Accounts pages
- Login page:
![Login](./documentation/login.png)

- Signup page:
![Sign Up](./documentation/signup.png)

- Change password page:
![Change password](./documentation/change_password.png)

#### Error pages
- 403 page:
![403](documentation/403.png)

- 404 page:
![404](documentation/404.png)

Home page:
![Home](./documentation/home.png)

#### Dish type pages

- Dish types page (as admin):
![Dish type list admin](documentation/dish_type_list_admin.png)

- Dish types page (as moderator):
![Dish type list moderator](documentation/dish_type_list_moderator.png)

- Dish types page (as user):
![Dish type list user](documentation/dish_type_list_user.png)

- Create dish type page:
![Dish_type create](./documentation/dish_type_create.png)

- Update dish type page:
![Dish_type update](./documentation/dish_type_update.png)

- Delete dish type page:
![Dish_type delete](./documentation/dish_type_delete.png)

#### Ingredient pages

- Ingredients page (as admin):
![Ingredient list admin](documentation/ingredient_list_admin.png)

- Ingredients page (as moderator):
![Ingredient list moderator](documentation/ingredient_list_moderator.png)

- Ingredients page (as user):
![Ingredient list user](documentation/ingredient_list_user.png)

- Create ingredient page:
![Ingredient create](./documentation/ingredient_create.png)

- Update ingredient page:
![Ingredient update](./documentation/ingredient_update.png)

- Delete ingredient page:
![Ingredient delete](./documentation/ingredient_delete.png)

#### Dish pages

- Dishes page:
![Dish list](./documentation/dish_list.png)

- Dish page (as admin):
![Dish detail admin](documentation/dish_detail_admin.png)

- Dish page (as moderator):
![Dish detail moderator](documentation/dish_detail_moderator.png)

- Dish page (as user):
![Dish detail user](documentation/dish_detail_user.png)

- Create dish page:
![Dish create](./documentation/dish_create.png)

- Update dish page:
![Dish update](./documentation/dish_update.png)

- Delete dish page:
![Dish delete](./documentation/dish_delete.png)

#### Cook pages

Cook list page:
![Cook list](./documentation/cook_list.png)

Cook detail (as admin):
![Cook detail admin](./documentation/cook_detail_admin.png)

Cook detail (as moderator):
![Cook detail moderator](./documentation/cook_detail_moderator.png)

Cook detail (as user):
![Cook detail user](./documentation/cook_detail_user.png)

Cook create (as admin):
![Cook create admin](./documentation/cook_create_admin.png)

Cook create (as moderator):
![Cook create moderator](./documentation/cook_create_moderator.png)

Cook update (as admin):
![Cook update admin](./documentation/cook_update_admin.png)

Cook update (as moderator):
![Cook update moderator](./documentation/cook_update_moderator.png)

Cook delete:
![Cook delete](./documentation/cook_delete.png)

## Installation
Below are introduced steps how to install and run the project on your local machine.

1. Clone the repository - `git clone https://github.com/bknyrik/restaurant-kitchen-service.git`;
2. Install all dependencies using poetry - `poetry install --no-root`;
3. Add `.env` file according to `.env.sample` templates;
4. Apply migrations `flask db upgrade`;
5. Run the script file to create all user groups - `psql -d <DATABASE_NAME> -U <USER_USERNAME> -f init.sql`;
6. Run the server `flask --app app.main run -p 8000 --debug --reload`.

## Usage
Visit `http://localhost:8000/` to use this application. \
And also don't forget to create an admin user - `flask create_admin admin adminpass12345`.

## Contact
Email: knyrikkolesnichenko2004@gmail.com
