from django.core.management.base import BaseCommand
from faker import Faker
from contacts.models import Contact
from django.contrib.auth import get_user_model
import random

class Command(BaseCommand):
    help = 'Populates the database with random users and contacts'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()
        self.User = get_user_model()

    def handle(self, *args, **options):
        # Create or get a specific user
        user, created = self.User.objects.get_or_create(username='allisongreen')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new user: {user.username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'User already exists: {user.username}'))
        
        # Create a random contact for the specific user
        Contact.objects.create(
            owner=user, 
            name=self.fake.name(), 
            phone_number=self.fake.phone_number(),
            is_spam=random.choice([True, False]),
            spam_likelihood=random.uniform(0, 100)
        )

        # Create random users
        for _ in range(50):  
            user = self.User.objects.create_user(
                username=self.fake.user_name(),
                email=self.fake.email(),
                phone_number=self.fake.phone_number(),
                password='password123'
            )
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))

        # Create random contacts for all users
        users = self.User.objects.all()
        for user in users:
            for _ in range(random.randint(5, 20)): 
                contact = Contact.objects.create(
                    owner=user,
                    name=self.fake.name(),
                    phone_number=self.fake.phone_number(),
                    is_spam=random.choice([True, False]),
                    spam_likelihood=random.uniform(0, 100)
                )
                self.stdout.write(self.style.SUCCESS(f'Created contact for user {user.username}: {contact}'))

        self.stdout.write(self.style.SUCCESS('Database populated with random data'))
