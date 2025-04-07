1. Install virtual environment

   `python -m venv myenv`

2. Setup your database.

   Copy the `SEED_DATA.sql` code into a database query and run it

3. setup `.env` file using the `.env_template` file
4. activate environment

   `.\myenv\Scripts\Activate.ps1`

5. Install the following in the venv:

   1. `pip install flask`
   2. `pip install SQLAlchemy Flask-SQLAlchemy pyodbc`
   3. `pip install dotenv`

6. install requirements

   `pip install -r requirements.txt `

7. run app

   `python app.py`
