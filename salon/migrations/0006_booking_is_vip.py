from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0005_invoice_daily_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_vip',
            field=models.BooleanField(default=False, verbose_name='حجز VIP'),
        ),
    ]
