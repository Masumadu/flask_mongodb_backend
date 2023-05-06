from faker import Faker
from mongoengine import Document


class Seeder:
    db: Document
    fake: Faker

    @classmethod
    def run(cls):
        print("Seeding complete")
