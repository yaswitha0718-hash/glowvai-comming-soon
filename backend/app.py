from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")


@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "glowvai-email-backend"
    })


@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({"error": "Email is required"}), 400

    user_email = data["email"]

    try:
        msg = EmailMessage()
        msg["Subject"] = "🚀 New GLOWVAI Early Access Signup"
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_USER
        msg.set_content(
            f"""New Early Access Signup

User Email: {user_email}

Product: GLOWVAI
"""
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        print("SMTP ERROR:", e)
        return jsonify({"error": "Email sending failed"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
