from uuid import UUID, uuid4


class AbstractField:
    def __init__(self, data_type, primary_key=False, *args, **kwargs):
        self.data_type = data_type
        self.value = None
        self.primary_key = primary_key

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

    def validate(self, value):
        if not isinstance(value, self.data_type):
            raise ValueError(f"ValueError: The value `{value}` is not the appropriate type. ({self.data_type})")


class UUIDField(AbstractField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            data_type=UUID,
            verbose_name=kwargs.get("verbose_name", None),
            required=kwargs.get("required", True),
            default=kwargs.get("default", uuid4()),
            nullable=kwargs.get("nullable", False),
            *args,
            **kwargs
        )


class IntegerField(AbstractField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            data_type=int,
            verbose_name=kwargs.get("verbose_name", None),
            required=kwargs.get("required", True),
            default=kwargs.get("default", None),
            nullable=kwargs.get("nullable", False),
            *args,
            **kwargs
        )


class FloatField(AbstractField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            data_type=float,
            verbose_name=kwargs.get("verbose_name", None),
            required=kwargs.get("required", True),
            default=kwargs.get("default", None),
            nullable=kwargs.get("nullable", False),
            *args,
            **kwargs
        )


class StringField(AbstractField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            data_type=str,
            verbose_name=kwargs.get("verbose_name", None),
            required=kwargs.get("required", True),
            default=kwargs.get("default", None),
            nullable=kwargs.get("nullable", False),
            *args,
            **kwargs
        )


class BooleanField(AbstractField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            data_type=bool,
            verbose_name=kwargs.get("verbose_name", None),
            required=kwargs.get("required", True),
            default=kwargs.get("default", None),
            nullable=kwargs.get("nullable", False),
            *args,
            **kwargs
        )
