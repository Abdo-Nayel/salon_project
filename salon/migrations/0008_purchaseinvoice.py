import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0007_booking_serial_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.PositiveIntegerField(default=0, verbose_name='المسلسل')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_invoices', to='salon.branch', verbose_name='Branch')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_invoices', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
            options={
                'verbose_name': 'Purchase Invoice',
                'verbose_name_plural': 'Purchase Invoices',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PurchaseInvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Qty')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Unit Cost')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Unit Price')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_items', to='salon.product', verbose_name='Product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='salon.purchaseinvoice', verbose_name='Purchase')),
            ],
            options={
                'verbose_name': 'Purchase Item',
                'verbose_name_plural': 'Purchase Items',
            },
        ),
        migrations.AddConstraint(
            model_name='purchaseinvoice',
            constraint=models.UniqueConstraint(fields=('branch', 'serial_number'), name='unique_branch_purchase_serial'),
        ),
    ]
