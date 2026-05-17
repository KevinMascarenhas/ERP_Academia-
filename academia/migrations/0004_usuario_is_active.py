# Generated manually for the custom user model.

from django.contrib.auth.hashers import identify_hasher, make_password
from django.db import migrations, models


def hash_raw_passwords(apps, schema_editor):
    Usuario = apps.get_model("academia", "Usuario")

    for usuario in Usuario.objects.all().only("pk", "password"):
        if not usuario.password:
            continue

        try:
            identify_hasher(usuario.password)
        except ValueError:
            usuario.password = make_password(usuario.password)
            usuario.save(update_fields=["password"])


class Migration(migrations.Migration):

    dependencies = [
        ("academia", "0003_administrador_remove_usuario_modalidades_inscritas_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(hash_raw_passwords, migrations.RunPython.noop),
    ]
