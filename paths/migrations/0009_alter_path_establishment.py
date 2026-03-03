import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paths', '0008_establishment'),
    ]

    operations = [
        migrations.AddField(
            model_name='path',
            name='establishment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paths', to='paths.establishment'),
        ),
    ]