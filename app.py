from flask import Flask, request, render_template, redirect, url_for, flash, session
import feedparser
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask_session import Session


template_env = Environment(loader=FileSystemLoader('templates'))

app = Flask(__name__)
app.secret_key = 'n)-VzT{/1_0k)3sGFe?FD]/Y-X}COW'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
scheduler = BackgroundScheduler()

def schedule_send_email_job():
    scheduler = BackgroundScheduler()
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    
    # Check if the email_schedule table exists
    c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="email_schedule"')
    table_exists = c.fetchone()

    if table_exists:
        # The email_schedule table exists, so retrieve the scheduled time
        c.execute('SELECT hour, minute FROM email_schedule WHERE id = 1')
        schedule_data = c.fetchone()
        
        if schedule_data:
            # Use the scheduled hour and minute from the database
            hour, minute = schedule_data
            scheduler.add_job(send_email_background, 'cron', hour=hour, minute=minute)
        else:
            # There is no schedule data, use a default of every 24 hours
            scheduler.add_job(send_email_background, 'interval', hours=24)
    else:
        # The email_schedule table doesn't exist, use a default of every 24 hours
        scheduler.add_job(send_email_background, 'interval', hours=24)

    conn.close()
    scheduler.start()

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

    c.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE
        )
    ''')

    # Check if the keywords table is empty and insert the sample keyword if it is
    c.execute('SELECT COUNT(*) FROM keywords')
    count = c.fetchone()[0]

    if count == 0:
        sample_keyword = "thisisasamplewordtonotbemonitored"
        c.execute('INSERT INTO keywords (keyword) VALUES (?)', (sample_keyword,))

    # Predefine your categories
    categories = ["Main"]
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
    c.execute('''
        CREATE TABLE IF NOT EXISTS email_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hour INTEGER,
            minute INTEGER
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
    # Connect to the database
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()

    # Fetch the count of RSS feeds
    c.execute('SELECT COUNT(*) FROM feed_sources')
    rss_feeds_count = c.fetchone()[0]

    # Fetch the count of subscribers
    c.execute('SELECT COUNT(*) FROM subscribers')
    subscriber_count = c.fetchone()[0]

    # Fetch the count of categories
    c.execute('SELECT COUNT(*) FROM categories')
    category_count = c.fetchone()[0]

    # Fetch the count of keywords
    c.execute('SELECT COUNT(*) FROM keywords')
    keyword_count = c.fetchone()[0]

    # Fetch the list of subscribers
    c.execute('SELECT * FROM subscribers')
    subscribers = c.fetchall()

    # Close the database connection
    conn.close()

    # Pass the counts to the template
    return render_template('index.html', subscribers=subscribers, rss_feeds_count=rss_feeds_count, subscriber_count=subscriber_count, category_count=category_count, keyword_count=keyword_count)

@app.route('/manage_categories', methods=['GET'])
def manage_categories():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()

    # Fetch the list of existing categories
    c.execute('SELECT * FROM categories')
    categories = c.fetchall()

    conn.close()

    return render_template('manage_categories.html', categories=categories)

# New route to add a category
@app.route('/add_category', methods=['POST'])
def add_category():
    category_name = request.form['category_name']

    if category_name:
        conn = sqlite3.connect('subscribers.db')
        c = conn.cursor()

        # Check if the category already exists
        c.execute('SELECT name FROM categories WHERE name = ?', (category_name,))
        existing_category = c.fetchone()

        if not existing_category:
            # If the category does not exist, add it
            c.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
            conn.commit()
            conn.close()
            flash('Category added successfully!', 'success')
        else:
            conn.close()
            flash('Category already exists!', 'error')

    return redirect(url_for('manage_categories'))

# New route to remove a category
@app.route('/remove_category/<int:id>')
def remove_category(id):
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()

    # Check if there are feed sources associated with this category
    c.execute('SELECT * FROM feed_sources WHERE category = (SELECT name FROM categories WHERE id = ?)', (id,))
    feed_sources = c.fetchall()

    if feed_sources:
        conn.close()
        flash('Cannot remove the category as it is associated with feed sources!', 'error')
        return redirect(url_for('manage_categories'))

    # Remove the category
    c.execute('DELETE FROM categories WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Category removed!', 'success')
    return redirect(url_for('manage_categories'))

