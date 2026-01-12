# 🌍 AI Travel Itinerary Planner Bot
An intelligent AI-powered travel planning assistant that generates personalized itineraries with budget optimization, local recommendations, and hidden gems for multiple destinations worldwide.

## ✨ Features

### 🎯 Core Functionality
- **Smart Itinerary Generation** - AI-powered day-by-day travel plans
- **5 Major Destinations** - Paris, Tokyo, Bali, New York City, Rome
- **Budget Optimization** - Choose from budget, moderate, or luxury options
- **Interest-Based Planning** - Food, culture, nature, adventure, shopping
- **Weather-Aware** - Seasonal recommendations included

### 💎 Premium Features
- **Hidden Gems** - Discover local favorites and off-the-beaten-path locations
- **Restaurant Recommendations** - Curated dining suggestions with price ranges
- **Time Optimization** - Efficient scheduling with duration estimates
- **Cost Breakdown** - Detailed budget tracking per day and activity
- **Real-Time Statistics** - Track trips planned, budget, and destinations

### 🎨 User Experience
- **Natural Language Processing** - Conversational interface
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Real-Time Chat** - Interactive messaging system
- **Quick Actions** - Pre-built trip templates
- **Beautiful UI** - Modern gradient design with smooth animation


## 💬 Usage Examples

### Example Queries

Try these commands in the chat interface:

```
"Plan a 5-day trip to Paris"
"I want a budget trip to Tokyo"
"Create a 3-day romantic itinerary for Bali"
"Give me a food-focused tour of Rome"
"Plan a week in New York City on a luxury budget"
```

### Sample Output

```
✈️ YOUR PARIS, FRANCE ITINERARY
============================================================

Duration: 5 days
Budget Level: Moderate
Estimated Total Cost: EUR 750
Weather: 25°C ☀️

------------------------------------------------------------

📅 DAY 1

🌅 MORNING: Eiffel Tower
   ⏱️  Duration: 2-3 hours | 💰 Cost: EUR 26
   Type: Landmark

☀️ AFTERNOON: Louvre Museum
   ⏱️  Duration: 3-4 hours | 💰 Cost: EUR 17
   Type: Museum

🌙 EVENING DINNER: Le Comptoir du Relais
   🍽️  French | €€€ | Traditional French

💵 Estimated Day Budget: EUR 150

------------------------------------------------------------
[... continues for all days ...]

💎 HIDDEN GEMS & LOCAL TIPS

• Sainte-Chapelle for stunning stained glass
• Canal Saint-Martin for a local vibe
• Marché des Enfants Rouges (oldest market)
• Père Lachaise Cemetery
```

## 🛠️ Customization

### Adding New Destinations

Edit `app.py` and add to the `DESTINATIONS` dictionary:

```python
'london': {
    'name': 'London, UK',
    'currency': 'GBP',
    'avg_daily': 180,
    'weather': {
        'spring': '15°C ☀️',
        'summer': '22°C ☀️',
        'fall': '12°C 🍂',
        'winter': '7°C ❄️'
    },
    'attractions': [
        {
            'name': 'Big Ben',
            'type': 'landmark',
            'time': '1 hour',
            'cost': 0,
            'must_see': True
        },
        # Add more attractions...
    ],
    'restaurants': [
        {
            'name': 'Dishoom',
            'type': 'Indian',
            'price': '££',
            'specialty': 'Bombay cafe'
        },
        # Add more restaurants...
    ],
    'hidden_gems': [
        'Borough Market for food lovers',
        'Little Venice canal boats',
        # Add more gems...
    ]
}
```


## 📊 Technical Architecture

### Backend (Python/Flask)
- **Flask Framework** - Web server and routing
- **Regular Expressions** - Natural language parsing
- **Dictionary-based DB** - Fast data retrieval
- **REST API** - JSON-based communication

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **Vanilla JavaScript** - No frameworks needed
- **Fetch API** - Asynchronous communication

### Algorithm
1. **Input Analysis** - Parse user query for destination, days, budget, interests
2. **Data Filtering** - Select relevant attractions based on preferences
3. **Itinerary Generation** - Distribute activities across days
4. **Budget Calculation** - Apply budget multipliers and sum costs
5. **Response Formatting** - Generate readable text output

## 🎯 Skills Demonstrated

This project showcases:

- ✅ **Backend Development** - Flask web framework
- ✅ **Frontend Development** - HTML/CSS/JavaScript
- ✅ **API Design** - RESTful endpoints
- ✅ **Natural Language Processing** - Text parsing and analysis
- ✅ **Algorithm Design** - Itinerary optimization
- ✅ **Data Structures** - Complex nested dictionaries
- ✅ **UI/UX Design** - Responsive and intuitive interface
- ✅ **Software Architecture** - Clean, modular code

## 🐛 Known Issues & Roadmap

### Current Limitations
- Limited to 5 destinations (easily expandable)
- No persistent storage (trips not saved)
- Static weather data (can integrate real API)
- No user accounts

### Future Enhancements
- [ ] Real-time weather API integration
- [ ] Google Maps integration
- [ ] Flight and hotel price comparison
- [ ] User authentication and profile
- [ ] Save and share itineraries
- [ ] Multi-language support
- [ ] Mobile application
- [ ] AI model integration (GPT API)
- [ ] Photo galleries for destinations
- [ ] User reviews and ratings

**Made with ❤️ and Python**

*Last Updated: January 2026*
