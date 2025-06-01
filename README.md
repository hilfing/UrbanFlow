# UrbanFlow: Smart Traffic Light System with Dynamic Priority Management

UrbanFlow is a smart traffic light management system designed to prioritize emergency vehicles and optimize traffic
flow. The system uses real-time data, machine learning, and the Google Maps API to enhance urban traffic efficiency.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

## Project Overview

UrbanFlow is an innovative traffic management solution that integrates live traffic signal data and GPS information from
emergency vehicles to dynamically adjust traffic lights. The system uses a priority algorithm to ensure emergency
vehicles receive the necessary priority at intersections, reducing response times and improving traffic flow.

The project includes a [Voluntary Data Collector](https://github.com/PaulStudios/Voluntary-Data-Collector), which allows
users to submit their GPS data voluntarily, enriching the dataset used for traffic analysis and prediction. This
additional data source enhances the accuracy and reliability of the UrbanFlow system by providing a broader view of
traffic patterns.

## Features

- **Real-Time Traffic Data Collection**: Collects live traffic signal status and GPS data every 30 seconds.
- **Voluntary Data Collection**: Utilizes the Voluntary Data Collector app to gather additional GPS data from users,
  increasing the robustness of traffic predictions.
- **Priority Management**: Assigns dynamic priority scores to vehicles based on type and proximity to intersections.
- **Machine Learning Integration**: Predicts vehicle routes using historical and real-time data.
- **Google Maps API**: Utilizes Maps API for accurate ETA calculations and route predictions.
- **Traffic Signal Optimization**: Automatically updates and manages traffic signals based on processed data.
- **User-Friendly Interface**: Mobile application for emergency vehicle drivers with real-time updates and
  notifications.
- **Scalable Architecture**: Supports high volumes of data with robust performance monitoring and load balancing.

## System Architecture

![UrbanFlow Algorithm](UrbanFlow%20Flowchart.png)

The UrbanFlow system consists of several key components:

1. **UrbanFlow Server**: Central hub for processing incoming data and managing traffic priorities.
2. **API Server**: Handles GPS data collection and processing from voluntary data submissions.
3. **Database**: Stores traffic and GPS data, along with machine learning models.
4. **Priority Algorithm**: Calculates priority scores and schedules signal changes.
5. **Machine Learning Model**: Predicts vehicle routes and updates models regularly.
6. **Data Collection**: Collects GPS from users to further train Route Prediction AI.

## Voluntary Data Collector

The [Voluntary Data Collector](https://github.com/PaulStudios/Voluntary-Data-Collector) is an integral part of
UrbanFlow, designed to enhance data collection by allowing users to contribute their GPS data. This app helps gather a
diverse set of traffic data points, which are used to improve traffic predictions and system efficiency. Users can
easily download the app, register, and start contributing data to the system.

## Installation

To set up the UrbanFlow project locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hilfing/urbanflow.git
   cd urbanflow
   ```

2. **Install Dependencies**:
   Ensure you have Python and pip installed. Then, run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Private Keys**:
   Create a `.env` file in the root directory with your API keys:
   ```plaintext
   DATABASE_URL_ASYNC=postgresql+asyncpg://user:password@host/dbname
   DATABASE_URL=postgresql://user:password@host/dbname
   API_URL = <Voluntary Data Collector API URL>
   GOOGLE_MAPS_API_KEY=your_google_maps_apikey
   SECRET_KEY=secret_key_used_for_hashing
   ALGORITHM=HS256
   ```

4. **Set Up the Database** (UNDER DEVELOPMENT):
   Initialize the database using:
   ```bash
   alembic upgrade head
   ```

5. **Run the Server**:
   Start the server with:
   ```bash
   python main.py train_and_evaluate --download
   python main.py runserver
   ```

## Usage

1. **Mobile App**: Install the UrbanFlow app on emergency vehicle drivers' phones to send GPS data.
2. **Voluntary Data Collector**: Encourage users to download and use the Voluntary Data Collector app to submit GPS data
   voluntarily.
3. **Web Interface**: Access the UrbanFlow web dashboard to monitor traffic and manage configurations.
4. **Notifications**: Receive real-time notifications on traffic signal updates and priority routes.

## Contributing

We welcome contributions to UrbanFlow! To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Submit a pull request.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## Acknowledgments

- This project was developed as part of the ISEF project by HilFing.
- Special thanks to my mentor for guidance and support.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Contact

For any questions or suggestions, feel free to reach out:

- **Email**: [HilFIng](mailto:contact@hilfing.dev)
- **GitHub**: [HilFing](https://github.com/hilfing)
