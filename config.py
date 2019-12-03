import os
import yaml

class Config():
    pq_user = os.environ.get("POSTGRES_USER")
    pq_pass = os.environ.get("POSTGRES_PASSWORD")

    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=False
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{pq_user}:{pq_pass}@clustersitter-db:5432/{pq_user}"

