from sqlalchemy import Connection

from app.core.db import user_table


def find_user_by_email(db: Connection, email: str):
    stmt = user_table.select().where(user_table.c.email == email)
    user = db.execute(stmt)
    return user.fetchone()


def find_user_by_id(db_conn: Connection, user_id: int):
    stmt = user_table.select().where(user_table.c.uid == user_id)
    user = db_conn.execute(stmt)
    return user.fetchone()
