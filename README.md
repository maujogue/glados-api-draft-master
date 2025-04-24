# glados-back

## Prerequisite:
- Python 3
- Docker
- Flake8

## Prepare container

### Environment variables
In order to access the environment variables, it is essential to have them in a `.env` file. You can change them whenever you want.
To do this, copy the contents of the `.env.example` file into a new `.env`.
```
cp .env.example .env
```

### Build container
Then it is necessary to build the container and initiate the database.
```
make build
```

## Test application

`Test Driven Development` (TDD) is a software development process. The objective is to first think about the tests that are going to be performed, and therefore the expected results, and to write the associated tests before developing the application.

The `coverage` is the percentage of code covered by all the tests in the application. The application should have a coverage of at least 85%.

Every new endpoints, services, providers should be unit tested.

### Run tests
You can easily run all pytests using :
```
make tests
```

### Run coverage
To display the coverage you can use :
```
make coverage
```

If you want a full report of the coverage you can run :
```
make coverage_html
```

### Lints and fixes files
To check the quality of your code and if it respects certain rules, use this command :
```
make lint
```

## Run application
To launch the project on a development environment, use this command :
```
make run
```

The first time you run the application or when you add some modifications to the database structure, you should upgrade the database schema base on the migration files :
```
make db_upgrade
```

You can now access to the application via your web browser on `localhost` and port you choose in your `.env`.

You can display what's going on there :
```
make logs
```


## Database managment

Adminer (formerly phpMinAdmin) is a full-featured database management tool written in PHP. Conversely to phpMyAdmin, it consist of a single file ready to deploy to the target server. Adminer is available for MySQL, MariaDB, PostgreSQL, SQLite, MS SQL, Oracle, Elasticsearch, MongoDB and others via plugin.

You can easily access Adminer via your web browser on `localhost` and port you choose in your `.env`.

```
system: `PostgreSQL`
server: `db`
username: `postgres`
password: `root`
database: `glados`
```
