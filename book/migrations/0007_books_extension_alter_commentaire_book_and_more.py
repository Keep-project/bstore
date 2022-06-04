# Generated by Django 4.0.4 on 2022-06-04 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_alter_books_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='extension',
            field=models.CharField(default='pdf', max_length=50),
        ),
        migrations.AlterField(
            model_name='commentaire',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.books'),
        ),
        migrations.AlterField(
            model_name='telecharge',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.books'),
        ),
    ]
