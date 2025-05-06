from uuid import UUID
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, joinedload, lazyload, Mapped
from sqlalchemy import URL, MetaData, DateTime, BigInteger

from schemas.user import BaseSchema

def create_connection_string(database_name, username='root', password='root', host='localhost', port=3306):
    if not database_name:
        raise ValueError('database_name can\'t empty')

    connection_string = URL.create(
        "mysql+pymysql",
        username=username,
        password=password,
        host=host,
        database=database_name,
        port=port,
    ).render_as_string(hide_password=False)

    return connection_string

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now())
    

db = SQLAlchemy(model_class=Base)

class BaseModel(Base):
    __abstract__ = True
    def save(self, commit=False):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self
    
    def delete(self, commit=False):
        db.session.delete(self)
        if commit:
            db.session.commit()
        return self
    
    def load(self, relationships=[]):
        return db.session.query(type(self)).options(
            *[lazyload(getattr(self, rel)) for rel in relationships]
        )
    
    def to_dict(self, **kwargs):
        schema: BaseSchema | None = getattr(self, "Schema", None)
        if schema is not None:
            return schema.model_validate(self).model_dump(**kwargs)
    
    @classmethod
    def find(cls, id):
        try:
            id = UUID(id)
        except ValueError:
            id = id
        return db.session.query(cls).get(id)
    
    @classmethod
    def where(cls, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, str):
                try:
                    value = UUID(value)
                except ValueError:
                    pass
            kwargs[key] = value

        return db.session.query(cls).filter_by(**kwargs)
    
    @classmethod
    def create(cls, attributes: dict, commit=False):
        instance = cls(**attributes)
        db.session.add(instance)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        return instance
    
    @classmethod
    def with_relation(cls, relationships=[]):
        return db.session.query(cls).options(
            *[joinedload(getattr(cls, rel)) for rel in relationships]
        )
    
    @classmethod
    def commit(cls):
        db.session.commit()