# Generated by Django 2.1.5 on 2020-03-10 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100000)),
                ('heading', models.CharField(max_length=10000)),
                ('source', models.CharField(max_length=1000)),
                ('author', models.CharField(max_length=10000)),
                ('label', models.IntegerField(default=-1)),
            ],
        ),
    ]