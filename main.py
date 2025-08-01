from flask import Flask, request, jsonify
import openai
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/generate", methods=["POST"])
def generate_ad():
    if not openai.api_key:
        return jsonify({"error": "OpenAI API key not set"}), 500

    data = request.get_json()
    ad_description = data.get("description")
    if not ad_description:
        return jsonify({"error": "Missing ad description"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates high-converting ad content: title, call to action, and hashtags."},
                {"role": "user", "content": ad_description}
            ],
            temperature=0.7
        )
        text = response.choices[0].message.content

        image = Image.new("RGB", (1080, 1080), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((50, 50), text, font=font, fill=(0, 0, 0))

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return jsonify({"text": text, "image": img_str})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
