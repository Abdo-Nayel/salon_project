import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0009_stockmovement_serial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumptionInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.PositiveIntegerField(default=0, verbose_name='المسلسل')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumption_invoices', to='salon.branch', verbose_name='Branch')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consumption_invoices', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
            options={
                'verbose_name': 'Consumption Invoice',
                'verbose_name_plural': 'Consumption Invoices',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ConsumptionInvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Qty')),
                ('unit_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Unit Cost')),
                ('consumption', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='salon.consumptioninvoice', verbose_name='Consumption')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumption_items', to='salon.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Consumption Item',
                'verbose_name_plural': 'Consumption Items',
            },
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='reference_consumption',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movements', to='salon.consumptioninvoice', verbose_name='فاتورة استهلاك'),
        ),
        migrations.AddConstraint(
            model_name='consumptioninvoice',
            constraint=models.UniqueConstraint(fields=('branch', 'serial_number'), name='unique_branch_consumption_serial'),
        ),
    ]
