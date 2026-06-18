from django.db import migrations, models


def assign_serial_numbers(apps, schema_editor):
    Invoice = apps.get_model('salon', 'Invoice')
    by_branch = {}
    for inv in Invoice.objects.order_by('created_at', 'id'):
        bid = inv.branch_id
        by_branch[bid] = by_branch.get(bid, 0) + 1
        inv.serial_number = by_branch[bid]
        inv.invoice_number = str(by_branch[bid])
        inv.save(update_fields=['serial_number', 'invoice_number'])


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0003_dailyqueuenumber'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='invoice',
                    name='is_voided',
                    field=models.BooleanField(default=False, verbose_name='ملغاة'),
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        'ALTER TABLE salon_invoice '
                        'ADD COLUMN IF NOT EXISTS is_voided boolean NOT NULL DEFAULT false;'
                    ),
                    reverse_sql=(
                        'ALTER TABLE salon_invoice '
                        'DROP COLUMN IF EXISTS is_voided;'
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='serial_number',
            field=models.PositiveIntegerField(default=0, verbose_name='المسلسل'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(max_length=20, verbose_name='رقم الفاتورة'),
        ),
        migrations.RunPython(assign_serial_numbers, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='invoice',
            constraint=models.UniqueConstraint(
                fields=('branch', 'serial_number'),
                name='unique_branch_invoice_serial',
            ),
        ),
    ]
