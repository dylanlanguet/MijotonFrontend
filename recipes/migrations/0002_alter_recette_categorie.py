from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recette',
            name='categorie',
            field=models.CharField(choices=[('entree', 'Entrée'), ('plat', 'Plat'), ('dessert', 'Dessert'), ('cocktail', 'Cocktail')], max_length=20),
        ),
    ]
