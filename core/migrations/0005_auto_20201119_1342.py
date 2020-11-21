# Generated by Django 3.0.8 on 2020-11-19 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201119_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produto', to='core.Produto'),
        ),
        migrations.AlterField(
            model_name='item',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to='core.Usuario'),
        ),
    ]