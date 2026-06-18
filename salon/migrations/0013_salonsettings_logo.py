from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0012_salonsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='salonsettings',
            name='logo',
            field=models.ImageField(blank=True, upload_to='salon/logo/', verbose_name='الشعار'),
        ),
    ]
