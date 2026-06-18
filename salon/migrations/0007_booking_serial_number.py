from django.db import migrations, models


def backfill_booking_serials(apps, schema_editor):
    Booking = apps.get_model('salon', 'Booking')
    for b in Booking.objects.all().iterator():
        serial = b.queue_number or b.id
        Booking.objects.filter(pk=b.pk).update(
            serial_number=serial,
            daily_number=serial,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0006_booking_is_vip'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='booking',
                    name='serial_number',
                    field=models.PositiveIntegerField(default=0, verbose_name='المسلسل'),
                ),
                migrations.AddField(
                    model_name='booking',
                    name='daily_number',
                    field=models.PositiveIntegerField(default=0, verbose_name='رقم يومي'),
                ),
            ],
            database_operations=[],
        ),
        migrations.RunPython(backfill_booking_serials, migrations.RunPython.noop),
    ]
