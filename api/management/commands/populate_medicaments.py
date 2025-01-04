from django.core.management.base import BaseCommand
from api.models import Medicament  

class Command(BaseCommand):
    help = 'Populate the database with sample medicaments'

    def handle(self, *args, **options):
        medicaments = [
    {
        'nom': 'Paracétamol',
        'description': 'Analgésique et antipyrétique utilisé pour traiter la douleur et la fièvre.',
        'max_duree': 7,
        'max_dose': 4.0,
        'in_stock': True,
        'prix': 200
    },
    {
        'nom': 'Ibuprofène',
        'description': 'Anti-inflammatoire non stéroïdien (AINS) utilisé pour traiter la douleur et l\'inflammation.',
        'max_duree': 5,
        'max_dose': 2.4,
        'in_stock': True,
        'prix': 300
    },
    {
        'nom': 'Amoxicilline',
        'description': 'Antibiotique de la famille des pénicillines utilisé pour traiter diverses infections bactériennes.',
        'max_duree': 10,
        'max_dose': 3.0,
        'in_stock': True,
        'prix': 400
    },
    {
        'nom': 'Oméprazole',
        'description': 'Inhibiteur de la pompe à protons utilisé pour réduire la production d\'acide gastrique.',
        'max_duree': 14,
        'max_dose': 40.0,
        'in_stock': True,
        'prix': 250
    },
    {
        'nom': 'Metformine',
        'description': 'Médicament antidiabétique oral utilisé pour traiter le diabète de type 2.',
        'max_duree': 0,  # Indéfinie
        'max_dose': 2.0,
        'in_stock': True,
        'prix': 150
    },
    {
        'nom': 'Salbutamol',
        'description': 'Bronchodilatateur utilisé pour traiter l\'asthme et la BPCO.',
        'max_duree': 0,  # Indéfinie
        'max_dose': 0.8,
        'in_stock': True,
        'prix': 180
    },
    {
        'nom': 'Loratadine',
        'description': 'Antihistaminique utilisé pour traiter les allergies.',
        'max_duree': 0,  # Indéfinie
        'max_dose': 10.0,
        'in_stock': True,
        'prix': 120
    },
    {
        'nom': 'Sertraline',
        'description': 'Antidépresseur de type ISRS utilisé pour traiter la dépression et l\'anxiété.',
        'max_duree': 0,  # Indéfinie
        'max_dose': 200.0,
        'in_stock': True,
        'prix': 500
    },
    {
        'nom': 'Amlodipine',
        'description': 'Inhibiteur calcique utilisé pour traiter l\'hypertension artérielle.',
        'max_duree': 0,  # Indéfinie
        'max_dose': 10.0,
        'in_stock': True,
        'prix': 350
    },
    {
        'nom': 'Lévothyroxine',
        'description': 'Hormone thyroïdienne de synthèse utilisée pour traiter l\'hypothyroïdie.',
        'max_duree': 0,  # Indéfinie
        'max_dose': 0.0,  # Indéfinie
        'in_stock': True,
        'prix': 300
    },
    # Nouveaux médicaments
    {
        'nom': 'Atorvastatine',
        'description': 'Médicament hypolipémiant utilisé pour réduire le cholestérol.',
        'max_duree': 0,  # Indéfinie
        'max_dose': 80.0,
        'in_stock': True,
        'prix': 400
    },
    {
        'nom': 'Clarithromycine',
        'description': 'Antibiotique macrolide utilisé pour traiter diverses infections.',
        'max_duree': 14,
        'max_dose': 1.0,
        'in_stock': False,
        'prix': 600
    },
    {
        'nom': 'Diclofénac',
        'description': 'Anti-inflammatoire non stéroïdien utilisé pour traiter la douleur et l\'inflammation.',
        'max_duree': 7,
        'max_dose': 150.0,
        'in_stock': True,
        'prix': 220
    },
    {
        'nom': 'Furosemide',
        'description': 'Diurétique utilisé pour traiter l\'hypertension et l\'oedème.',
        'max_duree': 0,  # Indéfinie
        'max_dose': 80.0,
        'in_stock': True,
        'prix': 180
    }
         ]


        for medicament_data in medicaments:
            try:
                medicament = Medicament.objects.create(**medicament_data)
                self.stdout.write(self.style.SUCCESS(f'Successfully created medicament: {medicament.nom}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create medicament {medicament_data["nom"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Database population completed!'))