from flask import Flask, render_template, request, jsonify
from datetime import datetime
import re

app = Flask(__name__)

# Destination Database
DESTINATIONS = {
    'paris': {
        'name': 'Paris, France',
        'currency': 'EUR',
        'avg_daily': 150,
        'weather': {
            'spring': '15°C ☀️',
            'summer': '25°C ☀️',
            'fall': '12°C 🌥️',
            'winter': '5°C ❄️'
        },
        'attractions': [
            {'name': 'Eiffel Tower', 'type': 'landmark', 'time': '2-3 hours', 'cost': 26, 'must_see': True},
            {'name': 'Louvre Museum', 'type': 'museum', 'time': '3-4 hours', 'cost': 17, 'must_see': True},
            {'name': 'Notre-Dame Cathedral', 'type': 'landmark', 'time': '1-2 hours', 'cost': 0, 'must_see': True},
            {'name': 'Sacré-Cœur', 'type': 'landmark', 'time': '1-2 hours', 'cost': 0, 'must_see': False},
            {'name': 'Arc de Triomphe', 'type': 'landmark', 'time': '1 hour', 'cost': 13, 'must_see': True},
            {'name': "Musée d'Orsay", 'type': 'museum', 'time': '2-3 hours', 'cost': 16, 'must_see': False},
            {'name': 'Versailles Palace', 'type': 'landmark', 'time': '4-5 hours', 'cost': 27, 'must_see': True}
        ],
        'restaurants': [
            {'name': 'Le Comptoir du Relais', 'type': 'French', 'price': '€€€', 'specialty': 'Traditional French'},
            {'name': "L'As du Fallafel", 'type': 'Middle Eastern', 'price': '€', 'specialty': 'Best falafel'},
            {'name': 'Breizh Café', 'type': 'Creperie', 'price': '€€', 'specialty': 'Authentic crepes'}
        ],
        'hidden_gems': [
            'Sainte-Chapelle for stunning stained glass',
            'Canal Saint-Martin for a local vibe',
            'Marché des Enfants Rouges (oldest market)',
            'Père Lachaise Cemetery'
        ]
    },
    'tokyo': {
        'name': 'Tokyo, Japan',
        'currency': 'JPY',
        'avg_daily': 120,
        'weather': {
            'spring': '15°C 🌸',
            'summer': '28°C ☀️',
            'fall': '18°C 🍂',
            'winter': '7°C ❄️'
        },
        'attractions': [
            {'name': 'Senso-ji Temple', 'type': 'temple', 'time': '1-2 hours', 'cost': 0, 'must_see': True},
            {'name': 'Shibuya Crossing', 'type': 'landmark', 'time': '30 min', 'cost': 0, 'must_see': True},
            {'name': 'Meiji Shrine', 'type': 'temple', 'time': '1-2 hours', 'cost': 0, 'must_see': True},
            {'name': 'Tokyo Skytree', 'type': 'landmark', 'time': '2 hours', 'cost': 25, 'must_see': False},
            {'name': 'Tsukiji Outer Market', 'type': 'market', 'time': '2 hours', 'cost': 0, 'must_see': True},
            {'name': 'TeamLab Borderless', 'type': 'museum', 'time': '2-3 hours', 'cost': 35, 'must_see': False},
            {'name': 'Harajuku & Takeshita Street', 'type': 'shopping', 'time': '2 hours', 'cost': 0, 'must_see': True}
        ],
        'restaurants': [
            {'name': 'Ichiran Ramen', 'type': 'Ramen', 'price': '¥', 'specialty': 'Tonkotsu ramen'},
            {'name': 'Sukiyabashi Jiro', 'type': 'Sushi', 'price': '¥¥¥¥', 'specialty': 'World-famous sushi'},
            {'name': 'Genki Sushi', 'type': 'Sushi', 'price': '¥¥', 'specialty': 'Conveyor belt sushi'}
        ],
        'hidden_gems': [
            'Omoide Yokocho (Memory Lane) for yakitori',
            'Nakameguro for cherry blossoms',
            'Kagurazaka for traditional atmosphere',
            'Yanaka Ginza shopping street'
        ]
    },
    'bali': {
        'name': 'Bali, Indonesia',
        'currency': 'IDR',
        'avg_daily': 60,
        'weather': {
            'spring': '28°C ☀️',
            'summer': '27°C 🌧️',
            'fall': '28°C ☀️',
            'winter': '27°C 🌧️'
        },
        'attractions': [
            {'name': 'Tanah Lot Temple', 'type': 'temple', 'time': '2 hours', 'cost': 5, 'must_see': True},
            {'name': 'Ubud Monkey Forest', 'type': 'nature', 'time': '2 hours', 'cost': 7, 'must_see': True},
            {'name': 'Tegalalang Rice Terraces', 'type': 'nature', 'time': '2 hours', 'cost': 3, 'must_see': True},
            {'name': 'Uluwatu Temple', 'type': 'temple', 'time': '2 hours', 'cost': 5, 'must_see': True},
            {'name': 'Sacred Monkey Forest', 'type': 'nature', 'time': '1-2 hours', 'cost': 7, 'must_see': False},
            {'name': 'Mount Batur Sunrise Trek', 'type': 'adventure', 'time': '6 hours', 'cost': 35, 'must_see': True}
        ],
        'restaurants': [
            {'name': 'Locavore', 'type': 'Fine Dining', 'price': '$$$', 'specialty': 'Modern Indonesian'},
            {'name': 'Warung Babi Guling', 'type': 'Local', 'price': '$', 'specialty': 'Suckling pig'},
            {'name': "Naughty Nuri's", 'type': 'BBQ', 'price': '$$', 'specialty': 'Famous ribs'}
        ],
        'hidden_gems': [
            'Tukad Cepung Waterfall for unique photos',
            'Jatiluwih Rice Terraces (less crowded)',
            'Sidemen Valley for authentic village life',
            'Amed for snorkeling and diving'
        ]
    },
    'newyork': {
        'name': 'New York City, USA',
        'currency': 'USD',
        'avg_daily': 200,
        'weather': {
            'spring': '15°C ☀️',
            'summer': '28°C ☀️',
            'fall': '15°C 🍂',
            'winter': '2°C ❄️'
        },
        'attractions': [
            {'name': 'Statue of Liberty', 'type': 'landmark', 'time': '3-4 hours', 'cost': 24, 'must_see': True},
            {'name': 'Central Park', 'type': 'park', 'time': '2-3 hours', 'cost': 0, 'must_see': True},
            {'name': 'Times Square', 'type': 'landmark', 'time': '1 hour', 'cost': 0, 'must_see': True},
            {'name': 'Empire State Building', 'type': 'landmark', 'time': '2 hours', 'cost': 44, 'must_see': True},
            {'name': 'Metropolitan Museum', 'type': 'museum', 'time': '3-4 hours', 'cost': 30, 'must_see': True},
            {'name': 'Brooklyn Bridge', 'type': 'landmark', 'time': '1-2 hours', 'cost': 0, 'must_see': True},
            {'name': 'High Line Park', 'type': 'park', 'time': '1-2 hours', 'cost': 0, 'must_see': False}
        ],
        'restaurants': [
            {'name': "Joe's Pizza", 'type': 'Pizza', 'price': '$', 'specialty': 'Classic NY slice'},
            {'name': "Katz's Delicatessen", 'type': 'Deli', 'price': '$$', 'specialty': 'Pastrami sandwich'},
            {'name': 'Le Bernardin', 'type': 'Fine Dining', 'price': '$$$$', 'specialty': 'Seafood'}
        ],
        'hidden_gems': [
            'Roosevelt Island Tramway for views',
            'The Cloisters museum in Upper Manhattan',
            'Smorgasburg food market (weekends)',
            "St. Patrick's Cathedral"
        ]
    },
    'rome': {
        'name': 'Rome, Italy',
        'currency': 'EUR',
        'avg_daily': 130,
        'weather': {
            'spring': '18°C ☀️',
            'summer': '30°C ☀️',
            'fall': '20°C 🌥️',
            'winter': '10°C 🌧️'
        },
        'attractions': [
            {'name': 'Colosseum', 'type': 'landmark', 'time': '2-3 hours', 'cost': 18, 'must_see': True},
            {'name': 'Vatican Museums', 'type': 'museum', 'time': '3-4 hours', 'cost': 20, 'must_see': True},
            {'name': 'Trevi Fountain', 'type': 'landmark', 'time': '30 min', 'cost': 0, 'must_see': True},
            {'name': 'Pantheon', 'type': 'landmark', 'time': '1 hour', 'cost': 0, 'must_see': True},
            {'name': 'Roman Forum', 'type': 'landmark', 'time': '2 hours', 'cost': 18, 'must_see': True},
            {'name': 'Spanish Steps', 'type': 'landmark', 'time': '30 min', 'cost': 0, 'must_see': False}
        ],
        'restaurants': [
            {'name': 'Roscioli', 'type': 'Italian', 'price': '€€€', 'specialty': 'Carbonara'},
            {'name': 'Pizzarium', 'type': 'Pizza', 'price': '€', 'specialty': 'Pizza al taglio'},
            {'name': 'Trastevere Trattorias', 'type': 'Italian', 'price': '€€', 'specialty': 'Traditional Roman'}
        ],
        'hidden_gems': [
            'Villa Borghese gardens',
            'Appian Way ancient road',
            'Aventine Hill keyhole view',
            'Testaccio neighborhood for food'
        ]
    }
}


