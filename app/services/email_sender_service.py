from google.oauth2.credentials import Credentials
from app.database import SessionLocal
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.models.voter import Voter
from app.repositories.voter_repository import check_voter_limit, save_voter_credentials
from app.utils.crypto import generate_nonce
from app.config import settings

watcher_thread = None

import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

def send_email(to_email: str):
    """Send credentials email via Gmail API with Service Account."""
    n1 = generate_nonce()
    n2 = generate_nonce()

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Your Voting Credentials</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap');

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
        background-color: #f0f2f5;
        font-family: 'DM Sans', sans-serif;
        padding: 40px 16px;
        color: #1a1a2e;
        }}

        .wrapper {{
        max-width: 560px;
        margin: 0 auto;
        }}

        .card {{
        background: #ffffff;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        }}

        .header {{
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
        padding: 36px 40px;
        position: relative;
        overflow: hidden;
        }}

        .header::before {{
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 180px; height: 180px;
        border-radius: 50%;
        background: rgba(255,255,255,0.04);
        }}

        .header::after {{
        content: '';
        position: absolute;
        bottom: -60px; left: 30px;
        width: 240px; height: 240px;
        border-radius: 50%;
        background: rgba(255,255,255,0.03);
        }}

        .badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 11px;
        font-weight: 500;
        color: rgba(255,255,255,0.7);
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 16px;
        }}

        .header h1 {{
        font-size: 22px;
        font-weight: 600;
        color: #ffffff;
        line-height: 1.3;
        }}

        .header p {{
        color: rgba(255,255,255,0.55);
        font-size: 13px;
        margin-top: 6px;
        }}

        .body {{
        padding: 36px 40px;
        }}

        .greeting {{
        font-size: 15px;
        color: #444;
        margin-bottom: 24px;
        line-height: 1.6;
        }}

        .credentials-box {{
        background: #f7f8fc;
        border: 1px solid #e4e7f0;
        border-radius: 12px;
        overflow: hidden;
        margin: 24px 0;
        }}

        .credentials-label {{
        background: #eef0f8;
        padding: 10px 20px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #7a82a6;
        border-bottom: 1px solid #e4e7f0;
        }}

        .credential-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 20px;
        border-bottom: 1px solid #e4e7f0;
        }}

        .credential-row:last-child {{
        border-bottom: none;
        }}

        .credential-key {{
        font-size: 12px;
        font-weight: 600;
        color: #7a82a6;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        min-width: 40px;
        }}

        .credential-value {{
        font-family: 'DM Mono', monospace;
        font-size: 15px;
        font-weight: 500;
        color: #1a1a2e;
        letter-spacing: 0.04em;
        word-break: break-all;
        text-align: right;
        }}

        .warning {{
        display: flex;
        align-items: flex-start;
        gap: 12px;
        background: #fff8f0;
        border: 1px solid #f5d9b8;
        border-left: 3px solid #e8893a;
        border-radius: 8px;
        padding: 14px 16px;
        margin: 24px 0;
        }}

        .warning-icon {{
        font-size: 16px;
        flex-shrink: 0;
        margin-top: 1px;
        }}

        .warning p {{
        font-size: 13px;
        color: #7a4a1a;
        line-height: 1.5;
        }}

        .warning strong {{
        font-weight: 600;
        }}

        .footer-text {{
        font-size: 13px;
        color: #666;
        line-height: 1.6;
        margin-top: 8px;
        }}

        .divider {{
        height: 1px;
        background: #eee;
        margin: 28px 0;
        }}

        .footer {{
        padding: 20px 40px;
        background: #f7f8fc;
        border-top: 1px solid #eee;
        font-size: 11.5px;
        color: #aaa;
        text-align: center;
        line-height: 1.6;
        }}
    </style>
    </head>
    <body>
    <div class="wrapper">
        <div class="card">

        <div class="header">
            <div class="badge">🔐 Secure Credential Delivery</div>
            <h1>Your Voting Credentials</h1>
            <p>Keep these safe — they are unique to you.</p>
        </div>

        <div class="body">
            <p class="greeting">
            Dear Voter,<br/><br/>
            Your unique credentials have been securely generated and assigned to your account.
            Use them to authenticate your vote. These credentials are <strong>one-time use</strong>
            and strictly personal.
            </p>

            <div class="credentials-box">
            <div class="credentials-label">Your Credentials</div>
            <div class="credential-row">
                <span class="credential-key">N1</span>
                <span class="credential-value">{n1}</span>
            </div>
            <div class="credential-row">
                <span class="credential-key">N2</span>
                <span class="credential-value">{n2}</span>
            </div>
            </div>

            <div class="warning">
            <span class="warning-icon">⚠️</span>
            <p>
                <strong>Do not share these credentials</strong> with anyone, including system
                administrators. Anyone who has access to them could vote on your behalf.
            </p>
            </div>

            <div class="divider"></div>

            <p class="footer-text">
            If you did not request these credentials or believe you received this message in error,
            please contact our support team immediately.
            </p>

            <p class="footer-text" style="margin-top: 20px;">
            Regards,<br/>
            <strong>The e-voting System Team</strong>
            </p>
        </div>

        <div class="footer">
            This is an automated message. Please do not reply directly to this email.<br/>
            © 2026 e-voting. All rights reserved.
        </div>

        </div>
    </div>
    </body>
    </html>
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Confidential: Your Secure Voting Credentials"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    creds = Credentials(
        token=settings.GMAIL_TOKEN,
        refresh_token=settings.GMAIL_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GMAIL_CLIENT_ID,
        client_secret=settings.GMAIL_CLIENT_SECRET,
    )

    service = build("gmail", "v1", credentials=creds)
    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()


    return n1, n2

def watch_voters():
    """Watch until voters table reaches TRIGGER_COUNT, then send emails to all."""
    while True:
        db = SessionLocal()
        try:
            if check_voter_limit(db):
                voters = db.query(Voter).all()
                for voter in voters:
                    n1,n2= send_email(voter.email)
                    print(f"Email sent to {voter.email}")
                    save_voter_credentials(n1=n1,n2=n2,db=db)
                    print(f"credentials saved")

                print("All emails sent.")
                break

        except Exception as e:
            print(f" Error: {e}")

        finally:
            db.close()

        threading.Event().wait(10)


def start_voter_watcher():
    global watcher_thread
    watcher_thread = threading.Thread(target=watch_voters, daemon=True)
    watcher_thread.start()