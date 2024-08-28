# Generated by Django 5.0.6 on 2024-07-25 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("circuits", "0043_circuittype_color"),
        ("komora_service_path_plugin", "0008_servicepath_comments"),
        ("tenancy", "0015_contactassignment_rename_content_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="segment",
            old_name="supplier_segment_contract",
            new_name="provider_segment_contract",
        ),
        migrations.RenameField(
            model_name="segment",
            old_name="supplier_segment_id",
            new_name="provider_segment_id",
        ),
        migrations.RenameField(
            model_name="segment",
            old_name="supplier_segment_name",
            new_name="provider_segment_name",
        ),
        migrations.AddField(
            model_name="segment",
            name="provider",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="circuits.provider",
            ),
        ),
        migrations.AlterField(
            model_name="segment",
            name="supplier",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="tenancy.tenant",
            ),
        ),
    ]
