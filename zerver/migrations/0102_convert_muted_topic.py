# Generated by Django 1.11.4 on 2017-08-30 00:26
import ujson
from django.db import connection, migrations
from django.db.backends.postgresql_psycopg2.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps


def convert_muted_topics(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    stream_query = '''
        SELECT
            zerver_stream.name,
            zerver_stream.realm_id,
            zerver_stream.id,
            zerver_recipient.id
        FROM
            zerver_stream
        INNER JOIN zerver_recipient ON (
            zerver_recipient.type_id = zerver_stream.id AND
            zerver_recipient.type = 2
        )
    '''

    stream_dict = {}

    with connection.cursor() as cursor:
        cursor.execute(stream_query)
        rows = cursor.fetchall()
        for (stream_name, realm_id, stream_id, recipient_id) in rows:
            stream_name = stream_name.lower()
            stream_dict[(stream_name, realm_id)] = (stream_id, recipient_id)

    UserProfile = apps.get_model("zerver", "UserProfile")
    MutedTopic = apps.get_model("zerver", "MutedTopic")

    new_objs = []

    user_query = UserProfile.objects.values(
        'id',
        'realm_id',
        'muted_topics'
    )

    for row in user_query:
        user_profile_id = row['id']
        realm_id = row['realm_id']
        muted_topics = row['muted_topics']

        tups = ujson.loads(muted_topics)
        for (stream_name, topic_name) in tups:
            stream_name = stream_name.lower()
            val = stream_dict.get((stream_name, realm_id))
            if val is not None:
                stream_id, recipient_id = val
                muted_topic = MutedTopic(
                    user_profile_id=user_profile_id,
                    stream_id=stream_id,
                    recipient_id=recipient_id,
                    topic_name=topic_name,
                )
                new_objs.append(muted_topic)

    with connection.cursor() as cursor:
        cursor.execute('DELETE from zerver_mutedtopic')

    MutedTopic.objects.bulk_create(new_objs)

class Migration(migrations.Migration):

    dependencies = [
        ('zerver', '0101_muted_topic'),
    ]

    operations = [
        migrations.RunPython(convert_muted_topics),
    ]
