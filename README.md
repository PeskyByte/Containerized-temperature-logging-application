# **Containerized Microservices Data Collection and Analytics System**

## Project Overview:
This project aims to develop a containerized microservices-based system for data collection, analytics, and user authentication using Docker. The system will consist of multiple microservices, each handling a specific task such as data entry, analytics, and authentication. The services will interact with MySQL and MongoDB databases to store and retrieve data. Docker Compose will be used to orchestrate and manage the deployment of these microservices in a unified environment.

![image](https://github.com/user-attachments/assets/6eacaaef-1c88-42c1-a2c8-c3e00c4843b4)

## Objectives:
- Build individual Docker images for each service, including the data entry service, analytics service, and authentication service.
- Develop a `docker-compose.yml` file to manage the deployment of the system’s microservices.
- Ensure proper communication between microservices, databases, and web apps through a seamless containerized architecture.

## System Microservices:
1. **Enter Data (Web App)**:
   - A web application that allows users to collect and enter data (such as grades, temperatures, etc.).
   - The service validates user credentials through the **Authentication Service** before permitting data entry.
   - Once data is entered, it is written to the **MySQL DB Service**.

2. **Show Results (Web App)**:
   - A web application that presents simple analytics such as maximum, minimum, and average values.
   - The service validates user credentials through the **Authentication Service** before displaying the results.
   - It reads the required data from the **MongoDB Service**, which stores processed analytics data.

3. **Authentication Service**:
   - A service responsible for validating user credentials across the system.
   - Both the **Enter Data** and **Show Results** services rely on the Authentication Service to ensure secure access to their respective functionalities.

4. **Analytics Service**:
   - This service reads raw data from the **MySQL DB Service**, processes the data, and computes simple statistics like maximum, minimum, and average values.
   - The computed results are written to the **MongoDB Service**, which is then accessed by the **Show Results** service for display.

## Key Features:
- **Dockerized Microservices**:
  - Each service will have its own Docker image, ensuring isolated and efficient operation of individual components.
  
- **Docker Compose Integration**:
  - A `docker-compose.yml` file will be used to orchestrate the deployment of all services, allowing them to communicate effectively within a containerized environment.

- **Data Flow**:
  - Data collection begins in the **Enter Data** service and is stored in **MySQL DB**. The **Analytics Service** processes this data and stores the analytics in **MongoDB**, which is then accessed by the **Show Results** service.

- **Authentication**:
  - All data entry and results display operations are secured by the **Authentication Service**, ensuring that only authorized users can access the system.
