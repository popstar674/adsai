from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def index():
    return "adsai is running!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "Create a professional ad image description for Instagram.")
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert ad designer."},
            {"role": "user", "content": f"Generate a prompt for an AI image model to create an ad image for: {prompt}"}
        ]
    )

    image_prompt = response['choices'][0]['message']['content']
    return jsonify({"image_prompt": image_prompt})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
