# Generated by Django 3.1.1 on 2020-09-05 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('busker', '0010_auto_20200829_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='number_of_codes',
            field=models.IntegerField(default=100, help_text='The number of Download Codes to be generated with this batch. (Additional codes may be added to the batch later.)'),
        ),
        migrations.AlterField(
            model_name='downloadcode',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code', to='busker.batch'),
        ),
    ]
