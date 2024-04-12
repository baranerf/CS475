# CS475 Project: Object Relational Mapper (ORM)

This project is a simple, stand-alone and lightweight implementation of an Object Relational Mapper (ORM) for Python. 
The ORM is a library that allows developers to interact with a relational database using Python objects. 
The ORM will handle the mapping of Python objects to database tables and vice versa.

## How to use

The first step to is to design your models (tables). For each model you can inherit from `models.Model` and define its
fields as class attributes of available fields from the `fields` module.

```python
from models import Model
from fields import UUIDField, StringField, IntegerField

class MyModel(Model):
    id = UUIDField(primary_key=True)
    name = StringField()
    rating = IntegerField()
```

As appears in the example above, you can define the primary key by setting the `primary_key` attribute to `True` in 
only one field. Then you can start data manipulation by creating instances of your models, etc.

```python
from uuid import uuid4

id_1 = uuid4()
my_model = MyModel.objects.create(id=id_1, name='My Model', rating=5)
print(my_model.id)
print(my_model.name)
print(my_model.rating)
```

```python
id_2 = uuid4()
my_model_2 = MyModel.objects.create(id=id_2, name='My Model 2', rating=4)
print(my_model_2.id)
print(my_model_2.name)
print(my_model_2.rating)
```

```python
models = MyModel.objects.all()
for model in models:
    print(model.id)
    print(model.name)
    print(model.rating)
```

```python
specific_model = MyModel.objects.get(id=id_1)
print(specific_model.id)
```

```python
models_with_rating_4 = MyModel.objects.filter(rating=4)
for model in models_with_rating_4:
    print(model.id)
    print(model.name)
    print(model.rating)
```

Furthermore, you may manipulate and update the data in the database by updating the fields of the model instances and
calling the `save` method to apply the changes to the database.

```python
my_model.rating = 3
my_model.save()
```

Finally, you can delete a model instance by calling the `delete` method.

```python
my_model.delete()
```

## Unit Testing
TODO