class TravelBot:
    """AI Travel Itinerary Planner Bot"""

    def __init__(self):
        self.stats = {
            'trips_planned': 0,
            'total_budget': 0,
            'destinations': 0
        }

    def analyze_request(self, user_input):
        """Analyze user input to extract travel preferences"""
        lower_input = user_input.lower()

        request = {
            'destination': None,
            'days': 3,
            'budget': 'moderate',
            'interests': [],
            'season': 'spring'
        }

        # Detect destination
        for key, dest in DESTINATIONS.items():
            if key in lower_input or dest['name'].lower() in lower_input:
                request['destination'] = key
                break

        # Detect number of days
        days_match = re.search(r'(\d+)\s*(day|night)', lower_input)
        if days_match:
            request['days'] = min(int(days_match.group(1)), 7)

        # Detect budget level
        if any(word in lower_input for word in ['budget', 'cheap', 'affordable']):
            request['budget'] = 'budget'
        elif any(word in lower_input for word in ['luxury', 'expensive', 'premium']):
            request['budget'] = 'luxury'

        # Detect interests
        if any(word in lower_input for word in ['food', 'restaurant', 'eat', 'dining']):
            request['interests'].append('food')
        if any(word in lower_input for word in ['museum', 'art', 'culture', 'history']):
            request['interests'].append('culture')
        if any(word in lower_input for word in ['nature', 'outdoor', 'hiking', 'park']):
            request['interests'].append('nature')
        if any(word in lower_input for word in ['adventure', 'active', 'sport']):
            request['interests'].append('adventure')
        if 'shopping' in lower_input:
            request['interests'].append('shopping')

        # Detect season
        if 'summer' in lower_input:
            request['season'] = 'summer'
        elif 'winter' in lower_input:
            request['season'] = 'winter'
        elif any(word in lower_input for word in ['fall', 'autumn']):
            request['season'] = 'fall'

        return request

    def generate_itinerary(self, request):
        """Generate a complete travel itinerary"""
        dest_key = request['destination']
        if not dest_key or dest_key not in DESTINATIONS:
            return None

        dest = DESTINATIONS[dest_key]

        # Calculate budget
        budget_multiplier = {'budget': 0.7, 'moderate': 1.0, 'luxury': 1.5}
        daily_budget = dest['avg_daily'] * budget_multiplier[request['budget']]
        total_budget = daily_budget * request['days']

        # Select attractions
        attractions = dest['attractions'].copy()

        # Filter by interests if specified
        if request['interests']:
            filtered = [a for a in attractions
                        if any(interest in a['type'] or interest in a['name'].lower()
                               for interest in request['interests'])]
            if filtered:
                attractions = filtered

        # Sort by must_see priority
        attractions.sort(key=lambda x: (not x['must_see'], x['cost']))

        # Generate day-by-day plan
        itinerary = []
        attractions_per_day = max(2, len(attractions) // request['days'])

        for day in range(request['days']):
            start_idx = day * attractions_per_day
            end_idx = min(start_idx + attractions_per_day, len(attractions))
            day_attractions = attractions[start_idx:end_idx]

            day_plan = {
                'day': day + 1,
                'morning': day_attractions[0] if len(day_attractions) > 0 else None,
                'afternoon': day_attractions[1] if len(day_attractions) > 1 else None,
                'evening': dest['restaurants'][day % len(dest['restaurants'])],
                'budget': round(daily_budget, 2)
            }
            itinerary.append(day_plan)

        # Update stats
        self.stats['trips_planned'] += 1
        self.stats['total_budget'] += int(total_budget)
        self.stats['destinations'] += 1

        return {
            'destination': dest,
            'itinerary': itinerary,
            'total_budget': round(total_budget, 2),
            'weather': dest['weather'][request['season']],
            'hidden_gems': dest['hidden_gems'],
            'request': request
        }

    def format_itinerary(self, plan):
        """Format itinerary as readable text"""
        dest = plan['destination']
        req = plan['request']

        output = f"✈️ YOUR {dest['name'].upper()} ITINERARY\n"
        output += "=" * 60 + "\n\n"
        output += f"Duration: {req['days']} days\n"
        output += f"Budget Level: {req['budget'].title()}\n"
        output += f"Estimated Total Cost: {dest['currency']} {plan['total_budget']}\n"
        output += f"Weather: {plan['weather']}\n"
        output += "\n" + "-" * 60 + "\n\n"

        for day in plan['itinerary']:
            output += f"📅 DAY {day['day']}\n\n"

            if day['morning']:
                m = day['morning']
                output += f"🌅 MORNING: {m['name']}\n"
                output += f"   ⏱️  Duration: {m['time']} | 💰 Cost: {dest['currency']} {m['cost']}\n"
                output += f"   Type: {m['type'].title()}\n\n"

            if day['afternoon']:
                a = day['afternoon']
                output += f"☀️ AFTERNOON: {a['name']}\n"
                output += f"   ⏱️  Duration: {a['time']} | 💰 Cost: {dest['currency']} {a['cost']}\n"
                output += f"   Type: {a['type'].title()}\n\n"

            if day['evening']:
                e = day['evening']
                output += f"🌙 EVENING DINNER: {e['name']}\n"
                output += f"   🍽️  {e['type']} | {e['price']} | {e['specialty']}\n\n"

            output += f"💵 Estimated Day Budget: {dest['currency']} {day['budget']}\n"
            output += "\n" + "-" * 60 + "\n\n"

        output += "💎 HIDDEN GEMS & LOCAL TIPS\n\n"
        for gem in plan['hidden_gems']:
            output += f"• {gem}\n"

        output += "\n🎒 TRAVEL TIPS\n\n"
        tips = [
            "Book attractions online in advance for skip-the-line access",
            "Use public transportation to save money",
            "Try local street food for authentic experiences",
            "Download offline maps before traveling",
            "Learn a few basic phrases in the local language"
        ]
        for tip in tips:
            output += f"• {tip}\n"

        return output


# Initialize bot
bot = TravelBot()


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Analyze request
    travel_request = bot.analyze_request(user_message)

    # Generate response
    if travel_request['destination']:
        plan = bot.generate_itinerary(travel_request)
        if plan:
            response = {
                'type': 'itinerary',
                'message': bot.format_itinerary(plan),
                'plan': plan,
                'stats': bot.stats
            }
        else:
            response = {
                'type': 'error',
                'message': 'Sorry, I could not generate an itinerary for that destination.'
            }
    else:
        available = ', '.join([d['name'] for d in DESTINATIONS.values()])
        response = {
            'type': 'help',
            'message': f"""I'd love to help you plan a trip! 

Available destinations: {available}

Try asking:
• "Plan a 5-day trip to Paris"
• "I want a budget trip to Tokyo"  
• "Create a 3-day romantic itinerary for Bali"
• "Give me a food-focused tour of Rome"

Which destination interests you?""",
            'stats': bot.stats
        }

    return jsonify(response)


@app.route('/stats')
def stats():
    """Get bot statistics"""
    return jsonify(bot.stats)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
