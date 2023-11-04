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


## Docker Installation

You can also run the King Blue Newsletter App using Docker for containerized deployment. Follow these steps to set up the app with Docker:

1. Clone the repository:

   ```shell
   git clone https://github.com/salemae/king_blue_news_feed.git
   cd king_blue_news_feed
   ```

2. Build a Docker image from the provided Dockerfile. Make sure you have Docker installed on your system.

   ```shell
   docker build -t king-blue-app .```

3. Once the image is built, you can run the app in a Docker container. Replace your_port with the desired port for the app (e.g., 8080):

   ```shell
   docker run -p your_port:5000 -d king-blue-app```

   This command maps the app's internal port (5000) to the specified port on your host system.

4. Access the app by opening a web browser and navigating to the following URL:

   ```shell
   http://localhost:your_port```

5. To stop and remove the Docker container when you're done, use the following command:

   ```shell
   docker stop $(docker ps -a -q)
   docker rm $(docker ps -a -q)```
    Now, the King Blue Newsletter App should be up and running in a Docker container, accessible at the specified port on your local machine.


Build a Docker image from the provided Dockerfile. Make sure you have Docker installed on your system.

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
