# King Blue News Feed

![King Blue Icon](https://github.com/salemae/king_blue_news_feed/blob/main/static/logo.png?raw=true)

King Blue News Feed is an open-source tool that allows you to manage, subscribe, and send email notifications for various RSS feed sources. Whether you want to keep your subscribers informed about the latest news, vulnerabilities, data leaks, or any other custom category, this application makes it easy to set up and send notifications.

## Features

- **Subscriber Management:** Add, edit, or remove subscribers to your email notifications.

- **SMTP Configuration:** Easily configure your SMTP server settings for sending emails.

- **Feed Source Management:** Add, edit, or remove RSS feed sources categorized into News, Vulnerabilities, Data Leakage, or Custom categories.

- **Email Notifications:** Automatically send email notifications to subscribers based on feed categories.

## Getting Started

Follow these steps to set up and run King Blue News Feed on your local environment:

1. Clone the repository from GitHub:
git clone https://github.com/yourusername/king-blue-news-feed.git


2. Create a Python virtual environment and install dependencies:
cd king-blue-news-feed
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt


3. Initialize the SQLite database:
python app.py


4. Open a web browser and access the application at `http://localhost:5000`.

## Contributing

We welcome contributions from the open-source community. Whether it's fixing bugs, adding new features, or improving the documentation, your contributions are highly appreciated. Please follow our [contributing guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

We would like to express our gratitude to the open-source community for their valuable contributions and support.

## Screenshots

Home Page and Subscripers Management
![Home Page and Subscripers Management](https://github.com/salemae/king_blue_news_feed/blob/main/screenshots/Screenshot_1.png?raw=true)


Feeds Management
![Feeds Management](https://github.com/salemae/king_blue_news_feed/blob/main/screenshots/Screenshot_2.png?raw=true)

Email Example

![Email Example](https://github.com/salemae/king_blue_news_feed/blob/main/screenshots/Screenshot_3.png?raw=true)