from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# In-memory storage for demonstration purposes
users = {}


# Chat response for the communication with the user
chat_responses = {
    "hello": "Hi there! Firstimer, Welcome, Would you like to know what GeoCities is about?",
    "yes": "GeoCities is a web hosting service that allows users to create their own websites. To be part of a specific community, please answer the following question about yourself. What would you mostly do on a Friday holiday with R100,000 in your bank? \n- Party\n- Stay home\n- Movies\n- Date\n- Drive\n- Shopping",
    "no": "Alright! How else can I assist you today?",
    "bye": "Goodbye! Have a great day!",
    "how are you": "I'm just a bunch of code, but I'm functioning as expected!",
    "help": "You can ask me about GeoCities, or just say hello!",
    "party": "You belong to Las Vegas. Las Vegas is a neighborhood associated with entertainment and nightlife. Click 'Go to Neighborhoods' to explore GeoCities ",
    "stay home": "You might enjoy any of our communities, take your pick on the next screen, just Click 'Go to Neighborhoods' to explore GeoCities!",
    "movies": "You belong to Hollywood. Hollywood is a neighborhood where you could create or find websites about movies, TV shows, and celebrities. Click 'Go to Neighborhoods' to explore GeoCities",
    "date": "You belong to Paris. Paris is dedicated to art and literature, where you could explore or share works of art, poetry, and novels about love. Click 'Go to Neighborhoods' to explore GeoCities",
    "drive": "You belong at MotorCity. Motorcity is a neighborhood for people who like Cars, trucks, motorcycles. Click 'Go to Neighborhoods' to explore GeoCities",
    "shopping": "You belong to GeoCities Market. GeoCities Market is a neighborhood where members sell and buy products. Click 'Go to Neighborhoods' to explore GeoCities",
}

# routing for the systems to navigate through different interfaces.
@app.route('/')
def index():
    if 'username' in session:
        user = users[session['username']]
        if user['new_user']:
            return redirect(url_for('chatbot'))
        elif not user.get('completed_chatbot', False):
            return redirect(url_for('chatbot'))
        else:
            return redirect(url_for('neighborhoods'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists!')
        else:
            users[username] = {
                'password': generate_password_hash(password),
                'new_user': True,
                'completed_chatbot': False,
                'neighborhood': None
            }
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)

        if user is None or not check_password_hash(user['password'], password):
            flash('Invalid username or password! if you have not register click "Register" on the navigation bar and Register')
        else:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/chatbot')
def chatbot():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = users[session['username']]
    user['new_user'] = False
    return render_template('chatbot.html')


@app.route('/chatbot_response', methods=['POST'])
def chatbot_response():
    if 'username' not in session:
        return jsonify({"response": "Please log in first!"}), 401

    user_input = request.json.get('message').strip().lower()  # Convert user input to lowercase
    response = chat_responses.get(user_input,
                                  "Sorry, I don't understand that. You can ask me about GeoCities, or just say hello!")

    # Handle special responses that imply neighborhood assignment
    if user_input in ["party", "movies", "date", "study", "shopping", "stay at home"]:
        users[session['username']]['completed_chatbot'] = True
        users[session['username']]['neighborhood'] = response.split(" ")[-1].rstrip('.')

    return jsonify({"response": response})


@app.route('/neighborhoods', methods=['GET', 'POST'])
def neighborhoods():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = users[session['username']]
    if not user.get('completed_chatbot', False):
        return redirect(url_for('chatbot'))
    if request.method == 'POST':
        selected_neighborhood = request.form['neighborhood']
        user['neighborhood'] = selected_neighborhood
        return redirect(url_for('geocities'))
    return render_template('neighborhoods.html')


@app.route('/geocities')
def geocities():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = users[session['username']]
    neighborhood = user.get('neighborhood', 'None selected')
    return render_template('geocities.html', neighborhood=neighborhood)


if __name__ == '__main__':
    app.run(debug=True)
