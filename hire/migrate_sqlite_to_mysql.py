import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import models and metadata
from models import db as flask_db
from models import (
    User, Job, Candidate, Round, Interview, Assessment, MCQQuestion, AuditLog,
    ProgrammingLanguage, QuestionBank, QuestionBankItem, ScoringPolicy, RoundTemplate,
    InterviewSchedule, InterviewPlan, CandidateTestResult
)
from config import Config


def get_sqlite_url():
    # Use the same SQLite fallback the app uses
    return os.environ.get("SQLITE_URL", Config.SQLALCHEMY_DATABASE_URI)


def get_mysql_url():
    # Build from env similar to Config
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT", "3306")
    dbname = os.environ.get("MYSQL_DB")
    if not all([user, password, host, dbname]):
        raise RuntimeError(
            "Missing MySQL env vars: MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB"
        )
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"


def create_mysql_schema(mysql_engine):
    # Create all tables in MySQL based on Flask SQLAlchemy metadata
    flask_db.Model.metadata.create_all(mysql_engine)


def migrate_table(src_session, dst_session, model):
    rows = src_session.query(model).all()
    for row in rows:
        # Detach ORM instance and add to destination
        dst_session.merge(row)
    dst_session.commit()


def main():
    sqlite_url = get_sqlite_url()
    mysql_url = get_mysql_url()

    print(f"Source (SQLite): {sqlite_url}")
    print(f"Destination (MySQL): {mysql_url}")

    src_engine = create_engine(sqlite_url)
    dst_engine = create_engine(mysql_url)

    # Ensure destination schema exists
    create_mysql_schema(dst_engine)

    SrcSession = sessionmaker(bind=src_engine)
    DstSession = sessionmaker(bind=dst_engine)

    src_session = SrcSession()
    dst_session = DstSession()

    # Collect all mapped classes from Flask-SQLAlchemy
    models = []
    for cls in flask_db.Model._decl_class_registry.values():
        if hasattr(cls, "__table__"):
            models.append(cls)

    # Preserve a simple dependency order by using foreign key counts
    def fk_count(m):
        return len(m.__table__.foreign_keys)

    models.sort(key=fk_count)

    for model in models:
        print(f"Migrating {model.__name__}...")
        migrate_table(src_session, dst_session, model)

    src_session.close()
    dst_session.close()
    print("Migration complete.")


if __name__ == "__main__":
    main()