# New route to edit a category
@app.route('/edit_category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()

    if request.method == 'POST':
        new_category_name = request.form['new_category_name']

        # Check if the new category name is not empty
        if new_category_name:
            c.execute('UPDATE categories SET name = ? WHERE id = ?', (new_category_name, id))
            conn.commit()
            conn.close()
            flash('Category updated!', 'success')
            return redirect(url_for('manage_categories'))

    c.execute('SELECT * FROM categories WHERE id = ?', (id,))
    category = c.fetchone()
    conn.close()
    return render_template('edit_category.html', category=category)


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

@app.route('/configure_schedule', methods=['GET', 'POST'])
def configure_email_schedule():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()

    # Fetch the current email delivery schedule
    c.execute('SELECT * FROM email_schedule WHERE id=1')
    email_schedule = c.fetchone()

    if request.method == 'POST':
        # Get the email schedule settings from the form
        hour = int(request.form['hour'])
        minute = int(request.form['minute'])

        if email_schedule:
            # Update the existing email schedule
            c.execute('UPDATE email_schedule SET hour=?, minute=? WHERE id=1',
                      (hour, minute))
        else:
            # If it doesn't exist, create it
            c.execute('INSERT INTO email_schedule (id, hour, minute) VALUES (1, ?, ?)',
                      (hour, minute))

        conn.commit()
        flash('Email schedule configuration updated!', 'success')

        # Stop the current scheduler
        scheduler.shutdown()

        # Start a new scheduler with the updated schedule
        start_scheduler()

    # Fetch the current email schedule from the database
    if not email_schedule:
        email_schedule = [1, 0, 0]  # Initialize with default values if it doesn't exist

    conn.close()

    return render_template('configure_schedule.html', email_schedule=email_schedule)


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

@app.route('/manage_keywords', methods=['GET', 'POST'])
def manage_keywords():
    conn = sqlite3.connect('subscribers.db')  # Replace with your database file
    c = conn.cursor()

    if request.method == 'POST':
        if 'Add Keyword' in request.form:
            keyword = request.form['keyword']  # Updated to match the HTML form field name
            try:
                if keyword:
                    c.execute('INSERT INTO keywords (keyword) VALUES (?)', (keyword,))
                    conn.commit()
                    flash('Keyword added successfully!', 'success')
                else:
                    flash('Keyword cannot be empty!', 'error')
            except Exception as e:
                flash(f'Error adding keyword: {str(e)}', 'error')

    c.execute('SELECT keyword FROM keywords')
    keywords = [row[0] for row in c.fetchall()]

    conn.close()
    return render_template('manage_keywords.html', keywords=keywords)

@app.route('/remove_keyword/<string:id>', methods=['GET'])
def remove_keyword(id):
    conn = sqlite3.connect('subscribers.db')  # Replace with your database file
    c = conn.cursor()
    
    try:
        c.execute('DELETE FROM keywords WHERE keyword = ?', (id,))
        conn.commit()
        flash(f'Keyword "{id}" removed successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')

    conn.close()
    return redirect(url_for('manage_keywords'))


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

    # Fetch monitored keywords
    c.execute('SELECT word FROM keywords')
    monitored_keywords = [row[0] for row in c.fetchall()]

    # Fetch categories and their associated feed sources
    c.execute('SELECT * FROM categories')
    categories = c.fetchall()

    matching_articles = []

    for category in categories:
        category_name = category[1]  # Get the category name
        c.execute('SELECT id FROM feed_sources WHERE category = ?', (category_name,))
        source_ids = [row[0] for row in c.fetchall()]

        for source_id in source_ids:
            c.execute('SELECT url FROM feed_sources WHERE id = ?', (source_id,))
            source_url = c.fetchone()
            if source_url:
                source_feed = feedparser.parse(source_url[0])
                category_entries = source_feed.entries

                # Check if entries match the monitored keywords
                matching_articles.extend([
                    (entry, category_name) for entry in category_entries
                    if any(keyword.lower() in entry.get('title', '').lower() or keyword.lower() in entry.get('summary', '').lower() for keyword in monitored_keywords)
                ])

    # Send a separate email with matching articles to all subscribers
    if matching_articles:
        for subscriber in subscribers:
            matching_entries = [entry for entry, category_name in matching_articles if category_name]

            if matching_entries:
                send_notification(subscriber, 'Matching Articles', matching_entries)

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

def send_email_background():
    print('email sending background started')
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


def start_scheduler():
    # Start the scheduler
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('SELECT * FROM email_schedule WHERE id=1')
    email_schedule = c.fetchone()

    if email_schedule:
        # Retrieve the email schedule settings from the database
        hour, minute = email_schedule[1], email_schedule[2]

        # Add the scheduled job using the retrieved settings
        scheduler.add_job(send_email_background, 'cron', hour=hour, minute=minute)
    else:
        # If no schedule exists, use a default of every 24 hours
        scheduler.add_job(send_email_background, 'interval', hours=24)

    scheduler.start()
    conn.close()

if __name__ == '__main__':
    init_db()

    start_scheduler()
    app.run(host='0.0.0.0', port=5000, debug=True)
