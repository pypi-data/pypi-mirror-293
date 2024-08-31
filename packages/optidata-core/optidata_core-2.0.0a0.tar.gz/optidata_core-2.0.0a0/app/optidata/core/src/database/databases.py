import threading

from sqlalchemy import create_engine, QueuePool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class DatabasePoolSingleton:
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, db_url, pool_size=5, max_overflow=10, pool_timeout=30):
        with cls._lock:
            if db_url not in cls._instances:
                instance = super(DatabasePoolSingleton, cls).__new__(cls)
                engine = create_engine(
                    db_url,
                    poolclass=QueuePool,
                    pool_size=pool_size,
                    max_overflow=max_overflow,
                    pool_timeout=pool_timeout
                )
                session_factory = sessionmaker(bind=engine)
                instance._engine = engine
                instance._Session = session_factory
                cls._instances[db_url] = instance
            return cls._instances[db_url]

    def get_session(self):
        return self._Session()

    def close_session(self, session):
        session.close()
