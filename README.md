# test_assignment_fastapi
Developed a service using FastAPI and PostgreSQL, which includes a basic role system, request handling and storage, and message sending to Telegram.  The service is designed to be scalable and maintainable, with clear separation of concerns and modular code.

How to run the application:



## Prerequisites

Ensure that Python 3.12, pip, Docker, and Docker Compose are installed on your machine.


## Common Steps


Regardless of the method of running the application, follow these steps:


```shell
git clone https://github.com/wandererOdmolyboh/test_assignment_fastapi.git
```
```shell
cd <your catalog with project>
```



### Running on your local machine

chage file .env.example to .env and fill it with your data


```shell
python3 -m venv venv
```
```shell
source venv/bin/activate
```
```shell
pip install -r requirements.txt
```

```shell
alembic init alembic
```

1. Open the `alembic.ini` file and update the `sqlalchemy.url` value:

    ```ini
        sqlalchemy.url = postgresql+asyncpg://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s/%(DB_NAME)s?async_fallback=True
    ```
2. open the `alembic/env.py` file and update config:

    ```python

        from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
        config = context.config

        section = config.config_ini_section
        config.set_section_option(section, "DB_HOST", DB_HOST)
        config.set_section_option(section, "DB_PORT", DB_PORT)
        config.set_section_option(section, "DB_NAME", DB_NAME)
        config.set_section_option(section, "DB_USER", DB_USER)
        config.set_section_option(section, "DB_PASS", DB_PASS)
   ```
3. Navigate to the `alembic/env.py` file and add the following imports at the top of the file:

    ```python
        from src.message.models import *
        from src.user.models import *
    ```

4. Still in the `alembic/env.py` file, update the `target_metadata` value:

    ```python
        target_metadata = [Base.metadata]
    ```

Make DB migration:
```shell
  alembic revision --autogenerate -m 'Cread table' 
```
```shell
  alembic upgrade head     
```
if you want to fill the database with test data, run the script:
```shell
   python3 tests/fill_test_data.py  
```

Start the server:
```shell
  uvicorn main:app --reload  
```

### Running with Docker

chage file .env.example to .env and fill it with your data  and set parameters to DB_HOST=postgres

1. Open the `alembic.ini` file and update the `sqlalchemy.url` value:

    ```ini
        sqlalchemy.url = postgresql+asyncpg://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s/%(DB_NAME)s?async_fallback=True
    ```
2. open the `alembic/env.py` file and update config:

    ```python

        from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
        config = context.config

        section = config.config_ini_section
        config.set_section_option(section, "DB_HOST", DB_HOST)
        config.set_section_option(section, "DB_PORT", DB_PORT)
        config.set_section_option(section, "DB_NAME", DB_NAME)
        config.set_section_option(section, "DB_USER", DB_USER)
        config.set_section_option(section, "DB_PASS", DB_PASS)
   ```
3. Navigate to the `alembic/env.py` file and add the following imports at the top of the file:

    ```python
        from src.message.models import *
        from src.user.models import *
    ```

4. Still in the `alembic/env.py` file, update the `target_metadata` value:

    ```python
        target_metadata = [Base.metadata]
    ```

```shell
  docker-compose up 
```

## Additional Information
1. Do not forget to start chat with your bot and/or add bot to your group chat!!!
2. Tested POST requests via Postman https://www.postman.com/
3. Sure, please ensure that you replace <your catalog with project> with the appropriate path to your project.