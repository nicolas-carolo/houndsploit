# Generated by Django 2.1.2 on 2018-12-07 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exploit',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('file', models.TextField()),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('author', models.TextField()),
                ('vulnerability_type', models.TextField()),
                ('platform', models.TextField()),
                ('port', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shellcode',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('file', models.TextField()),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('author', models.TextField()),
                ('vulnerability_type', models.TextField()),
                ('platform', models.TextField()),
            ],
        ),
    ]
