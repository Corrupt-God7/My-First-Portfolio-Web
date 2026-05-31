from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ── Config (set these in your .env file) ──────────────────────────────────────
SENDER_EMAIL    = os.getenv("SENDER_EMAIL", "chiragdeviputra33@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "nzzg zbgm iavt luns")          # Gmail App Password
RECEIVER_EMAIL  = os.getenv("RECEIVER_EMAIL", "chiragdeviputra33@gmail.com")
# ─────────────────────────────────────────────────────────────────────────────


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()

    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()

    # Basic validation
    if not all([name, email, message]):
        return jsonify({"success": False, "error": "Please fill in all required fields."}), 400

    # Build email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Portfolio Contact: {subject or 'New Message'} — from {name}"
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECEIVER_EMAIL
    msg["Reply-To"] = email

    html_body = f"""
    <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#0d1321;color:#e2e8f0;border-radius:12px;overflow:hidden;">
      <div style="background:#0ea5e9;padding:20px 28px;">
        <h2 style="margin:0;color:#fff;font-size:1.1rem;">📬 New Portfolio Message</h2>
      </div>
      <div style="padding:28px;">
        <table style="width:100%;border-collapse:collapse;">
          <tr><td style="padding:8px 0;color:#64748b;width:80px;font-size:0.85rem;">Name</td><td style="padding:8px 0;font-weight:600;">{name}</td></tr>
          <tr><td style="padding:8px 0;color:#64748b;font-size:0.85rem;">Email</td><td style="padding:8px 0;"><a href="mailto:{email}" style="color:#0ea5e9;">{email}</a></td></tr>
          <tr><td style="padding:8px 0;color:#64748b;font-size:0.85rem;">Subject</td><td style="padding:8px 0;">{subject or '—'}</td></tr>
        </table>
        <hr style="border:none;border-top:1px solid #1e2d45;margin:16px 0;">
        <p style="color:#94a3b8;font-size:0.85rem;margin-bottom:8px;">Message:</p>
        <p style="line-height:1.7;white-space:pre-wrap;">{message}</p>
      </div>
      <div style="padding:16px 28px;background:#111827;font-size:0.75rem;color:#475569;text-align:center;">
        Sent via Chirag Deviputra's Portfolio
      </div>
    </div>
    """

    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        return jsonify({"success": True, "message": "Message sent! I'll get back to you soon."})
    except Exception as e:
        print(f"Email error: {e}")
        return jsonify({"success": False, "error": "Failed to send. Please email me directly."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
