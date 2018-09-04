# Generated by Django 2.1.1 on 2018-09-02 18:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VnfModel',
            fields=[
                ('vnfInstanceId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vnfInstanceName', models.CharField(max_length=255)),
                ('vnfInstanceDescription', models.CharField(max_length=255)),
                ('vnfdId', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('vnfProvider', models.CharField(max_length=255)),
                ('vnfProductName', models.CharField(max_length=255)),
                ('vnfSoftwareVersion', models.CharField(max_length=255)),
                ('vnfdVersion', models.CharField(max_length=255)),
            ],
        ),
    ]
