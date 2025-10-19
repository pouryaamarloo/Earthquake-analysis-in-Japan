# Earthquake-Analysis-In-Japan
# 🌏 Earthquake Data Analysis in Japan

This project focuses on **analyzing earthquake data in Japan**, using a PostgreSQL database and Python tools such as **Pandas**, **NumPy**, and **SQLAlchemy**.  
It enables storing, cleaning, and analyzing seismic data to gain insights into **regional patterns, magnitudes, and depths** of earthquakes.

---

## 📊 Project Overview

Earthquakes occur frequently in Japan, and understanding their behavior can help identify trends in seismic activity.  
This project provides a modular, database-driven system to:
- Store earthquake records (time, location, depth, magnitude, etc.)
- Clean outlier or suspicious records
- Calculate statistical summaries by region
- Retrieve and visualize recent or high-magnitude earthquakes

---

## 🧱 Features

### 1. **Data Storage**
- Earthquake data is saved in a PostgreSQL database (`earthquakes` table).
- The `SQLConnector` class handles all database operations.

### 2. **Data Cleaning**
- Detects and removes suspicious rows using the Interquartile Range (IQR) method based on `magnitude` and `depth`.

### 3. **Analytical Queries**
- **Average Magnitude by Region**
- **Monthly Earthquake Counts per Region**
- **Recent 10 Strongest Earthquakes**
- **Depth Range (Max & Min) by Region**

### 4. **Error Handling**
- Every database operation includes exception handling.
- Prevents crashes from connection or SQL errors.

---

## 🗂️ Database Schema

| Column Name       | Type        | Description                          |
|-------------------|-------------|--------------------------------------|
| `id`              | SERIAL      | Unique record ID                     |
| `time`            | TIMESTAMP   | Date and time of earthquake          |
| `longitude`       | FLOAT       | Geographic longitude                 |
| `latitude`        | FLOAT       | Geographic latitude                  |
| `depth`           | FLOAT       | Depth of the earthquake (km)         |
| `magnitude`       | FLOAT       | Earthquake magnitude (Richter scale) |
| `region`          | TEXT        | Region name (e.g., Tokyo, Osaka)     |
| `source`          | TEXT        | Data source or sensor ID             |
| `distance_to_tokyo` | FLOAT     | Distance to Tokyo (in km)            |

---


