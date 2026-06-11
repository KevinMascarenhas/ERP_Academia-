from django.db import migrations, models
import django.db.models.deletion


def create_turmas_for_existing_modalidades(apps, schema_editor):
    Modalidade = apps.get_model("modalidades", "Modalidade")
    Turma = apps.get_model("modalidades", "Turma")
    for modalidade in Modalidade.objects.all():
        Turma.objects.get_or_create(
            modalidade=modalidade,
            defaults={"nome": f"Turma {modalidade.modalidade_nome}"},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("modalidades", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Turma",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120)),
                ("capacidade", models.PositiveIntegerField(default=30)),
                (
                    "modalidade",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="turma",
                        to="modalidades.modalidade",
                    ),
                ),
            ],
            options={
                "verbose_name": "Turma",
                "verbose_name_plural": "Turmas",
                "ordering": ["modalidade__modalidade_nome"],
            },
        ),
        migrations.RunPython(create_turmas_for_existing_modalidades, migrations.RunPython.noop),
    ]
