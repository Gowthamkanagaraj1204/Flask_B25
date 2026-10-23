
from flask import Flask, render_template, request
import smtplib
import os
from email.message import EmailMessage

app = Flask(__name__)

@app.route("/smtp", methods=["GET", "POST"])
def smtp():

    if request.method == "POST":
        sender_email = request.form["sender_email"]
        password = os.environ.get("GMAIL_APP_PASSWORD")
        to_email = request.form["to_email"]
        mes = request.form["message"]

        if not password:
            return render_template(
                "smtp.html",
                error="Gmail app password is not configured."
            )
        try:
            msg = EmailMessage()
            msg["Subject"] = "Message from Flask SMTP"
            msg["From"] = sender_email
            msg["To"] = to_email
            msg.set_content(mes)

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)

            return render_template("smtp.html",
                success="Email sent successfully!"
            )

        except Exception as e:
            return render_template(
                "smtp.html",
                error=f"Email failed: {e}"
            ) 
    return render_template("smtp.html")

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True,port=5001)