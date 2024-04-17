
# Lunawa Elections Project

## Project Overview
The Lunawa Elections Project is designed to facilitate paper-based offline elections by enabling real-time counts of votes through a dashboard. Developed for the NGO Lunawa Helping Hand in Mumbai, this project aims to streamline the election process and reduce human errors, making the voting process more efficient and transparent.

## Features
- **Real-time Election Vote Updates:** A dashboard displays the count of votes in real-time.
- **Automatic Ballot Processing:** The system automatically processes images of ballots to determine votes.
- **Android Application:** An Android app is used to capture and submit images of the ballots.

## Technology Stack
- **Django:** Used for the backend to process ballot images and maintain votes in a SQLite database.
- **Streamlit:** Serves as the frontend to display real-time voting results in a web browser.
- **Java:** The Android application is developed in Java, with XML for styling.

## Setup and Installation

### Backend Setup
```bash
cd backend-server
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:80
```

### Android Application Setup
- **Android Studio:**
  - Open the project in Android Studio.
  - Sync the project with Gradle files.
  - Build the project using `Build > Build Bundle(s) / APK(s) > Build APK(s)`.
  - Run the app on an emulator or a physical device.
- **APK Installation:**
  - Install the APK file from the root directory directly onto an Android device.

## Usage
1. **Android App:**
   - Install the app and enter the password `0000` to access.
   - In the next activity, capture the image of a voted ballot. The image will automatically be uploaded and processed by the server. The parsed modified image will be displayed on the mobile view.

2. **Dashboard:**
   - Visit [Lunawa Elections Dashboard](http://lunawaelections.southindia.cloudapp.azure.com/) to view the real-time updates of vote counts.

3. **Note:**
   - In order to use a local server, you need to change the `serverUrl` in `strings.xml` on Android and rebuild the application with the new URL. Currently, the server is hosted on Azure at the URL: [http://lunawaelections.southindia.cloudapp.azure.com/](http://lunawaelections.southindia.cloudapp.azure.com/).

## Contributing
This project is developed as a part of the course project for EE 769 Introduction to Machine Learning at IIT Bombay. Contributions, bug reports, and feature requests are welcome. Please feel free to fork the repository and submit pull requests.

## Contact
- **Name:** Dhruv Jain
- **Roll Number:** 22M0828
- For direct queries, please open an issue in this repository or contact via the institute's email service.

## License
This project is currently unlicensed and is intended for educational purposes and non-commercial use only.
