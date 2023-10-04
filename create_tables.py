# from decouple import config

from prh.models import create_tables
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    create_tables()
    