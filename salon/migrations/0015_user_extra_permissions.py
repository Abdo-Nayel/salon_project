from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0014_user_user_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_audit',
            field=models.BooleanField(default=False, verbose_name='Can Access Audit'),
        ),
        migrations.AddField(
            model_name='user',
            name='can_bookings',
            field=models.BooleanField(default=False, verbose_name='Can Access Bookings'),
        ),
        migrations.AddField(
            model_name='user',
            name='can_customers',
            field=models.BooleanField(default=False, verbose_name='Can Access Customers'),
        ),
        migrations.AddField(
            model_name='user',
            name='can_services',
            field=models.BooleanField(default=False, verbose_name='Can Access Services'),
        ),
        migrations.AddField(
            model_name='user',
            name='can_employees',
            field=models.BooleanField(default=False, verbose_name='Can Access Employees'),
        ),
        migrations.AddField(
            model_name='user',
            name='can_delete_pos',
            field=models.BooleanField(default=False, verbose_name='Can Delete POS'),
        ),
        migrations.AddField(
            model_name='user',
            name='can_delete_bookings',
            field=models.BooleanField(default=False, verbose_name='Can Delete Bookings'),
        ),
        migrations.AddField(
            model_name='user',
            name='can_delete_expenses',
            field=models.BooleanField(default=False, verbose_name='Can Delete Expenses'),
        ),
        migrations.AddField(
            model_name='user',
            name='can_delete_inventory',
            field=models.BooleanField(default=False, verbose_name='Can Delete Inventory'),
        ),
        migrations.AddField(
            model_name='user',
            name='can_delete_employees',
            field=models.BooleanField(default=False, verbose_name='Can Delete Employees'),
        ),
    ]
