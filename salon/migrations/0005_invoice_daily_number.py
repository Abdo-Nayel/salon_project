from django.db import migrations, models
import django.db.models.deletion


def backfill_daily_number(apps, schema_editor):
    Invoice = apps.get_model('salon', 'Invoice')
    for inv in Invoice.objects.all().iterator():
        serial = inv.serial_number or 0
        doc = inv.document_date
        if inv.created_at and not doc:
            doc = inv.created_at.date()
        Invoice.objects.filter(pk=inv.pk).update(
            daily_number=serial,
            document_date=doc,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0004_invoice_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='daily_number',
            field=models.PositiveIntegerField(default=0, verbose_name='المسلسل اليومي'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='document_date',
            field=models.DateField(blank=True, null=True, verbose_name='تاريخ المستند'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='booking',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='invoices',
                to='salon.booking',
                verbose_name='Booking',
            ),
        ),
        migrations.RunPython(backfill_daily_number, migrations.RunPython.noop),
    ]
