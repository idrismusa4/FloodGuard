# 🛡️ FloodGuardian AI

An intelligent flood prediction and emergency response system powered by NVIDIA Earth-2 climate digital twin technology.

## 🌊 Overview

FloodGuardian AI is a comprehensive flood monitoring and emergency response system that:

- **Predicts flood risks** using NVIDIA Earth-2 climate modeling
- **Sends automated SMS alerts** to communities and farmers
- **Provides evacuation routes** and emergency guidance
- **Allocates resources** automatically based on risk levels
- **Offers real-time dashboard** for emergency response coordination

## 🏗️ Architecture

```
FloodGuardian AI/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application entry
│   ├── config.py           # Configuration management
│   ├── database.py         # Supabase database client
│   ├── routes/             # API endpoints
│   │   ├── predictions.py  # Flood prediction endpoints
│   │   ├── alerts.py       # SMS alert management
│   │   ├── routes.py       # Evacuation routing
│   │   └── resources.py    # Resource allocation
│   ├── services/           # Core services
│   │   ├── earth2_service.py    # NVIDIA Earth-2 integration
│   │   ├── sms_service.py       # SMS gateway service
│   │   ├── routing_service.py   # Maps & routing service
│   │   └── resource_allocator.py # Resource management
│   └── jobs/
│       └── flood_monitor.py     # Automated monitoring job
├── frontend/               # React dashboard
│   ├── src/
│   │   ├── components/     # React components
│   │   └── services/       # API integration
│   └── public/
└── docker-compose.yml     # Container orchestration
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- Supabase account
- API keys for external services

### 1. Environment Setup

Copy and configure your environment variables:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-service-role-key

# NVIDIA Earth-2 API
EARTH2_API_KEY=your-nvidia-earth2-key

# SMS Gateway (Twilio/Africa's Talking)
SMS_GATEWAY_KEY=your-sms-provider-key

# Maps API (Optional - using OpenStreetMap for free)
MAPS_API_KEY=your-maps-api-key-optional
```

### 2. Database Setup

Set up your Supabase database schema:

```bash
cd backend
python database.py
```

This creates the necessary tables:
- `users` - Registered users and their locations
- `predictions` - Flood prediction history
- `alerts` - SMS alert logs
- `resources` - Resource allocation records

### 3. Run with Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 4. Run Manually (Development)

#### Backend:
```bash
cd backend
pip install -r ../requirements.txt
python main.py
```

#### Frontend:
```bash
cd frontend
npm install
npm start
```

#### Flood Monitor (Optional):
```bash
cd backend
python jobs/flood_monitor.py --continuous
```

## 📱 Features

### 🌊 Flood Prediction
- Real-time flood risk assessment
- Integration with NVIDIA Earth-2 climate models
- Historical prediction tracking
- Risk level categorization (Low/Medium/High)

### 🚨 Alert System
- Automated SMS alerts for high-risk areas
- Bulk messaging to affected regions
- Emergency alert broadcasting
- Alert history and analytics

### 🗺️ Evacuation Planning
- Dynamic evacuation route calculation
- Traffic condition monitoring
- Evacuation center locations
- Real-time route optimization

### 🚛 Resource Management
- Automatic resource allocation
- Inventory tracking across regions
- Cost estimation and budgeting
- Priority-based distribution

### 📊 Dashboard
- Real-time monitoring interface
- Regional risk visualization
- System status monitoring
- Quick action controls

## 🔧 API Endpoints

### Predictions
- `GET /predictions/{region}` - Get flood prediction
- `GET /predictions/history/{region}` - Prediction history
- `GET /predictions/` - Recent predictions

### Alerts
- `POST /alerts/send` - Send individual alert
- `POST /alerts/bulk` - Send bulk regional alerts
- `GET /alerts/history/{user_id}` - User alert history

### Routes
- `POST /routes/evacuation` - Get evacuation route
- `GET /routes/evacuation-centers/{region}` - Evacuation centers
- `GET /routes/traffic/{region}` - Traffic conditions

### Resources
- `POST /resources/allocate` - Allocate resources
- `GET /resources/status/{region}` - Resource status
- `GET /resources/inventory` - Global inventory

## 🌍 Supported Regions

Currently monitoring major Nigerian regions:
- Abuja, Lagos, Kano, Port Harcourt
- Ibadan, Kaduna, Benin City, Jos
- Maiduguri, Sokoto, Ilorin, Enugu
- And more...

## 🔑 API Integration

### NVIDIA Earth-2
```python
from services.earth2_service import earth2_service

prediction = earth2_service.get_flood_prediction("Lagos")
print(f"Risk Level: {prediction['risk_level']}")
```

### SMS Alerts
```python
from services.sms_service import sms_service

success = sms_service.send_sms("+234123456789", "Flood warning!")
```

### Resource Allocation
```python
from services.resource_allocator import resource_allocator

allocation = resource_allocator.allocate_resources("Abuja", 50000, 0.8)
```

## 🚀 Deployment

### Production Deployment

1. **Configure Environment**:
   ```bash
   export ENVIRONMENT=production
   export SUPABASE_URL=your-production-url
   # ... other production variables
   ```

2. **Deploy with Docker**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Set up Monitoring**:
   - Configure log aggregation
   - Set up health checks
   - Monitor resource usage

### Scaling Considerations

- Use Redis for caching predictions
- Implement rate limiting for API endpoints
- Set up load balancing for high traffic
- Configure database connection pooling

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs.floodguardian.ai](https://docs.floodguardian.ai)
- **Issues**: [GitHub Issues](https://github.com/your-org/floodguardian-ai/issues)
- **Discord**: [Join our community](https://discord.gg/floodguardian)

## 🙏 Acknowledgments

- **NVIDIA Earth-2** for climate modeling technology
- **Supabase** for database and backend services
- **OpenAI** for AI assistance in development
- **Nigerian Emergency Management Agency** for guidance

---

**Built with ❤️ for community safety and disaster preparedness.**

