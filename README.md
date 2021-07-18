Journal is a simple web application written in Django. It is intended to be used as a diary or log companion.

For styling, Bootstrap 4 was used due to its easy setup process.

The default database (sqlite3) was changed to PostgreSQL as Heroku doesn't recommend sqlite3 for production.

Right now, asynchronous features aren't supported so requests will result in a relod. This will be fixed in the future. 