# CryptoFlow: Real-time Crypto Data Pipeline

## 🚀 Overview
CryptoFlow is a real-time cryptocurrency data pipeline built with FastAPI, Apache Airflow, PostgreSQL, and MinIO. It fetches live crypto prices, stores them in a database, and provides a FastAPI-powered API to retrieve data and visualize price trends.

## 🛠 Tech Stack
- **FastAPI** - REST API for serving crypto data
- **Apache Airflow** - Task scheduling for data collection
- **PostgreSQL** - Database for storing crypto prices
- **MinIO** - Object storage for raw data
- **Docker & Docker Compose** - Containerized deployment
- **Pandas, Matplotlib & Seaborn** - Data analysis & visualization

## 📸 Screenshots
![CryptoFlow Logo](logo.png)

## 📦 Installation
### Prerequisites
- Docker & Docker Compose installed

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cryptoflow.git && sudo chmod -R 777 cryptoflow && cd cryptoflow
   ```
2. Start the services:
   ```bash
   docker-compose up -d --build
   ```
3. Access the services:
   - FastAPI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Airflow UI: [http://localhost:8080](http://localhost:8080)
   - MinIO UI: [http://localhost:9001](http://localhost:9001)
   
## 📊 API Usage
### Get Crypto Price Graph
```bash
GET /graph?monnaie=BTC
```
Returns a PNG image of the Bitcoin price trend.


## 🤝 Contributing
Feel free to submit issues or pull requests.

## 📩 Contact
- **Malt**: [Your Profile](https://www.malt.fr/profile/sachametzger1)
- **GitHub**: [Your GitHub](https://github.com/LeGrandAkira)
- **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/sacha-metzger)

