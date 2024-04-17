
# Backend Server - Lunawa Elections Project

## Overview
This backend server is part of the Lunawa Elections system, designed to process and manage data for real-time election results. It handles the receipt and processing of ballot images from the Android app and provides APIs to fetch and display voting statistics.

## Django Models

### AndroidID
- **Purpose**: Tracks unique Android device IDs.
- **Fields**:
  - `name`: A unique identifier for the Android device.
  - `counter`: A counter to track the number of processed images from the device.

### Member
- **Purpose**: Represents members eligible for voting.
- **Fields**:
  - `loc`: Location identifier.
  - `name`: Name of the member.
  - `vaas`: Additional identifier or designation.
  - `votes`: Number of votes received.

### Image
- **Purpose**: Manages the images of ballots uploaded from the Android app.
- **Fields**:
  - `name`: The name of the image file.
  - `android_id`: A foreign key linking to the AndroidID.
  - `status`: Status of the image (e.g., Uploaded, Processed, Invalid).
  - `voted_members`: JSON field storing data on voted members.
- **Methods**:
  - `save()`: Custom save method that validates the image and triggers further processing.
  - `delete()`: Custom delete method that adjusts votes and cleans up resources.
  - `post_process()`: Handles image processing to extract voting data.

## Views in views.py

### delete_all()
- **Endpoint**: Deletes all images and related data for a given Android ID.
- **Method**: POST
- **Functionality**: This view handles the deletion of images and related Android IDs, including cleanup operations.

### stats()
- **Endpoint**: Provides statistics on votes.
- **Method**: GET
- **Functionality**: Returns a CSV format response with all members and their vote counts.

### streamlit()
- **Endpoint**: Integrates and starts a Streamlit session to display results in a dashboard.
- **Method**: GET
- **Functionality**: Starts the Streamlit server if not already running and embeds the Streamlit app in a webpage.

## API Endpoints (urls.py)

- **/delete_all/<android_id>/**: Endpoint to delete all data for a specified Android ID.
- **/stats/**: Endpoint to fetch voting statistics.
- **/streamlit/**: Endpoint to access the Streamlit dashboard.

## Setup and Installation

Ensure Django and other dependencies are installed:

```bash
cd backend-server
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:80
```

## Usage

Interact with the API using standard HTTP methods through tools like curl, Postman, or your browser to test and use the provided endpoints.

## Contributing

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request.

## Contact

For further information or to report issues, please contact the project team or open an issue in the main repository.

## License

This project is intended for educational use and is not licensed for commercial purposes.
