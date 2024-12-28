from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drf_simple_apikey", "0002_alter_apikey_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apikey",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
