# IronQueue ⚙️

**Distributed job scheduler for high-reliability asynchronous task execution.**

**[Live Demo](https://ironqueue.vercel.app/)**

### **Overview**

IronQueue is a distributed task management system built to handle asynchronous workflows with strict persistence. It utilizes a producer-consumer architecture to manage, execute, and monitor long-running background jobs with automated failure recovery.

### **The Stack**

* **Python (FastAPI)**: RESTful API for job submission and state management.
* **Redis**: High-throughput message broker for the task queue.
* **PostgreSQL**: Relational storage for job history, metadata, and persistent state.
* **Alembic**: Database migration tool for version-controlled schema evolution.
* **Docker**: Orchestrated environment for worker, reaper, and API services.

### **Core Features**

* **Persistence & Reliability**: Every job is backed by **PostgreSQL** to ensure no data loss during system restarts or worker crashes.
* **Automated Reaping**: Implemented a "Reaper" service that monitors the queue for orphaned tasks and automatically resets stalled jobs for retry.
* **Real-Time Monitoring**: Integrated dashboard for tracking job lifecycles—from pending and active to successful or failed—with full execution logs.

### **Quick Start**

```bash
# Spin up the Database, Redis, and Workers
docker-compose up -d

# Run database migrations
alembic upgrade head

```
