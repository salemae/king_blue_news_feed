# King Blue Newsletter App

![Insert Logo Here - Replace with Your App Logo](https://github.com/salemae/king_blue_news_feed/blob/main/static/logo.png)

The King Blue Newsletter App is a Flask-based web application designed to manage and send newsletters to subscribers. It allows users to subscribe to newsletters, manage subscribers, configure SMTP settings, schedule email delivery, and organize feed sources into categories. The app periodically sends newsletters to subscribers based on the configured schedule and feed sources.

![Screenshot 1 - Home Page](https://github.com/salemae/king_blue_news_feed/blob/main/screenshots/Screenshot_2.png)
![Screenshot 2 - Subscriber Management](https://github.com/salemae/king_blue_news_feed/blob/main/screenshots/Screenshot_3.png)

## Features

- **Subscriber Management**: Users can subscribe to newsletters by providing their email addresses. Subscribers can be edited and removed by administrators.

- **Feed Source Management**: Administrators can add, edit, and remove RSS feed sources. Feed sources can be organized into categories.

- **Category Management**: Administrators can create, edit, and remove categories for feed sources.

- **SMTP Configuration**: Administrators can configure SMTP settings to enable email delivery.

- **Email Schedule Configuration**: Administrators can configure the schedule for sending newsletters. This includes specifying the hour and minute for email delivery.

- **Automatic Email Delivery**: The app uses a background scheduler to automatically send newsletters to subscribers based on the configured schedule. Newsletters are customized for each category and include the latest feed entries.


## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your_username/king-blue-newsletter-app.git
   cd king-blue-newsletter-app

## Usage

1. Access the web application at [http://localhost:5000](http://localhost:5000).

2. Use the web interface to manage subscribers, feed sources, categories, SMTP settings, and email schedule.

3. Subscribers can subscribe to newsletters by providing their email addresses.

4. Feed sources can be organized into categories. Categories can be created, edited, and removed.

5. Configure SMTP settings to enable email delivery.

6. Configure the email delivery schedule to control when newsletters are sent.

7. The app will automatically send newsletters to subscribers based on the configured schedule. Each newsletter includes the latest feed entries from the specified categories.

## Directory Structure

- `app.py`: The main Flask application.
- `templates/`: HTML templates for the web pages.
- `static/`: Static assets (CSS, images, etc.).
- `requirements.txt`: List of Python dependencies.
- `subscribers.db`: SQLite database for storing subscriber data and configuration.

## Contributing

If you want to contribute to this project, please fork the repository, create a new branch, make your changes, and submit a pull request.
