# Generated by Django 3.0.8 on 2020-11-19 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20201119_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='usuario',
        ),
        migrations.AlterField(
            model_name='item',
            name='produto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produto', to='core.Produto'),
        ),
    ]
