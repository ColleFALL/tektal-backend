from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paths', '0005_path_share_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='GPSPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('timestamp', models.BigIntegerField(help_text='Timestamp en millisecondes')),
                ('order', models.PositiveIntegerField(help_text='Ordre du point GPS dans le trajet')),
                ('path', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='gps_points',
                    to='paths.path'
                )),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
