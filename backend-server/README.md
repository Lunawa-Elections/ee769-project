
# Backend Server API and Models Documentation

## Overview
This README document provides a comprehensive overview of the backend structure for a Django-based project. It details the Django models used, the functionalities of various API endpoints, and the purpose of functions within the `views.py`. Additionally, it describes the processing logic encapsulated in the `processing.py` file.

## Models
### AndroidID
- `name`: CharField, a unique identifier for the Android device.
- `counter`: IntegerField, tracks the number of operations or transactions performed by this device.

### Member
- `loc`: CharField, location or designation of the member.
- `name`: CharField, the name of the member.
- `vaas`: CharField, an additional descriptor or role.
- `votes`: IntegerField, counts the votes or interactions by the member.

### Image
- `name`: CharField, the name of the image file.
- `android_id`: ForeignKey, links to an AndroidID.
- `status`: CharField, indicates the processing status of the image.
- `voted_members`: JSONField, stores information on members who have interacted with the image.
- Methods include save logic for processing the image and updating associated records, and delete logic for cleaning up resources.

## Endpoints
- **auth:** Handles authentication processes.
- **upload:** Manages the uploading of images, including validation and processing.
- **get_image:** Retrieves a specific image by its name.
- **counter:** Updates or retrieves the counter for a specified AndroidID.
- **delete:** Deletes all data associated with a given AndroidID, including related images.
- **stats:** Provides statistics or data about members, typically used for reporting.
- **streamlit:** Integrates with Streamlit for additional data visualization or interaction.

## API Endpoints and Function Descriptions in `views.py`

- **auth (request)**
  - **Purpose:** Handles user or device authentication. Validates credentials and manages sessions or tokens.
  - **Process:** Receives authentication data (e.g., username and password or device ID), validates it against the database or authentication service, and returns a session token or error message.
  - **Usage:** Typically used for login processes or API access control.

- **upload (request)**
  - **Purpose:** Manages the uploading of image files, ensuring they meet specified criteria for format and size, and processes them after validation.
  - **Process:** Parses the uploaded file, checks its validity (e.g., correct file type and not corrupted), and processes the image through various steps (like resizing or format conversion). Successful uploads update the database with the new image data.
  - **Usage:** Used whenever users need to upload images to the server, such as profile pictures or document scans.

- **get_image (request, img_name)**
  - **Purpose:** Retrieves and sends a specific image file by name to the requester.
  - **Process:** Looks up an image by its name in the database, checks access permissions, and serves the image file if found and authorized.
  - **Usage:** Useful in services that need to display or provide downloads of stored images.

- **counter (request, android_id)**
  - **Purpose:** Updates or retrieves the transaction count associated with a specific Android device ID.
  - **Process:** Increments the counter for the specified AndroidID or retrieves the current count from the database. Supports both POST and GET requests for updating or retrieving the counter, respectively.
  - **Usage:** Can be used to track or limit the number of operations performed by a device, useful in rate limiting or usage tracking.

- **delete (request, android_id)**
  - **Purpose:** Deletes all records and data associated with a given AndroidID from the database.
  - **Process:** Removes the AndroidID record, associated image records, and any other related data, ensuring thorough data cleanup to prevent data leaks.
  - **Usage:** Important for maintaining user privacy and complying with data protection regulations, especially when a user requests deletion of their data.

- **stats (request)**
  - **Purpose:** Provides statistical data about the members, such as counts of votes or interactions.
  - **Process:** Aggregates data from the `Member` model and formats it into a readable or exportable format (like CSV), often used for generating reports or analytics.
  - **Usage:** Useful for administrative or analytical purposes to understand user engagement and other metrics.

- **streamlit (request)**
  - **Purpose:** Integrates a Streamlit application for enhanced data visualization or interaction, typically running on a separate server or service.
  - **Process:** Checks if Streamlit is already running; if not, it starts the Streamlit server. Constructs a URL to the Streamlit service and embeds it in the Django application for user access.
  - **Usage:** Used for providing advanced interactive visualizations and dashboards to users, enhancing the user experience and providing deeper insights into the data.

## Processing Logic in `processing.py`

The `processing.py` module is a critical component of the system, handling various aspects of image processing and management. Below are the detailed functionalities implemented within this script:

- **Image Validation**
  - **Purpose:** Ensures that all uploaded images meet specific pre-defined standards necessary for further processing.
  - **Process:** Checks the integrity and format of each image using algorithms that might include checks for image size, file type (e.g., JPEG, PNG), and potentially harmful content. This step is crucial to prevent processing of corrupted or unsupported files.
  - **Usage:** Automatically invoked when new images are uploaded, ensuring only valid images are stored and processed.

- **Image Enhancements and Modifications**
  - **Purpose:** Improves the quality of images or alters them to meet certain specifications required by the application.
  - **Process:** Depending on the requirements, this could include resizing images, adjusting brightness and contrast, applying filters, or cropping images to fit certain dimensions. These modifications are performed using libraries such as OpenCV or PIL (Python Imaging Library).
  - **Usage:** Enhancements can be applied to user-uploaded images for aesthetic improvement or to prepare images for machine learning tasks or other analytical processes.

- **Image Management Utilities**
  - **Purpose:** Provides support functions to help manage image files within the application, including saving, retrieving, and deleting operations.
  - **Process:** Functions include methods to save processed images in a designated storage location, retrieve them for display or further processing, and delete them when no longer needed or upon user request. These utilities ensure that image data is handled efficiently, maintaining the integrity and availability of data within the system.
  - **Usage:** Used throughout the application wherever image file operations are required, ensuring consistent handling of all image files.

This module serves as a backbone for image-related operations, ensuring that the application can handle a variety of tasks related to image processing, from basic validation to complex enhancements. It supports the main application by ensuring robust and reliable image data management.

## Conclusion
This README serves as a guideline and documentation for managing the backend services of the specified Django project. It aids in understanding the database models, API functionalities, and the logic involved in processing data, particularly images. This documentation is crucial for effective maintenance and scaling of the backend services.

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