from django.db import migrations, models
import django.db.models.deletion


def backfill_movement_serials(apps, schema_editor):
    StockMovement = apps.get_model('salon', 'StockMovement')
    for m in StockMovement.objects.all().iterator():
        StockMovement.objects.filter(pk=m.pk).update(
            serial_number=m.id,
            daily_number=m.id,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0008_purchaseinvoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockmovement',
            name='serial_number',
            field=models.PositiveIntegerField(default=0, verbose_name='المسلسل'),
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='daily_number',
            field=models.PositiveIntegerField(default=0, verbose_name='رقم يومي'),
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='reference_invoice',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='movements',
                to='salon.purchaseinvoice',
                verbose_name='فاتورة مشتريات',
                db_column='reference_invoice_id',
            ),
        ),
        migrations.RunPython(backfill_movement_serials, migrations.RunPython.noop),
    ]
