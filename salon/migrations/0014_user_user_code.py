from django.db import migrations, models


def assign_user_codes(apps, schema_editor):
    User = apps.get_model('salon', 'User')
    code = 1
    for user in User.objects.order_by('id'):
        if not user.user_code:
            user.user_code = str(code)
            user.save(update_fields=['user_code'])
            code += 1


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0013_salonsettings_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_code',
            field=models.CharField(blank=True, max_length=20, verbose_name='كود المستخدم'),
        ),
        migrations.RunPython(assign_user_codes, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='user',
            name='user_code',
            field=models.CharField(blank=True, max_length=20, unique=True, verbose_name='كود المستخدم'),
        ),
    ]
