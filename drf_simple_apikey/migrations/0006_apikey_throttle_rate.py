import drf_simple_apikey.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drf_simple_apikey", "0005_apikey_hashed_secret"),
    ]

    operations = [
        migrations.AddField(
            model_name="apikey",
            name="throttle_rate",
            field=models.CharField(
                max_length=50,
                blank=True,
                default="",
                validators=[drf_simple_apikey.models.validate_throttle_rate],
                help_text=(
                    "Maximum request rate for this API key, e.g. '100/hour' "
                    "(s, m, h or d). Leave empty to use the 'api_key' rate from "
                    "DEFAULT_THROTTLE_RATES. Only enforced by APIKeyRateThrottle."
                ),
            ),
        )
    ]
