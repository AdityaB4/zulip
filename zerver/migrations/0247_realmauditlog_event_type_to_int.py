# Generated by Django 1.11.24 on 2019-10-02 16:48

from django.db import migrations, models
from django.db.backends.postgresql_psycopg2.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps

INT_VALUE = {
    'user_created': '101',
    'user_activated': '102',
    'user_deactivated': '103',
    'user_reactivated': '104',
    'user_soft_activated': '120',
    'user_soft_deactivated': '121',
    'user_password_changed': '122',
    'user_avatar_source_changed': '123',
    'user_full_name_changed': '124',
    'user_email_changed': '125',
    'user_tos_version_changed': '126',
    'user_api_key_changed': '127',
    'user_bot_owner_changed': '128',

    'realm_deactivated': '201',
    'realm_reactivated': '202',
    'realm_scrubbed': '203',
    'realm_plan_type_changed': '204',
    'realm_logo_changed': '205',
    'realm_exported': '206',

    'subscription_created': '301',
    'subscription_activated': '302',
    'subscription_deactivated': '303',

    'stripe_customer_created': '401',
    'stripe_card_changed': '402',
    'stripe_plan_changed': '403',
    'stripe_plan_quantity_reset': '404',

    'customer_created': '501',
    'customer_plan_created': '502',
}

STR_VALUE = {
    101: 'user_created',
    102: 'user_activated',
    103: 'user_deactivated',
    104: 'user_reactivated',

    120: 'user_soft_activated',
    121: 'user_soft_deactivated',
    122: 'user_password_changed',
    123: 'user_avatar_source_changed',
    124: 'user_full_name_changed',
    125: 'user_email_changed',
    126: 'user_tos_version_changed',
    127: 'user_api_key_changed',
    128: 'user_bot_owner_changed',

    201: 'realm_deactivated',
    202: 'realm_reactivated',
    203: 'realm_scrubbed',
    204: 'realm_plan_type_changed',
    205: 'realm_logo_changed',
    206: 'realm_exported',

    301: 'subscription_created',
    302: 'subscription_activated',
    303: 'subscription_deactivated',

    401: 'stripe_customer_created',
    402: 'stripe_card_changed',
    403: 'stripe_plan_changed',
    404: 'stripe_plan_quantity_reset',

    501: 'customer_created',
    502: 'customer_plan_created',
}

def update_existing_event_type_values(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    RealmAuditLog = apps.get_model('zerver', 'RealmAuditLog')
    for log_entry in RealmAuditLog.objects.all():
        log_entry.event_type_int = INT_VALUE[log_entry.event_type]
        log_entry.save(update_fields=['event_type_int'])

def reverse_code(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    RealmAuditLog = apps.get_model('zerver', 'RealmAuditLog')
    for log_entry in RealmAuditLog.objects.all():
        log_entry.event_type = STR_VALUE[log_entry.event_type_int]
        log_entry.save(update_fields=['event_type'])

class Migration(migrations.Migration):
    dependencies = [
        ('zerver', '0246_message_date_sent_finalize_part2'),
    ]

    operations = [
        migrations.AddField(
            model_name='realmauditlog',
            name='event_type_int',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='realmauditlog',
            name='event_type',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.RunPython(update_existing_event_type_values,
                             reverse_code=reverse_code),
        migrations.RemoveField(
            model_name='realmauditlog',
            name='event_type',
        ),
        migrations.RenameField(
            model_name='realmauditlog',
            old_name='event_type_int',
            new_name='event_type',
        ),
        migrations.AlterField(
            model_name='realmauditlog',
            name='event_type',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
