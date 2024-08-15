import os
from flask import Flask, request, render_template, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Load MySQL credentials from environment variables
mysql_user = os.getenv("MYSQL_USER")
mysql_password_file = os.getenv("MYSQL_PASSWORD_FILE")
mysql_database_name = os.getenv("MYSQL_DATABASE")

# Read the MySQL password from the file
with open(mysql_password_file) as f:
    mysql_password = f.readline().strip()  # .strip() to remove any extraneous newline characters

# Function to get a database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="mysql",
            user=mysql_user,
            password=mysql_password,
            database=mysql_database_name
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Define a route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for searching clips
@app.route('/search', methods=['GET'])
def search_clips():
    clips = []
    search_term = request.args.get('query', '')
    if search_term:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Unable to connect to the database'}), 500

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT * FROM Clips
            WHERE MATCH(title, creator_name) AGAINST(%s IN BOOLEAN MODE);
            """
            cursor.execute(query, (search_term,))
            clips = cursor.fetchall()
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            connection.close()

    return render_template('search.html', clips=clips)

@app.route('/clip/<clip_id>')
def clip(clip_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    main_query = """
        SELECT c.clip_id, c.thumbnail_url, c.title, c.creator_name, c.view_count, c.clip_date,
               b.broadcaster_name, g.game_name
        FROM Clips c
        JOIN Broadcasters b ON c.broadcaster_id = b.broadcaster_id
        JOIN Games g ON c.game_id = g.game_id
        WHERE c.clip_id = %s
    """
    related_clips_query = """
    SELECT 
        clip_id, 
        title, 
        thumbnail_url, 
        ABS(TIMESTAMPDIFF(MINUTE, clip_date, %s)) AS date_diff,
        TIMESTAMPDIFF(MINUTE, clip_date, %s) AS date_diff_signed
    FROM Clips
        WHERE ABS(TIMESTAMPDIFF(MINUTE, clip_date, %s)) >= 3
    ORDER BY 
        date_diff ASC
    LIMIT 10;
    """
    cursor.execute(main_query, (clip_id,))
    clip = cursor.fetchone()
    cursor.execute(related_clips_query, (clip["clip_date"], clip["clip_date"], clip["clip_date"]))
    related_clips = cursor.fetchall()
    cursor.close()

    if clip:
        # Construct the clip URL from the thumbnail URL
        index = clip['thumbnail_url'].find('-preview')
        clip_url = clip['thumbnail_url'][:index] + '.mp4'
        clip['clip_url'] = clip_url
        clip['clip_date'] = clip['clip_date'].strftime('%Y-%m-%d %H:%M:%S')
        return render_template('clip.html', clip=clip, related_clips=related_clips)
    else:
        return "Clip not found", 404

if __name__ == '__main__':
    app.run(debug=False)
