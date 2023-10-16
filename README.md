# A web application for a book review site build using Python Flask and PostgreSQL. 
### The application should show book reviews and user can inspect a specific book's reviews. 
- A user should be able to add books and give a review for those. Book's ratings are based on stars (or numbers between 1 and 5). A free form written review should also be given. The length of written review should be limitted to, for example, 400 characters. 
- User can also edit edit and delete their own messages.  
- A user can find books for example using their name or author.
- A user can see the most reviwed books or the books with the best overall ratings.
- An administrator can delete reviews (written reviews).

### This project is not on Fly.io so please run it locally.
- Clone the repository to any directory on your computer.
- Navigate to that directory and create a new test environment using "python3 -m venv test". Then activate the environment using "source test/bin/activate".
- Use "pip install -r requirements.txt" to install required dependencies.
- Create a new database and add tables using "psql -d <tietokannan-nimi> < schema.sql".
- Create a .env file inside cloned repository and add DATABASE_URL and SECRET_KEY variables. DATABASE_URL should be the same you used for your project. For example DATABASE_URL=postgresql:///user. Depending on your PosgoreSQL installation it can be something different. This works for me DATABASE_URL=postgresql://username:password@localhost/database_name. The SECRET_KEY should be created using instruction on https://hy-tsoha.github.io/materiaali/osa-2/#istunnot-ja-kirjautuminen. Please also read the instructions on https://hy-tsoha.github.io/materiaali/vertaisarviointi/.
- After these step the app can be run from terminal using "flask run".
- When testing the application, please create at least couple of reviews to test all functionalities.
### Currently implemented features:
- User can create an account.
- User can leave a review if they are logged in.
- The 5 most recent reviews are displayed on the front page (This is empty if no reviews are added).
- Reviews can be ordered by rating, book's names or the authors. 
- Search method where user can search for reviews.
- Users can delete their reviews and admin can delete any reviews.
  - Please note that admin account can only be created by directly inserting it to database.
- Users can save their favorite revies.  
