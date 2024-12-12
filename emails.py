import imaplib
import email
from datetime import datetime, timedelta, timezone
from email.header import decode_header
from email.utils import parsedate_to_datetime, getaddresses


def fetch_emails(user_email, password):
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(user_email, password)
        imap.select('"INBOX"')
        status, messages = imap.search(None, "UNSEEN")

        emails = []

        # iterate over the messages and retrieve their contents
        for num in messages[0].split():
            _, msg = imap.fetch(num, "(RFC822)")
            message = email.message_from_bytes(msg[0][1])

            # print the message details
            emails.append(
                {
                    "id": decode_header(message["Message-ID"])[0][0],
                    "timestamp": parsedate_to_datetime(message["Date"]),
                    "index": int(num),
                    "sender": getaddresses(message.get_all("From", []))[0][1],
                    "subject": decode_header(message["Subject"])[0][0],
                }
            )
        imap.close()
        imap.logout()

        return emails
    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            imap.logout()
        except:
            pass
