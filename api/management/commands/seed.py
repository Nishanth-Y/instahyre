import random
from django.core.management.base import BaseCommand
from faker import Faker # type: ignore
from api.models import User, Contact, SpamReport

class Command(BaseCommand):
    help = 'Seed the database with test data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Users
        users = []
        for _ in range(10):  # Adjust the range to create more users if needed
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password123',
                phone_number=fake.phone_number(),
                email=fake.email()
            )
            users.append(user)

        # Create Contacts for Each User
        for user in users:
            for _ in range(random.randint(5, 15)):  # Each user gets between 5 to 15 contacts
                Contact.objects.create(
                    user=user,
                    name=fake.name(),
                    phone_number=fake.phone_number(),
                    email=fake.email() if random.choice([True, False]) else None
                )

        # Create Spam Reports
        for _ in range(20):  # Adjust the range to create more spam reports if needed
            SpamReport.objects.create(
                reported_user=random.choice(users),
                phone_number=fake.phone_number(),
                is_spam=True
            )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
