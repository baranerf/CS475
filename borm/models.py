from .fields import AbstractField
from .manager import Manager
from .database import Database


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        new_attrs = {}
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, AbstractField):
                attr_value.name = attr_name
            new_attrs[attr_name] = attr_value

        db = getattr(attrs.get("Meta"), "db", Database())
        objects = getattr(attrs.get("Meta"), "objects", Manager) or Manager

        new_class = super().__new__(cls, name, bases, new_attrs)
        new_class.objects = objects(new_class, db)

        # Generate columns for SQL table creation
        columns = []
        primary_key_set = False
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, AbstractField):
                column_type = 'TEXT' if attr_value.data_type is str else attr_value.data_type.__name__.upper()
                column_definition = f"{attr_name} {column_type}"
                if attr_value.primary_key:
                    if primary_key_set:
                        raise AttributeError(f"{name} cannot have more than one primary key.")
                    column_definition += " PRIMARY KEY"
                    new_class._primary_key = attr_name
                    primary_key_set = True
                columns.append(column_definition)

        if columns:
            db.create_table(name, columns)

        return new_class


class Model(metaclass=ModelMeta):
    """Base Model class to be inherited by other models."""

    class Meta:
        verbose_name = None
        verbose_name_plural = None
        db: Database = None
        objects: Manager = None

    def __init__(self, **kwargs):
        for field_name, value in kwargs.items():
            if hasattr(self, field_name):
                field = getattr(self.__class__, field_name)
                if not isinstance(value, field.data_type):
                    value = field.data_type(value)
                setattr(self, field_name, value)
            else:
                raise AttributeError(f"{field_name} is not a valid field name.")

    def save(self):
        fields = {}
        for field_name, field in self.__class__.__dict__.items():
            if isinstance(field, AbstractField):
                fields[field_name] = getattr(self, field_name)
        self.objects._update(self, **fields)

    def delete(self):
        self.objects._delete(self)
