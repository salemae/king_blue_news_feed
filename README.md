# King Blue News Feed

![King Blue Icon](youricon.png)

King Blue News Feed is an open-source tool that allows you to manage, subscribe, and send email notifications for various RSS feed sources. Whether you want to keep your subscribers informed about the latest news, vulnerabilities, data leaks, or any other custom category, this application makes it easy to set up and send notifications.

## Features

- **Subscriber Management:** Add, edit, or remove subscribers to your email notifications.

- **SMTP Configuration:** Easily configure your SMTP server settings for sending emails.

- **Feed Source Management:** Add, edit, or remove RSS feed sources categorized into News, Vulnerabilities, Data Leakage, or Custom categories.

- **Category Management:** Create, edit, or remove categories to organize your feed sources.

- **Category-Source Associations:** Associate feed sources with categories, allowing you to send notifications based on categories.

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

## Usage

1. **Subscriber Management:**
- Visit the `/subscribe` route to subscribe new users.
- Visit the `/edit/<subscriber_id>` route to edit existing subscribers.
- Visit the `/remove/<subscriber_id>` route to remove subscribers.

2. **SMTP Configuration:**
- Configure SMTP settings at `/config`.

3. **Feed Source Management:**
- Manage feed sources at `/manage_feeds`.
- Add new feed sources using the `/add_feed_source` route.
- Edit and remove feed sources using the `/edit_source/<feed_source_id>` and `/remove_source/<feed_source_id>` routes.

4. **Category Management:**
- Create, edit, and remove categories at `/manage_feeds`.

5. **Category-Source Associations:**
- Configure associations at `/configure_sources/<category_id>`.

6. **Sending Email Notifications:**
- Trigger the email notifications by visiting the `/send_email` route.

## Contributing

We welcome contributions from the open-source community. Whether it's fixing bugs, adding new features, or improving the documentation, your contributions are highly appreciated. Please follow our [contributing guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

We would like to express our gratitude to the open-source community for their valuable contributions and support.

