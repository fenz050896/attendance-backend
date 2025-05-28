from uuid import UUID
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, joinedload, Mapped
from sqlalchemy import URL, MetaData, DateTime, BigInteger, select, func, exists

from app.schemas.base_schema import BaseSchema

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

def cast_uuid(val):
    if isinstance(val, str):
        try:
            return UUID(val)
        except ValueError:
            return val
    return val

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

    def to_dict(self, only_relations: list[str] = None, **kwargs):
        schema: BaseSchema | None = getattr(self, "Schema", None)
        if schema:
            model_dict = schema.model_validate(self).model_dump(**kwargs)
            if only_relations is not None:
                keys_to_keep = set(only_relations) | {
                    k for k in model_dict if not isinstance(model_dict[k], dict)
                }
                return {k: v for k, v in model_dict.items() if k in keys_to_keep}
            return model_dict
        return {}

    def __repr__(self):
        return f"<{type(self).__name__} id={getattr(self, 'id', None)}>"

    @classmethod
    def _cast_uuid(cls, val):
        return cast_uuid(val)

    @classmethod
    def find(cls, id, serialize=False, mode='python'):
        id = cls._cast_uuid(id)
        return QueryBuilder(cls).where(cls.id == id).first(serialize, mode)

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
    def create_many(cls, attributes: list, commit=False):
        instances = [cls(**attr) for attr in attributes]
        db.session.add_all(instances)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        return instances

    @classmethod
    def where(cls, *conditions):
        return QueryBuilder(cls).where(*conditions)

    @classmethod
    def with_relation(cls, relationships=[]):
        return QueryBuilder(cls).with_relation(relationships)

    @classmethod
    def all(cls, serialize=False, mode='python'):
        return QueryBuilder(cls).all(serialize, mode)

    @classmethod
    def first(cls, serialize=False, mode='python'):
        return QueryBuilder(cls).first(serialize, mode)

    @classmethod
    def count_with_condition(cls, *conditions):
        return QueryBuilder(cls).where(*conditions).count()

    @classmethod
    def commit(cls):
        db.session.commit()

    @classmethod
    def query_builder(cls):
        return QueryBuilder(cls)

class QueryBuilder:
    def __init__(self, model, stmt=None):
        self.model = model
        self.stmt = stmt or select(model)
        self._allowed_relations = []

    def where(self, *conditions):
        if conditions:
            self.stmt = self.stmt.where(*conditions)
        return self

    def with_relation(self, relationships=[]):
        self._allowed_relations = relationships
        self.stmt = self.stmt.options(*[
            joinedload(self._resolve_relation_path(rel)) for rel in relationships
        ])
        return self
    
    def _resolve_relation_path(self, relation: str):
        parts = relation.split('.')
        attr = getattr(self.model, parts[0])
        for part in parts[1:]:
            attr = getattr(attr.property.mapper.class_, part)
        return attr

    def order_by(self, *criteria):
        self.stmt = self.stmt.order_by(*criteria)
        return self

    def limit(self, n):
        self.stmt = self.stmt.limit(n)
        return self

    def offset(self, n):
        self.stmt = self.stmt.offset(n)
        return self

    def paginate(self, page=1, per_page=10, serialize=False, mode='python'):
        count_stmt = self.stmt.with_only_columns(func.count(), maintain_column_froms=True).order_by(None)
        total = db.session.execute(count_stmt).scalar_one()

        paged_stmt = self.stmt.offset((page - 1) * per_page).limit(per_page)
        items = db.session.execute(paged_stmt).scalars().all()

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
            "items": [self._serialize_item(i, mode) if serialize else i for i in items]
        }

    def all(self, serialize=False, mode='python'):
        results = db.session.execute(self.stmt).scalars().all()
        return [self._serialize_item(i, mode) if serialize else i for i in results]

    def first(self, serialize=False, mode='python'):
        result = db.session.execute(self.stmt.limit(1)).scalars().first()
        return self._serialize_item(result, mode) if serialize and result else result

    def count(self):
        count_stmt = self.stmt.with_only_columns(func.count(), maintain_column_froms=True).order_by(None)
        return db.session.execute(count_stmt).scalar_one()

    def exists(self):
        exists_stmt = select(exists(self.stmt))
        result = db.session.execute(exists_stmt).scalar()
        return bool(result)

    def get_query(self):
        return self.stmt

    def _serialize_item(self, item, mode):
        if hasattr(item, "to_dict"):
            return item.to_dict(only_relations=self._allowed_relations, mode=mode)
        return item
