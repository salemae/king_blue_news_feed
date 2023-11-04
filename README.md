# King Blue Newsletter App

![Insert Logo Here - Replace with Your App Logo](https://github.com/salemae/king_blue_news_feed/blob/main/static/logo.png)

The King Blue Newsletter App is a Flask-based web application designed to manage and send newsletters to subscribers. It allows users to subscribe to newsletters, manage subscribers, configure SMTP settings, schedule email delivery, and organize feed sources into categories. The app periodically sends newsletters to subscribers based on the configured schedule and feed sources.

![Screenshot 1 - Home Page](https://github.com/salemae/king_blue_news_feed/blob/main/screenshots/Screenshot_2.png)
![Screenshot 2 - Subscriber Management](https://github.com/salemae/king_blue_news_feed/blob/main/screenshots/Screenshot_3.png)

## Features

- **Subscriber Management**: Users can subscribe to newsletters by providing their email addresses. Subscribers can be edited and removed by administrators.

- **Feed Source Management**: you can add, edit, and remove RSS feed sources. Feed sources can be organized into categories.

- **Category Management**: you can create, edit, and remove categories for feed sources.

- **SMTP Configuration**: you can configure SMTP settings to enable email delivery.

- **Email Schedule Configuration**: you can configure the schedule for sending newsletters. This includes specifying the hour and minute for email delivery.

- **Automatic Email Delivery**: The app uses a background scheduler to automatically send newsletters to subscribers based on the configured schedule. Newsletters are customized for each category and include the latest feed entries.

- **Keywords Monitoring**: The app has a keywords monitoring list which will alert you when a news article matches your keywords.


## Installation Using `install.sh` Script

### Prerequisites

- Docker (for Docker Install)
- Python 3
- Python virtual environment (`venv` module)
- pip package manager

### Installation Steps

1. Clone the Kingblue repository:

   ```shell
   git clone https://github.com/salemae/king_blue_news_feed.git
   ```

2. Run the provided installation script:
      ```shell
   sudo sh install.sh
   ```


3. Choose the installation method:
- For Docker Install (Option 1), the Kingblue app will be available at: [http://localhost:8888](http://localhost:8888)
- For Local Install (Option 2), the Kingblue app will be available at: [http://localhost:5000](http://localhost:5000)
- Default login credentials for Kingblue:
  - Username: admin
  - Password: admin



## Manual Installation

You can also run the King Blue Newsletter App using Docker for containerized deployment. Follow these steps to set up the app with Docker:

1. Clone the Kingblue repository:

   ```shell
   git clone https://github.com/salemae/king_blue_news_feed.git
   ```

2. Create a Python virtual environment:
    ```shell
   python3 -m venv venv
   
   source venv/bin/activate
   ```

3. Install the required packages from `requirements.txt`:
    ```shell
   pip install -r requirements.txt
   ```


4. Run the Kingblue app:

    ```shell
   python app.py
   ```

5. Access Kingblue in your web browser at: [http://localhost:5000](http://localhost:5000)

6. Default login credentials for Kingblue:
- Username: admin
- Password: admin

That's it! You have successfully installed Kingblue.

For more information and updates, visit the [Kingblue GitHub repository](https://github.com/salemae/king_blue_news_feed).

## Usage

1. Access the web application at [http://localhost:5000](http://localhost:5000).

2. Use the web interface to manage subscribers, feed sources, categories, SMTP settings, and email schedule.

3. Subscribers can subscribe to newsletters by providing their email addresses.

4. Feed sources can be organized into categories. Categories can be created, edited, and removed.

5. Configure SMTP settings to enable email delivery.

6. Configure the email delivery schedule to control when newsletters are sent.

7. Customize the news by specifing keywords via keywords managements

8. The app will automatically send newsletters to subscribers based on the configured schedule. Each newsletter includes the latest feed entries from the specified categories.

## Directory Structure

- `app.py`: The main Flask application.
- `templates/`: HTML templates for the web pages.
- `static/`: Static assets (CSS, images, etc.).
- `requirements.txt`: List of Python dependencies.
- `subscribers.db`: SQLite database for storing subscriber data and configuration.

## Contributing

If you want to contribute to this project, please fork the repository, create a new branch, make your changes, and submit a pull request.
