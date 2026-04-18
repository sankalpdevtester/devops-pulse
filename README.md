# DevOps Pulse: API Monitoring & Workflow Automation Platform

![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Description

DevOps Pulse is a comprehensive SaaS platform designed for development teams to monitor the health and performance of their APIs. It helps streamline operations by providing robust monitoring, insightful analytics, and intelligent workflow automation based on API status. This platform empowers teams to proactively identify issues, optimize performance, and automate critical responses, ensuring high availability and reliability for their services.

## Features

*   **Real-time API Health Monitoring:** Continuously track the uptime and responsiveness of your APIs.
*   **Performance Metrics Tracking:** Monitor key performance indicators such as latency, error rates, and throughput.
*   **Insightful Analytics Dashboards:** Visualize historical data and trends with customizable dashboards for better decision-making.
*   **Intelligent Workflow Automation:** Set up automated actions and notifications based on predefined API status changes (e.g., send alerts, trigger CI/CD pipelines).
*   **Customizable Alerting:** Configure alerts via various channels (email, Slack, webhooks) for immediate incident awareness.
*   **User-friendly Interface:** An intuitive and responsive UI built with Next.js and Tailwind CSS for a seamless user experience.
*   **Scalable Backend:** A high-performance FastAPI backend designed to handle extensive monitoring data.
*   **Lightweight Persistence:** Efficient data storage using SQLite for easy setup and development.

## Installation

To get DevOps Pulse up and running on your local machine, follow these steps:

### Prerequisites

Make sure you have the following installed:

*   Node.js (LTS version recommended) & npm/yarn
*   Python 3.8+ & pip
*   `venv` (Python virtual environment module, usually comes with Python)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/devops-pulse.git
cd devops-pulse
```

### 2. Backend Setup

Navigate to the `backend` directory, create a virtual environment, install dependencies, and run the server.

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
# On Windows: .\venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run the FastAPI server
# This will also create the SQLite database file if it doesn't exist.
uvicorn app.main:app --reload --port 8000
```

The backend API will be running at `http://localhost:8000`.

### 3. Frontend Setup

Open a new terminal, navigate to the `src` directory, install dependencies, and start the Next.js development server.

```bash
cd ../src

# Install Node.js dependencies
npm install # or yarn install

# Start the Next.js development server
npm run dev # or yarn dev
```

The frontend application will be running at `http://localhost:3000`.

## Usage

Once both the backend and frontend servers are running:

1.  Open your web browser and navigate to `http://localhost:3000`.
2.  Register a new user account or log in if you already have one.
3.  From the dashboard, you can:
    *   Add new API endpoints to monitor.
    *   Configure monitoring intervals and parameters.
    *   View real-time and historical performance metrics.
    *   Set up custom alert rules and notification channels.
    *   Define workflow automations triggered by specific API statuses.

Explore the intuitive interface to harness the full power of DevOps Pulse for your API monitoring and automation needs!

## Folder Structure

```
.
├── src/                          # Frontend (Next.js, React, TypeScript, Tailwind CSS)
│   ├── app/                      # Next.js app directory for routing and pages
│   ├── components/               # Reusable React components
│   ├── hooks/                    # Custom React hooks
│   ├── lib/                      # Utility functions and configurations
│   ├── types/                    # TypeScript type definitions
├── backend/                      # Backend (FastAPI, SQLite)
│   ├── app/                      # FastAPI application code
│   │   ├── api/                  # API endpoints (routers)
│   │   ├── models/               # SQLAlchemy models for database interaction
│   │   ├── schemas/              # Pydantic schemas for data validation and serialization
│   │   ├── crud/                 # CRUD (Create, Read, Update, Delete) operations
│   │   ├── core/                 # Core configurations, settings, and utilities
│   │   ├── tasks/                # Background tasks (e.g., for API monitoring)
│   │   └── main.py               # Main FastAPI application instance
│   └── requirements.txt          # Python dependencies
├── docs/                         # Project documentation
├── public/                       # Static assets for the frontend
└── README.md
```

## Contributing

We welcome contributions to DevOps Pulse! If you're interested in improving the platform, please follow these steps:

1.  **Fork** the repository on GitHub.
2.  **Clone** your forked repository to your local machine.
3.  Create a new **branch** for your feature or bug fix: `git checkout -b feature/your-feature-name`
4.  Make your **changes** and ensure tests pass (if applicable).
5.  **Commit** your changes with a descriptive message: `git commit -m "feat: Add new monitoring metric"`
6.  **Push** your branch to your forked repository: `git push origin feature/your-feature-name`
7.  Open a **Pull Request** to the `main` branch of the original repository.

Please ensure your code adheres to the existing style and conventions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.