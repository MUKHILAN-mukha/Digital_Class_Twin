# Digital Class Twin System

A role-based Digital Twin platform for academic performance visualization.

## Members
- Member 1: Event Tracking App (React)
- Member 2: Backend API (PostgreSQL + Python/FastAPI)
- Member 3: ML Engine (Event → Digital Twin)
- Member 4: Dashboard (Read-only Visualization)

## Architecture
- Events are raw and immutable
- ML processes events into digital twins
- Dashboards read only digital twins

## Current Status
- Member 1: Completed
- Member 3: Completed
- Member 4: Completed
- Member 2: In progress

## Security
- JWT-based authentication
- Role-based access control
- No raw events exposed to dashboards
