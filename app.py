from flask import Flask, request, render_template, redirect, url_for, flash
import feedparser
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import os

template_env = Environment(loader=FileSystemLoader('templates'))

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS smtp_config (
            id INTEGER PRIMARY KEY,
            server TEXT,
            port INTEGER,
            user TEXT,
            password TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # Predefine your categories
    categories = ["News", "Vulnerabilities", "Data Leakage", "Custom"]
    for category in categories:
        # Check if the category already exists
        c.execute('SELECT name FROM categories WHERE name = ?', (category,))
        if not c.fetchone():
            c.execute('INSERT INTO categories (name) VALUES (?)', (category,))

    c.execute('''
        CREATE TABLE IF NOT EXISTS feed_sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            url TEXT,
            category TEXT,
            FOREIGN KEY (category) REFERENCES categories (name)
        )
    ''')

    conn.commit()
    conn.close()




# Subscribe route
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    if email:
        conn = sqlite3.connect('subscribers.db')
        c = conn.cursor()
        c.execute('INSERT INTO subscribers (email) VALUES (?)', (email,))
        conn.commit()
        conn.close()
        flash('Subscribed successfully!', 'success')
    return redirect(url_for('index'))

# Edit subscriber route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        new_email = request.form['email']
        conn = sqlite3.connect('subscribers.db')
        c = conn.cursor()
        c.execute('UPDATE subscribers SET email = ? WHERE id = ?', (new_email, id))
        conn.commit()
        conn.close()
        flash('Subscriber updated!', 'success')
        return redirect(url_for('index'))
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('SELECT * FROM subscribers WHERE id = ?', (id,))
    subscriber = c.fetchone()
    conn.close()
    return render_template('edit.html', subscriber=subscriber)

# Remove subscriber route
@app.route('/remove/<int:id>')
def remove(id):
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('DELETE FROM subscribers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Subscriber removed!', 'success')
    return redirect(url_for('index'))

# Index route
@app.route('/')
def index():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('SELECT * FROM subscribers')
    subscribers = c.fetchall()
    conn.close()
    return render_template('index.html', subscribers=subscribers)

@app.route('/config', methods=['GET', 'POST'])
def configure_smtp():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()

    # Check if SMTP configuration with id=1 exists
    c.execute('SELECT * FROM smtp_config WHERE id=1')
    smtp_config = c.fetchone()

    if request.method == 'POST':
        smtp_server = request.form['server']
        smtp_port = int(request.form['port'])
        smtp_user = request.form['user']
        smtp_password = request.form['password']

        if smtp_config:
            # Update the existing SMTP configuration
            c.execute('UPDATE smtp_config SET server=?, port=?, user=?, password=? WHERE id=1',
                      (smtp_server, smtp_port, smtp_user, smtp_password))
        else:
            # If it doesn't exist, create it
            c.execute('INSERT INTO smtp_config (id, server, port, user, password) VALUES (1, ?, ?, ?, ?)',
                      (smtp_server, smtp_port, smtp_user, smtp_password))

        conn.commit()
        flash('SMTP configuration updated!', 'success')

    # Fetch the current SMTP configuration from the database
    if not smtp_config:
        smtp_config = [1, '', 0, '', '']  # Initialize with default values if it doesn't exist

    conn.close()

    return render_template('config.html', smtp_config=smtp_config)


# Modify the route to fetch both feed sources and categories
@app.route('/manage_feeds', methods=['GET'])
def manage_feeds():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    
    # Fetch feed sources
    c.execute('SELECT id, name, url, category FROM feed_sources')
    feed_sources = c.fetchall()

    c.execute('SELECT name FROM categories')
    categories = [row[0] for row in c.fetchall()]

    conn.close()

    return render_template('manage_feeds.html', feed_sources=feed_sources, categories=categories)



@app.route('/add_feed_source', methods=['POST'])
def add_feed_source():
    name = request.form['name']
    url = request.form['url']
    category = request.form['category']  # Get the selected category from the form

    if name and url and category:
        conn = sqlite3.connect('subscribers.db')
        c = conn.cursor()
        c.execute('INSERT INTO feed_sources (name, url, category) VALUES (?, ?, ?)', (name, url, category))
        conn.commit()
        conn.close()
        flash('Feed source added successfully!', 'success')
    return redirect(url_for('manage_feeds'))



# Edit feed source route
@app.route('/edit_source/<int:id>', methods=['GET', 'POST'])
def edit_source(id):
    if request.method == 'POST':
        new_name = request.form['name']
        new_url = request.form['url']
        conn = sqlite3.connect('subscribers.db')
        c = conn.cursor()
        c.execute('UPDATE feed_sources SET name = ?, url = ? WHERE id = ?', (new_name, new_url, id))
        conn.commit()
        conn.close()
        flash('Feed source updated!', 'success')
        return redirect(url_for('manage_feeds'))
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('SELECT * FROM feed_sources WHERE id = ?', (id,))
    source = c.fetchone()
    conn.close()
    return render_template('edit_source.html', source=source)

# Remove feed source route
@app.route('/remove_source/<int:id>')
def remove_source(id):
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('DELETE FROM feed_sources WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Feed source removed!', 'success')
    return redirect(url_for('index'))


@app.route('/configure_sources/<int:category_id>', methods=['GET', 'POST'])
def configure_sources(category_id):
    if request.method == 'POST':
        selected_sources = request.form.getlist('sources')
        conn = sqlite3.connect('subscribers.db')
        c = conn.cursor()

        # Remove existing associations for the category
        c.execute('DELETE FROM category_sources WHERE category_id = ?', (category_id,))

        # Add new associations for the category
        for source_id in selected_sources:
            c.execute('INSERT INTO category_sources (category_id, source_id) VALUES (?, ?)', (category_id, source_id))

        conn.commit()
        conn.close()
        flash('Feed sources configured for the category!', 'success')

    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
    category = c.fetchone()
    c.execute('SELECT * FROM feed_sources')
    sources = c.fetchall()
    c.execute('SELECT source_id FROM category_sources WHERE category_id = ?', (category_id,))
    selected_sources = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template('configure_sources.html', category=category, sources=sources, selected_sources=selected_sources)


def get_feed_sources():
    conn = sqlite3.connect('subscribers.db')  # Replace 'your_database.db' with your database file
    c = conn.cursor()
    c.execute('SELECT * FROM feed_sources')
    feed_sources = c.fetchall()
    conn.close()
    return feed_sources

def get_categories():
    conn = sqlite3.connect('subscribers.db')  # Replace 'your_database.db' with your database file
    c = conn.cursor()
    c.execute('SELECT * FROM categories')
    categories = c.fetchall()
    conn.close()
    return categories

# Helper functions
def get_subscribers():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('SELECT email FROM subscribers')
    subscribers = [row[0] for row in c.fetchall()]
    conn.close()
    return subscribers


@app.route('/send_email', methods=['GET'])
def send_email():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()

    # Fetch subscribers' emails
    c.execute('SELECT email FROM subscribers')
    subscribers = [row[0] for row in c.fetchall()]

    # Fetch categories and their associated feed sources
    c.execute('SELECT * FROM categories')
    categories = c.fetchall()

    for category in categories:
        category_name = category[1]  # Get the category name
        c.execute('SELECT id FROM feed_sources WHERE category = ?', (category_name,))
        source_ids = [row[0] for row in c.fetchall()]

        category_feeds = []

        for source_id in source_ids:
            c.execute('SELECT url FROM feed_sources WHERE id = ?', (source_id,))
            source_url = c.fetchone()
            if source_url:
                source_feed = feedparser.parse(source_url[0])
                category_feeds.append(source_feed)

        # Check if there are feeds in the category
        if category_feeds:
            # Extract entries from the first source (you may want to aggregate all entries from multiple sources)
            entries = category_feeds[0]['entries']

            # Check if there are entries in the category
            if entries:
                # Send email per category with all feeds associated with that category to all subscribers
                for subscriber in subscribers:
                    send_notification(subscriber, category_name, entries)

    conn.close()
    flash('Emails sent successfully!', 'success')
    return redirect(url_for('index'))


def send_notification(email, category_name, category_feeds):
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()

    # Fetch the SMTP configuration from the database
    c.execute('SELECT * FROM smtp_config WHERE id=1')
    smtp_config = c.fetchone()

    if smtp_config:
        smtp_server, smtp_port, sender_email, sender_password = smtp_config[1:5]

        # Create an environment for Jinja2 to load email templates
        template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))

        # Load the email template
        template = env.get_template('newsletter_template.html')

        # Render the template with the category name and feeds
        html_content = template.render(category_name=category_name, news_list=category_feeds)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = f'King Blue | {category_name}'

        msg.attach(MIMEText(html_content, 'html'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            server.quit()
        except Exception as e:
            print(f"Error sending email to {email}: {str(e)}")



if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
