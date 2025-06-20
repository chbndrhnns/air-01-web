# 💰 IT Salary Calculator

An interactive data visualization application based on JetBrains Developer Ecosystem Survey 2024 salary data. Built with FastAPI backend and Streamlit frontend.

## 🏗️ Project Structure

```
air-01-web/
├── backend/           # FastAPI backend application
│   ├── __init__.py
│   └── main.py        # API endpoints and server
├── frontend/          # Streamlit frontend application
│   └── streamlit_app.py # Interactive dashboard
├── shared/            # Shared utilities and models
│   ├── __init__.py
│   ├── models.py      # Pydantic data models
│   └── data_loader.py # Data loading utilities
├── data/              # Data files
│   └── calculatorData.json # JetBrains salary survey data
├── main.py            # Application entry point
├── pyproject.toml     # Project configuration
└── README.md          # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd /Users/jo/src/scratch/air-01-web
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

### Running the Application

The application consists of two components that need to be running simultaneously:

#### Option 1: Using the main entry point (Recommended)

1. **Start the backend server:**
   ```bash
   uv run python main.py backend
   ```
   This will start the FastAPI server on http://localhost:8000

2. **In a new terminal, start the frontend:**
   ```bash
   uv run python main.py frontend
   ```
   This will start the Streamlit app on http://localhost:8501

3. **Open your browser and visit:**
   - Frontend: http://localhost:8501 (main application)
   - Backend API docs: http://localhost:8000/docs (API documentation)

#### Option 2: Running components directly

1. **Backend:**
   ```bash
   cd backend
   uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Frontend:**
   ```bash
   uv run streamlit run frontend/streamlit_app.py --server.port 8501
   ```

## 🛠️ Technology Stack

- **Backend:** FastAPI with Pydantic models
- **Frontend:** Streamlit with Plotly visualizations
- **Data Processing:** Pandas
- **Package Management:** uv
- **Data Visualization:** Plotly Express & Plotly Graph Objects

## 📊 Features

- **Interactive Filters:** Filter by country, programming language, and experience level
- **Real-time Statistics:** Average, median salary, salary range, and sample size
- **Data Visualizations:**
  - Salary distribution histogram
  - Experience level box plots
- **Data Export:** Download filtered data as CSV
- **Responsive Design:** Clean, modern interface with custom styling

## 🔧 API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /` - API information
- `GET /countries` - List all available countries
- `GET /languages` - List programming languages (optionally filtered by country)
- `GET /experience-levels` - List experience levels (optionally filtered)
- `GET /salary-data` - Get salary entries with optional filters
- `GET /salary-stats` - Get aggregated salary statistics

## 📁 Data Source

The application uses salary data from the JetBrains Developer Ecosystem Survey 2024, stored in `data/calculatorData.json`. The data includes:

- **Countries:** Various countries worldwide
- **Programming Languages:** JavaScript/TypeScript, Python, Java, etc.
- **Experience Levels:** <1 year, 1-2 years, 3-5 years, etc.
- **Salary Information:** Annual salaries in USD

## 🎨 Design Reference

The application design is based on:
- [Figma Design](https://www.figma.com/design/pmxb4N3i62YgFVzE5Nq74b/IT-Salary-Calculator?node-id=0-1&p=f) (password: AirRPP_homework2025)
- [JetBrains Reference Page](https://www.jetbrains.com/lp/devecosystem-it-salary-calculator/)

## 🧪 Development

### Project Commands

```bash
# Show help
uv run python main.py

# Start backend only
uv run python main.py backend

# Start frontend only  
uv run python main.py frontend

# Install new dependencies
uv add package-name

# Run tests (when available)
uv run pytest
```

### Architecture

- **Separation of Concerns:** Clear separation between backend API, frontend UI, and shared utilities
- **RESTful API:** Clean REST endpoints with proper HTTP status codes
- **Data Models:** Pydantic models for type safety and validation
- **Error Handling:** Comprehensive error handling with user-friendly messages
- **CORS Configuration:** Properly configured for frontend-backend communication

## 🤝 Contributing

1. Follow the existing code style and patterns
2. Ensure both backend and frontend work together seamlessly
3. Test your changes with different filter combinations
4. Update documentation if needed

## 📝 License

This project is created for educational/demonstration purposes based on the JetBrains Developer Ecosystem Survey 2024 data.