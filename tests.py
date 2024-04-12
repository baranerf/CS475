from pathlib import Path
from unittest import TestCase
from uuid import uuid4, UUID

import database
import fields
import manager
import models


class DBTest(TestCase):
    def setUp(self):
        self.db = database.Database(db_name="unittest.sqlite3")

    def tearDown(self):
        self.db.connection.close()
        Path("unittest.sqlite3").unlink()

    def test_database_creation(self):
        db = database.Database(db_name="test_database_creation.sqlite3")
        self.assertIsNotNone(db)
        db.connection.close()
        Path("test_database_creation.sqlite3").unlink()

    def test_create_table(self):
        self.db.create_table("test_table", ["id INTEGER PRIMARY KEY", "name TEXT"])
        self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_table'")
        self.assertIsNotNone(self.db.fetchone())

    def test_insert_record(self):
        self.db.create_table("test_table", ["id INTEGER PRIMARY KEY", "name TEXT"])
        self.db.insert_record("test_table", id=1, name="Baran")
        self.db.execute("SELECT * FROM test_table")
        self.assertIsNotNone(self.db.fetchone())

    def test_get_record(self):
        self.db.create_table("test_table", ["id INTEGER PRIMARY KEY", "name TEXT"])
        self.db.insert_record("test_table", id=1, name="Baran")
        self.assertIsNotNone(self.db.get_record_by_pk("test_table", "id", 1))

    def test_fetch_all_records(self):
        self.db.create_table("test_table", ["id INTEGER PRIMARY KEY", "name TEXT"])
        self.db.insert_record("test_table", id=1, name="Baran")
        self.db.insert_record("test_table", id=2, name="Erfani")
        self.assertEqual(len(self.db.fetch_all_records("test_table")), 2)

    def test_get_description(self):
        self.db.create_table("test_table", ["id INTEGER PRIMARY KEY", "name TEXT"])
        self.db.execute("SELECT * FROM test_table")
        self.assertIsNotNone(self.db.get_description())

    def test_execute_fetchone(self):
        self.db.execute("SELECT 1")
        self.assertIsNotNone(self.db.fetchone())


class ORMTest(TestCase):
    def setUp(self):
        self.db = database.Database(db_name="unittest.sqlite3")

    def tearDown(self):
        self.db.connection.close()
        Path("unittest.sqlite3").unlink()

    def test_model_creation(self):
        class TestModel(models.Model):
            id = fields.UUIDField(primary_key=True)

            class Meta:
                db = self.db

        self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TestModel'")
        self.assertIsNotNone(self.db.fetchone())

    def test_model_insert(self):
        class TestModel(models.Model):
            id = fields.UUIDField(primary_key=True)

            class Meta:
                db = self.db

        test_id = uuid4()
        TestModel.objects.create(id=test_id)
        self.db.get_description()
        self.db.execute("SELECT * FROM TestModel")
        instance = self.db.fetchone()
        self.assertIsNotNone(instance)
        self.assertEqual(instance[0], str(test_id))

    def test_model_get(self):
        class TestModel(models.Model):
            id = fields.UUIDField(primary_key=True)

            class Meta:
                db = self.db

        test_id = uuid4()
        TestModel.objects.create(id=test_id)
        instance = TestModel.objects.get(pk=test_id)
        self.assertIsNotNone(instance)
        self.assertEqual(instance.id, test_id)

    def test_model_all(self):
        class TestModel(models.Model):
            id = fields.UUIDField(primary_key=True)

            class Meta:
                db = self.db

        test_id = uuid4()
        TestModel.objects.create(id=test_id)
        self.assertEqual(len(TestModel.objects.all()), 1)
        test_id_2 = uuid4()
        TestModel.objects.create(id=test_id_2)
        self.assertEqual(len(TestModel.objects.all()), 2)
        self.assertEqual(TestModel.objects.all()[0].id, test_id)
        self.assertEqual(TestModel.objects.all()[1].id, test_id_2)

    def test_data_type(self):
        class TestModel(models.Model):
            id = fields.UUIDField(primary_key=True)
            name = fields.StringField()

            class Meta:
                db = self.db

        test_id = uuid4()
        TestModel.objects.create(id=test_id, name="Baran")
        instance = TestModel.objects.get(pk=test_id)
        self.assertIsNotNone(instance)
        self.assertEqual(instance.id, test_id)
        self.assertIsInstance(instance.id, UUID)
        self.assertEqual(instance.name, "Baran")
        self.assertIsInstance(instance.name, str)

    def test_custom_manager(self):
        class CustomManager(manager.Manager):
            def custom_method(self):
                return "This is a custom method."

        class TestModel(models.Model):
            id = fields.UUIDField(primary_key=True)
            name = fields.StringField()

            class Meta:
                db = self.db
                objects = CustomManager

        test_id = uuid4()
        instance = TestModel.objects.create(id=test_id, name="Baran")
        self.assertEqual(instance.objects.custom_method(), "This is a custom method.")

    def test_get_or_create(self):
        class TestModel(models.Model):
            id = fields.UUIDField(primary_key=True)
            name = fields.StringField()

            class Meta:
                db = self.db

        test_id_1 = uuid4()
        test_id_2 = uuid4()
        is_created_1, instance_1 = TestModel.objects.get_or_create(id=test_id_1, name="Baran")
        is_created_2, instance_2 = TestModel.objects.get_or_create(id=test_id_1, name="Baran")
        self.assertEqual(instance_1.id, instance_2.id)
        self.assertEqual(is_created_1, True)
        self.assertEqual(is_created_2, False)
        is_created_3, instance_3 = TestModel.objects.get_or_create(id=test_id_2, name="Yazdan")
        self.assertEqual(is_created_3, True)
        self.assertNotEqual(instance_1.id, instance_3.id)
        self.assertNotEqual(instance_2.id, instance_3.id)

    def test_filter(self):
        class TestModel(models.Model):
            id = fields.UUIDField(primary_key=True)
            name = fields.StringField()
            age = fields.IntegerField()

            class Meta:
                db = self.db

        test_id_1 = uuid4()
        test_id_2 = uuid4()
        test_id_3 = uuid4()
        TestModel.objects.create(id=test_id_1, name="Baran", age=23)
        TestModel.objects.create(id=test_id_2, name="Yazdan", age=23)
        TestModel.objects.create(id=test_id_3, name="Sobhan", age=18)
        self.assertEqual(len(TestModel.objects.filter(age=23)), 2)
        self.assertEqual(len(TestModel.objects.filter(age=18)), 1)
        self.assertEqual(len(TestModel.objects.filter(age=24)), 0)
