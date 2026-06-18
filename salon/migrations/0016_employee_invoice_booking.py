# Generated manually — salon_employee table already exists in DB

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0015_user_extra_permissions'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Employee',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('serial_number', models.CharField(max_length=30, verbose_name='كود الموظف')),
                        ('name', models.CharField(max_length=100, verbose_name='اسم الموظف')),
                        ('phone', models.CharField(blank=True, default='', max_length=20, verbose_name='Phone')),
                        ('job_title', models.CharField(blank=True, default='', max_length=50, verbose_name='الوظيفة')),
                        ('base_salary', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='الراتب')),
                        ('hire_date', models.DateField(verbose_name='تاريخ التعيين')),
                        ('is_active', models.BooleanField(default=True, verbose_name='نشط')),
                        ('notes', models.TextField(blank=True, default='', verbose_name='Notes')),
                        ('daily_number', models.PositiveIntegerField(default=0, verbose_name='رقم يومي')),
                        ('created_at', models.DateTimeField(auto_now_add=True)),
                        ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='salon.branch', verbose_name='Branch')),
                        ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                    ],
                    options={
                        'verbose_name': 'Employee',
                        'verbose_name_plural': 'Employees',
                        'db_table': 'salon_employee',
                        'ordering': ['serial_number'],
                        'unique_together': {('branch', 'serial_number')},
                    },
                ),
            ],
            database_operations=[],
        ),
        migrations.AddField(
            model_name='invoice',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='salon.employee', verbose_name='Employee'),
        ),
        migrations.AddField(
            model_name='booking',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='salon.employee', verbose_name='Employee'),
        ),
    ]
