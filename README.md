#  LAB 1: Environment and Agent Platform Setup

> Course: Intelligent Agents  
> Student: Theo Daniels   
> Institution: University of Ghana  
> Date: 29th January 2026  

---

##  Objective

This lab focuses on configuring a Python-based intelligent agent development environment using the SPADE framework and deploying a basic intelligent agent that communicates through the XMPP protocol.

---

## Technologies Used

- Python 3  
- SPADE Framework  
- GitHub Codespaces  
- XMPP Protocol  
- Prosody / Embedded SPADE Server  
- Visual Studio Code (Web)

---

##  Environment Setup

The following steps were followed to set up the development environment:

1. Launched GitHub Codespaces from the provided repository.
2. Verified Python installation using the terminal.
3. Installed the SPADE framework using `pip`.
4. Started the embedded XMPP server.
5. Created agent credentials.
6. Created a project directory for source files.

---




# LAB 2: Perception and Environment Modeling

##  Overview

This project implements an intelligent agent that perceives and monitors a simulated disaster environment using the SPADE framework in Python. The agent periodically senses environmental conditions, evaluates disaster severity, and generates event logs.

The system demonstrates how perception enables intelligent agents to make informed decisions in dynamic environments.

---

##  Objective

To implement agent perception of environmental and disaster-related events by simulating real-world conditions such as temperature, flooding, and smoke levels.

---

##  System Description

The project consists of three main components:

### 1. Disaster Environment
A simulated environment that dynamically generates:
- Temperature (°C)
- Water Level (cm)
- Smoke Level (%)

These values change randomly to represent disaster situations.

### 2. SensorAgent
The SensorAgent periodically monitors the environment. It:
- Collects sensor data
- Analyzes disaster risk
- Determines severity levels
- Logs detected events
- Displays output in real time

### 3. Event Logging System
All detected events and severity levels are stored in a text file (`event_log.txt`) for reporting and analysis.

---

## Technologies Used

- Python 3
- SPADE Framework
- XMPP Protocol
- AsyncIO
- File-based Logging

