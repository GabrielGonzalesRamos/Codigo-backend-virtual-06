# Generated by Django 3.2.4 on 2021-06-21 19:11

import datetime
from django.db import migrations, models
import django.db.models.deletion
import gestion.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LibroModel',
            fields=[
                ('libroId', models.AutoField(db_column='id', primary_key=True, serialize=False, unique=True)),
                ('libroNombre', models.CharField(db_column='nombre', help_text='Ingrese un nombre valido', max_length=45, verbose_name='Nombre del libro')),
                ('libroEdicion', models.IntegerField(choices=[(1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)], db_column='edicion', default=gestion.models.anio_actual, help_text='Ingrese el año de la edicion', verbose_name='Año de edicion')),
                ('libroAutor', models.TextField(db_column='autor', help_text='Ingrese el autor', verbose_name='Autor del libro')),
                ('libroCantidad', models.IntegerField(db_column='cantidad', default=0, verbose_name='Cantidad')),
                ('createAt', models.DateTimeField(auto_now_add=True, db_column='created_at')),
                ('updateAt', models.DateTimeField(auto_now=True, db_column='updated_at')),
                ('deleteAt', models.DateTimeField(db_column='deleted_at', null=True)),
            ],
            options={
                'verbose_name': 'libro',
                'verbose_name_plural': 'libros',
                'db_table': 'libros',
                'ordering': ['-libroEdicion', '-libroCantidad', 'libroNombre'],
            },
        ),
        migrations.CreateModel(
            name='PrestamoModel',
            fields=[
                ('prestamoId', models.AutoField(db_column='id', primary_key=True, serialize=False, unique=True)),
                ('prestamoFechaInicio', models.DateField(db_column='fecha_inicio', default=datetime.date.today, verbose_name='Fecha de inicio del prestamo')),
                ('prestamoFechaFin', models.DateField(db_column='fecha_fin', verbose_name='Fecha de fin del prestamo')),
                ('prestamoEstado', models.BooleanField(db_column='estado', default=True, help_text='Indique el estado del prestamo', verbose_name='Estado del prestamo')),
            ],
            options={
                'verbose_name': 'prestamo',
                'verbose_name_plural': 'prestamos',
                'db_table': 'prestamos',
                'ordering': ['-prestamoFechaFin'],
            },
        ),
        migrations.CreateModel(
            name='UsuarioModel',
            fields=[
                ('usuarioId', models.AutoField(db_column='id', primary_key=True, serialize=False, unique=True)),
                ('usuarioNombre', models.CharField(db_column='nombre', help_text='Aqui debes ingresar el nombre', max_length=25, verbose_name='Nombre del usuario')),
                ('usuarioApellido', models.CharField(db_column='apellido', help_text='Debes de ingresar el apellido del usuario', max_length=25, verbose_name='Apellido del usuario')),
                ('usuarioCorreo', models.EmailField(db_column='correo', help_text='Debes de ingresar un correo valido', max_length=50, verbose_name='Correo del usuario')),
                ('usuarioDni', models.CharField(db_column='dni', help_text='Ingrese un DNI válido', max_length=8, verbose_name='Dni del usuario')),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuarios',
                'db_table': 'usuarios',
                'ordering': ['-usuarioCorreo', 'usuarioNombre'],
            },
        ),
        migrations.AddIndex(
            model_name='usuariomodel',
            index=models.Index(fields=['usuarioCorreo', 'usuarioDni'], name='usuarios_correo_fd9ad5_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='usuariomodel',
            unique_together={('usuarioCorreo', 'usuarioDni', 'usuarioNombre')},
        ),
        migrations.AddField(
            model_name='prestamomodel',
            name='libro',
            field=models.ForeignKey(db_column='libro_id', help_text='Seleccione el libro a prestar', on_delete=django.db.models.deletion.PROTECT, related_name='libroPrestamos', to='gestion.libromodel', verbose_name='Libro'),
        ),
        migrations.AddField(
            model_name='prestamomodel',
            name='usuario',
            field=models.ForeignKey(db_column='usuario_id', help_text='Seleccione el usuario a prestar', on_delete=django.db.models.deletion.CASCADE, related_name='usuarioPrestamos', to='gestion.usuariomodel', verbose_name='Usuario'),
        ),
        migrations.AlterUniqueTogether(
            name='libromodel',
            unique_together={('libroNombre', 'libroEdicion', 'libroAutor')},
        ),
    ]
