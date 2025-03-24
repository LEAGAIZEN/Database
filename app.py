from flask import Flask, request, jsonify, render_template
import psycopg2

# Initialize Flask app
app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname="flaskdb",  # Replace with your database name
        user="postgres",   # Replace with your PostgreSQL username
        password="skullmaster123",  # Replace with your PostgreSQL password
        host="localhost", 
        port="5432"
    )
    return conn

# Route for Registration (GET method renders registration page)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required!"}), 400

        # Connect to the database and insert the user data (without password hashing)
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            return jsonify({"message": "Registration successful!"}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({"error": "Failed to register user: " + str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    return render_template("register.html")  # Correct path to the template

# Route for Login (GET method renders login page)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required!"}), 400

        # Connect to the database and check user credentials
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            stored_password = user[2]  # Assuming password is stored in the 3rd column

            if password == stored_password:
                return jsonify({
                    "message": "Login successful!",
                    "redirect": "https://expense-tracker-three-liard.vercel.app/"
                }), 200
            else:
                return jsonify({"error": "Invalid password!"}), 401  # Fixed issue here
        else:
            return jsonify({"error": "User not found!"}), 401  # Fixed issue here

    return render_template("login.html")

# Running the app
if __name__ == "__main__":
    app.run(debug=True)
