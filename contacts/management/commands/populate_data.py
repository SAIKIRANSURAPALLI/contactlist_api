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
        user, created = self.User.objects.get_or_create(username='allisongreen')
        Contact.objects.create(
            owner=user, 
            name=self.fake.name(), 
            phone_number=self.fake.phone_number(),
            is_spam=random.choice([True, False]),
            spam_likelihood=random.uniform(0, 100)
        )

        # Create random users
        for _ in range(50):  # 50 users
            user = self.User.objects.create_user(
                username=self.fake.user_name(),
                email=self.fake.email(),
                phone_number=self.fake.phone_number(),
                password='password123'
            )
            user.save()

        # Create random contacts
        users = self.User.objects.all()
        for user in users:
            for _ in range(random.randint(5, 20)): 
                Contact.objects.create(
                    owner=user,
                    name=self.fake.name(),
                    phone_number=self.fake.phone_number(),
                    is_spam=random.choice([True, False]),
                    spam_likelihood=random.uniform(0, 100)
                )

        self.stdout.write(self.style.SUCCESS('Database populated with random data'))
