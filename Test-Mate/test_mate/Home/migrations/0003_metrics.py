# Generated by Django 3.1.2 on 2021-04-10 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Questions', '0001_initial'),
        ('Home', '0002_auto_20210410_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mean_marks', models.IntegerField(blank=True, null=True)),
                ('minimum_marks', models.IntegerField(blank=True, null=True)),
                ('maximum_marks', models.IntegerField(blank=True, null=True)),
                ('test_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Questions.configcreation')),
            ],
            options={
                'verbose_name': 'Code Metric',
                'verbose_name_plural': 'Code Metrics',
            },
        ),
    ]