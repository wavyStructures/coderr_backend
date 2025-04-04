# Generated by Django 5.1.4 on 2025-03-26 08:21

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.CreateModel(
            name='OfferDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('delivery_time', models.PositiveIntegerField()),
                ('offer_type', models.CharField(choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], max_length=10)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='offers_app.offer')),
            ],
        ),
    ]
