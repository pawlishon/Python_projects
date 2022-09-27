from django.core.management import BaseCommand
from Cookbook_app.models import Recipe
import mysql.connector

ALREADY_LOADED_ERROR_MESSAGE = """
                        If you need to reload recipe database, first delete the db.sqlite3 file to destroy the database.
                        Then run `manage.py migrate` for a new empty database with tables"""


class Command(BaseCommand):
    help = 'Loads data from MySQL database into our app model'

    def handle(self, *args, **options):
        if Recipe.objects.exists():
            print('Recipe data already loaded...')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        print('Creating recipe data')
        print('Importing db data')
        cnx = mysql.connector.connect(user='admin', password='admin', host='89.69.154.102', database='RECIPIES')
        c = cnx.cursor()
        query = """select *
                    from RECIPIES.recipies rec 
                    left join RECIPIES.recipies_metadata met on rec.file = replace(met.file, '.html', '')"""
        c.execute(query)
        db_data = c.fetchall()

        print('Assigning db data to model variables')
        for item in db_data:
            rec = Recipe()
            rec.file = int(item[0][1:])
            rec.content = item[1]
            rec.category = item[3]
            rec.title = item[4]
            rec.difficulty = item[5]
            rec.preparation_time = item[6]
            rec.total_time = item[7]
            rec.tags = item[8]
            rec.ingredients = item[9]
            rec.quantity = item[10]
            rec.save()
