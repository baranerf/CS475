from sqlite3 import IntegrityError
from typing import TYPE_CHECKING

from database import Database

if TYPE_CHECKING:
    from models import Model


class Manager:
    def __init__(self, model, db=None):
        self.model = model
        self.table_name = self.model.__name__
        self.db = db or Database()

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        try:
            self.db.insert_record(self.model.__name__, **kwargs)
        except IntegrityError:
            raise Exception(
                f"IntegrityError: The record with the primary key `{instance._primary_key}` already exists."
            )
        return instance

    def get(self, **kwargs):
        if "pk" in kwargs:
            pk_value = str(kwargs["pk"])
            primary_key = self.model._primary_key
            row = self.db.get_record_by_pk(self.model.__name__, primary_key, pk_value)
            if row:
                return self.model(**dict(zip([column[0] for column in self.db.get_description()], row)))
            else:
                return None
        else:
            row = self.db.get_records(self.model.__name__, kwargs.keys(), [str(val) for val in kwargs.values()])
            if len(row) > 1:
                raise Exception("Multiple records found.")
            if len(row) == 0:
                return None
            return self.model(**dict(zip([column[0] for column in self.db.get_description()], row[0])))

    def all(self):
        rows = self.db.fetch_all_records(self.model.__name__)
        return [
            self.model(**dict(zip([column[0] for column in self.db.get_description()], row)))
            for row in rows
        ]

    def get_or_create(self, **kwargs) -> (bool, "Model"):
        is_created = False
        instance = self.get(**kwargs)
        if instance is None:
            is_created = True
            instance = self.create(**kwargs)
        return is_created, instance

    def filter(self, **kwargs):
        rows = self.db.get_records(self.model.__name__, kwargs.keys(), [str(val) for val in kwargs.values()])
        return [
            self.model(**dict(zip([column[0] for column in self.db.get_description()], row)))
            for row in rows
        ]

    def update(self, instance, **kwargs):
        for field_name, value in kwargs.items():
            if hasattr(instance, field_name):
                field = getattr(self.model, field_name)
                if not isinstance(value, field.data_type):
                    value = field.data_type(value)
                setattr(instance, field_name, value)
            else:
                raise AttributeError(f"{field_name} is not a valid field name.")
        self.db.update_record(
            self.model.__name__, instance._primary_key, str(getattr(instance, instance._primary_key)), **kwargs
        )

    def delete(self, instance):
        self.db.delete_record(self.model.__name__, instance._primary_key, str(getattr(instance, instance._primary_key)))
        del instance
