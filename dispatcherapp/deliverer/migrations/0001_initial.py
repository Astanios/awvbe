# Generated by Django 2.0.4 on 2018-04-14 16:41

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('versions', jsonfield.fields.JSONField()),
            ],
        ),
    ]
