from app.db.session import engine
from app.db.base import Base
from app.models import user, post, comment

# call init_db() on app startup or from a script to create tables.
def init_db():
    Base.metadata.create_all(bind=engine)

