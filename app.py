from flask import Flask, render_template, redirect, url_for, request
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Function to generate image using OpenAI API
def fetch_image(prompt):
    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        return response.json()
    else:        
        return None

# Route for the main page
@app.route('/')
def index():
    image_url = request.args.get('image_url')
    return render_template('index.html', image_url=image_url)

# Route to handle form submission
@app.route('/submit-form', methods=['POST'])
def handle_form_submission():
    user_input = request.form.get('user_input')
    if not user_input:
        return render_template('index.html', message="Please enter a prompt")        

    response_data = fetch_image(user_input)

    if response_data:
        image_url = response_data['data'][0]['url']
        return redirect(url_for('index', image_url=image_url))
    else:       
        return render_template('index.html', message="Failed to generate image. Please try again later.")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)