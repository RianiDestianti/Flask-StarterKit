from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, event
from sqlalchemy.orm import Session, with_loader_criteria
from config.database import db


class SoftDelete:
    deleted_at = Column(DateTime, nullable=True)


class BaseModel(db.Model):
    __abstract__ = True
    __hidden__   = []

    id          = Column(Integer, primary_key=True)
    created_at  = Column(DateTime, default=datetime.now)
    updated_at  = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            column.name : getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in self.__hidden__
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def destroy(self):
        if isinstance(self, SoftDelete):
            self.deleted_at = datetime.now()
        else:
            db.session.delete(self)

        db.session.commit()


@event.listens_for(Session, "do_orm_execute")
def _exclude_soft_deleted(state):
    if (
        state.is_select
        and not state.is_column_load
        and not state.is_relationship_load
        and not state.execution_options.get("with_trashed", False)
    ):
        state.statement = state.statement.options(
            with_loader_criteria(SoftDelete, lambda cls: cls.deleted_at.is_(None), include_aliases=True)
        )
