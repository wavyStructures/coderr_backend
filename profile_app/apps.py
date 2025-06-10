from django.apps import AppConfig
from django.conf import settings
from django.utils import timezone
from django.db import connection
from decimal import Decimal
import os
import random
import sys

class ProfileAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile_app'
    
    def ready(self):
        if "migrate" in sys.argv or "makemigrations" in sys.argv:
            return
        
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
            return
           
        from offers_app.models import Offer
        from offers_app.models import OfferDetail

        from orders_app.models import Order
        from reviews_app.models import Review
        from django.contrib.auth import get_user_model

        User = get_user_model()     
        
        if 'user_auth_app_customuser' in connection.introspection.table_names():
            self.create_sample_data(User, Offer, Order, OfferDetail, Review)
        else:
            print("Skipping sample data creation — user table doesn't exist.")

    def create_sample_data(self, User, Offer, Order, OfferDetail, Review):
        
        # Create guest accounts
        guest_accounts = {
            "andrey": {
                "type": "customer",
                "first_name": "Andrey",
                "last_name": "Guest",
                "email": "andrey@example.com",
                "password": "asdasd"
            },
            "kevin": {
                "type": "business",
                "first_name": "Kevin",
                "last_name": "Guest",
                "email": "kevin@example.com",
                "password": "asdasd"
            }
        }

        for username, data in guest_accounts.items():
            user, created = User.objects.get_or_create(username=username)
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.email = data["email"]
            user.type = data["type"]

            if not user.password or not user.password.startswith('pbkdf2_sha256$'):
                user.set_password(data["password"])

            user.save()

        # Create or update customer users
        for i in range(5):
            user, created = User.objects.get_or_create(username=f'customer_user{i}')
            user.first_name = f'Customer{i}'
            user.last_name = f'LastNameC{i}'
            user.email = f'customer{i}@example.com'
            user.type = 'customer'
            
            # Only hash and set password if needed
            if not user.password or not user.password.startswith('pbkdf2_sha256$'):
                user.set_password('password123')
            
            user.save()

        # Create or update business users
        locations = ['Berlin', 'Munich', 'Hamburg', 'Cologne', 'Frankfurt', 'Stuttgart', 'Dresden', 'Leipzig']
        predefined_locations = {
            0: 'Berlin',
            1: 'Munich',
            2: 'Hamburg',
            3: 'Leipzig',
            4: 'Dresden',
            5: 'Hamburg',
            6: 'Berlin',
            7: 'Munich',
            8: 'Stuttgart',
            9: 'Berlin',
            10: 'Berlin',
        }
        descriptions = [
            {
                "text": "Hallo! Ich gestalte ein einzigartiges Logo, das deine Marke perfekt widerspiegelt – kreativ, einprägsam und maßgeschneidert für deinen Auftritt.",
            },
            {
                "text": "Mit gezielten Maßnahmen sorge ich dafür, dass deine Website bei Google besser gefunden wird – für mehr Sichtbarkeit und Reichweite.",
            },
            {
                "text": "Ob kleiner Shop oder große Plattform – ich baue dir einen sicheren und benutzerfreundlichen Online-Shop mit allen wichtigen Funktionen.",
            },
            {
                "text": "Ich erstelle dir eine moderne und responsive WordPress-Website, die du selbst leicht verwalten kannst – inklusive Design und Technik.",
            },
            {
                "text": "Langsame Website? Ich analysiere und verbessere die Ladezeit deiner Seite – für ein besseres Nutzererlebnis und Ranking.",
            },
            {
                "text": "Du brauchst mehr als eine einfache Website? Ich entwickle komplexe Web-Anwendungen nach deinen Anforderungen – funktional, skalierbar, durchdacht.",
            },
            {
                "text": "Deine Website ist veraltet? Ich überarbeite Design und Technik für einen frischen, zeitgemäßen Auftritt, der überzeugt.",
            },
            {
                "text": "Ich erstelle dir eine gezielte Landingpage, die dein Angebot perfekt in Szene setzt – ideal für Kampagnen und Werbung.",
            },
            {
                "text": "Ich baue dir eine Website, die mehrere Sprachen unterstützt – professionell übersetzt und benutzerfreundlich gestaltet.",
            },
            {
                "text": "Du bist dir nicht sicher, was du brauchst? Ich biete dir eine fundierte Beratung und helfe dir, die richtige Web-Lösung zu finden.",
            }
        ]
        working_hours = [
            "Mo–Fr 09:00–17:00 Uhr",
            "Mo–Mi 18:00–19:00 Uhr, Do–Fr 12:00–17:00 Uhr",
            "Mo, Mi, Fr 10:00–14:00 Uhr",
            "Di–Do 08:00–12:00 Uhr, Sa 09:00–11:00 Uhr",
            "Mo–So 11:00–20:00 Uhr",
            "Mo–Fr 14:00–18:00 Uhr, Sa 10:00–13:00 Uhr",
            "Mo–Do 09:30–16:30 Uhr, Fr 09:00–12:00 Uhr",
            "Di & Do 15:00–19:00 Uhr, Sa 10:00–12:00 Uhr",
            "Nur nach Vereinbarung",
            "Mo–Fr 07:00–15:00 Uhr, Wochenende geschlossen"
        ]
        for i in range(10):
            user, created = User.objects.get_or_create(username=f'business_user{i}')
            user.email = f'business{i}@example.com'
            user.first_name = f'Business{i}'
            user.last_name = f'LastNameB{i}'
            user.type = 'business'
            
            user.location = predefined_locations.get(i, random.choice(locations))
            # user.description = descriptions[i]
            user.description = descriptions[i % len(descriptions)]

            user.working_hours = working_hours[i]   
            if not user.password or not user.password.startswith('pbkdf2_sha256$'):
                user.set_password('password123')
            
            user.save()

        # Create sample offers
        business_users = User.objects.filter(type="business")
        if business_users.exists():
            some_user_instance = business_users.first()  
        else:
            some_user_instance = None  
            
        OfferDetail.objects.all().delete()

        for i in range(10):
            offer, created = Offer.objects.update_or_create(
                title=f"Offer {i}",
                defaults={
                    'description': f"Description for offer {i}",
                    'user': some_user_instance,
                    'image': None,
                }
            )

            offer.details.all().delete()

            prices = []
            delivery_times = []

            offer_types = ['basic', 'standard', 'premium']
            base_price = random.randint(50, 120)
            standard_price = base_price + random.randint(10, 50)
            premium_price = standard_price + random.randint(10, 50)

            price_map = {
                'basic': base_price,
                'standard': standard_price,
                'premium': premium_price,
            }

            for j, offer_type in enumerate(offer_types):
                price = price_map[offer_type]
                delivery_time_in_days = random.randint(1, 14)

                OfferDetail.objects.create(
                    offer=offer,
                    offer_type=offer_type,
                    price=price,
                    delivery_time_in_days=delivery_time_in_days,
                    title=f"{offer_type.capitalize()} Package",
                    description=f"Detail{j+1} for offer{i}"
                )

                prices.append(price)
                delivery_times.append(delivery_time_in_days)         

            
            # for j, offer_type in enumerate(offer_types):  # Create 3 details per offer
            #     price = random.randint(50, 200)
            #     delivery_time_in_days = random.randint(1, 14)

            #     OfferDetail.objects.create(
            #         offer=offer,
            #         offer_type=offer_type,
            #         price=price,
            #         delivery_time_in_days=delivery_time_in_days,
            #         title=f"{offer_type.capitalize()} Package",
            #         description=f"Detail{j+1} for offer{i}"
            #     )

            #     prices.append(price)
            #     delivery_times.append(delivery_time_in_days)

            # Set the new annotated fields
            offer.min_price = min(prices)
            offer.min_delivery_time = min(delivery_times)
            offer.save()

        # Create sample orders

        customer = User.objects.filter(type='customer').order_by('?').first()
        business = User.objects.filter(type='business').order_by('?').first()

        if not customer or not business:
            print("Skipping order creation: customer or business user not found.")
            return 
                   
        for i in range(5):
            Order.objects.update_or_create(
                id=i + 1,  
                 defaults={
                    'customer_user': User.objects.filter(type='customer').order_by('?').first(),
                    'business_user': User.objects.filter(type='business').order_by('?').first(),
                    'status': random.choice(['pending', 'completed', 'in_progress']),
                    'price': getattr(offer, 'price', Decimal('100.00')),
                    'title': random.choice(['Logo Design', 'Flyer Design', 'Webseite']),
                    'revisions': random.choice([1, 2, 3, -1]),
                    'features': [],
                    'offer_type': random.choice(['basic', 'standard', 'premium']),
                    'delivery_time_in_days': random.randint(3, 14),
                }

            )

        # Create sample reviews
        customer_users = list(User.objects.filter(type="customer"))
        business_users = list(User.objects.filter(type="business"))

        if not customer_users or not business_users:
            print("Skipping reviews: missing customer or business users.")
            return 

        if customer_users and business_users:
            used_pairs = set()
            max_reviews = 10
            created = 0
            attempts = 0

            while created < max_reviews and attempts < 100:
                reviewer = random.choice(customer_users)
                business_user = random.choice(business_users)
                pair = (reviewer.id, business_user.id)

                if pair in used_pairs:
                    attempts += 1
                    continue

                used_pairs.add(pair)

                Review.objects.update_or_create(
                    reviewer=reviewer,
                    business_user=business_user,
                    defaults={
                        'rating': random.randint(3, 5),
                        'description': random.choice([
                            "Sehr professioneller Service.",
                            "Top Qualität und schnelle Lieferung!",
                            "Würde ich definitiv weiterempfehlen.",
                            "Freundlich, kompetent und zuverlässig.",
                            "Hat alles perfekt geklappt!",
                            "Sehr zufrieden mit dem Ergebnis.",
                            f"Dies ist ein generischer Kommentar für Review {created+1}.",
                        ])
                    }
                )
                created += 1
                     

