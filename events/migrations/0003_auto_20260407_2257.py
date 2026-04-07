from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_is_akoka'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_akoka',
            field=models.BooleanField(default=False),
        ),
    ]