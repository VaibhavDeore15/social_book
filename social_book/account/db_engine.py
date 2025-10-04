# db_engine.py
from sqlalchemy import create_engine


# PostgreSQL connection: replace with your credentials
engine = create_engine(
    "postgresql+psycopg2://postgres:Pass%40123@localhost:5432/my_db"
)

engine1 = create_engine(
    "mysql+pymysql://root:Pass%40123@localhost:3306/std"
)


