from gino import Gino
from gino.schema import GinoSchemaVisitor

from dotenv import load_dotenv
from os import getenv

load_dotenv()
db = Gino()

postgresurl = f'postgresql://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}@{getenv("DB_HOST")}/{getenv("DB_NAME")}'


async def create_db():
    await db.set_bind(postgresurl)
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()
