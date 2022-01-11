# Generated by Django 4.0 on 2022-01-11 19:34

from django.db import migrations, models
import django.db.models.deletion


def set_default_upload_dandiset(apps, schema_editor):
    """Set the dandiset field for all existing uploads to the first dandiset."""
    Dandiset = apps.get_model('api', 'Dandiset')
    Upload = apps.get_model('api', 'Upload')
    # Fresh installations will have no dandisets, but also no uploads, so initialize this inside the loop
    first_dandiset = None
    uploads = list(Upload.objects.filter(dandiset=None).all())
    for upload in uploads:
        if first_dandiset is None:
            first_dandiset = Dandiset.objects.order_by('created').first()
        upload.dandiset = first_dandiset
    Upload.objects.bulk_update(uploads, ['dandiset'])


def reverse_set_default_upload_dandiset(apps, schema_editor):
    # Explicitly do nothing so the migration is still reversible.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_embargo_models'),
    ]

    operations = [
        # Set up the dandiset field, but make it nullable temporarily
        migrations.AddField(
            model_name='upload',
            name='dandiset',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='uploads',
                to='api.dandiset',
            ),
        ),
        # Set a default dandiset field for any uploads which have a null field
        migrations.RunPython(set_default_upload_dandiset, reverse_set_default_upload_dandiset),
        # Make dandiset non-nullable
        migrations.AlterField(
            model_name='upload',
            name='dandiset',
            field=models.ForeignKey(
                # This will never be used
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='uploads',
                to='api.dandiset',
            ),
            preserve_default=False,
        ),
    ]
