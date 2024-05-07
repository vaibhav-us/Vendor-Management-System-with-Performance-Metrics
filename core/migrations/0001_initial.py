# Generated by Django 4.2.2 on 2024-05-07 13:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact_details', models.TextField(max_length=500)),
                ('address', models.TextField(max_length=500)),
                ('vendor_code', models.CharField(max_length=50)),
                ('on_time_delivery_rate', models.FloatField(blank=True, default=0.0, null=True)),
                ('quality_rating_avg', models.FloatField(blank=True, default=0.0, null=True)),
                ('avg_response_time', models.FloatField(blank=True, default=0.0, null=True)),
                ('fulfillment_rate', models.FloatField(blank=True, default=0.0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.CharField(max_length=100)),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('in_time_delivery', models.BooleanField(default=False)),
                ('items', models.JSONField()),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(default='pending', max_length=100)),
                ('quality_rating', models.FloatField(blank=True, null=True)),
                ('issue_date', models.DateTimeField(blank=True, null=True)),
                ('acknowledgement_date', models.DateTimeField(blank=True, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('on_time_delivery_rate', models.FloatField(default=0.0)),
                ('quality_rating_avg', models.FloatField(default=0.0)),
                ('avg_response_time', models.FloatField(default=0.0)),
                ('fulfillment_rate', models.FloatField(default=0.0)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vendor')),
            ],
        ),
    ]
