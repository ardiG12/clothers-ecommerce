from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db import transaction
import random
from decimal import Decimal
from faker import Faker

from app.models import Category, Product

fake = Faker()


class Command(BaseCommand):
    help = "Seed database with categories and products using Faker"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding started..."))

        # ----- Categories -----
        category_names = [
            "Clothes",
            "Shoes",
            "Electronics",
            "Home",
            "Accessories",
            "Sport",
            "Cosmetics",
        ]

        categories = []

        for name in category_names:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={"slug": slugify(name)}
            )
            categories.append(cat)

        # ----- Choice lists -----
        COLOR_CHOICES = [c[0] for c in Product.COLOR_CHOICES]
        SIZE_CHOICES = [s[0] for s in Product.SIZE_CHOICES]

        # ----- Create Products -----
        for _ in range(40):
            category = random.choice(categories)

            price = Decimal(random.randint(10, 300))
            old_price = price + Decimal(random.randint(5, 80))

            Product.objects.create(
                title=fake.word().capitalize() + " " + fake.word().capitalize(),
                description=fake.text(max_nb_chars=200),
                price=price,
                old_price=old_price,
                color=random.choice(COLOR_CHOICES),
                size=random.choice(SIZE_CHOICES),
                rating=Decimal(random.randint(20, 50)) / 10,
                category=category,
            )

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))
