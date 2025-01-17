# Generated by Django 5.1.3 on 2025-01-05 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id_clase', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('video_url', models.URLField()),
                ('fecha_publicacion', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EntregaTarea',
            fields=[
                ('id_entrega', models.AutoField(primary_key=True, serialize=False)),
                ('archivo_entrega', models.FileField(upload_to='entregas/')),
                ('comentario_estud', models.TextField(blank=True, null=True)),
                ('fecha_entregaT', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id_material', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200)),
                ('archivo', models.FileField(upload_to='materiales/')),
                ('clase_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materiales', to='AppClase.clase')),
            ],
        ),
        migrations.CreateModel(
            name='Retroalimentacion',
            fields=[
                ('id_retro', models.AutoField(primary_key=True, serialize=False)),
                ('comentario', models.TextField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('entrega_tarea_r', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retroalimentaciones', to='AppClase.entregatarea')),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id_tarea', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('fecha_entrega', models.DateField()),
                ('clase_tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tareas', to='AppClase.clase')),
            ],
        ),
        migrations.AddField(
            model_name='entregatarea',
            name='tarea_en',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entregas', to='AppClase.tarea'),
        ),
    ]
