from flask import Flask, render_template, Response

from config import LocalDevelopmentConfig
from models import Email, db
from flask_apscheduler import APScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent
from emails import fetch_emails
import os
from logging import getLogger, StreamHandler, Formatter, INFO


app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)


with app.app_context():
    db.drop_all()
    db.create_all()

scheduler = APScheduler()
scheduler.init_app(app)

logger = getLogger("scheduler")
handler = StreamHandler()
handler.setFormatter(Formatter("%(asctime)s [%(levelname)s] : %(name)s - %(message)s"))
handler.setStream(open("scheduler.log", "a+"))
logger.addHandler(handler)
logger.setLevel(INFO)

app.app_context().push()


# @scheduler.task(
#     "cron",
#     id="fetch_emails",
#     minute="*",  # Every minute
#     misfire_grace_time=900,
#     max_instances=1,
#     coalesce=True,
# )
@scheduler.task(
    "interval",
    id="fetch_emails",
    seconds=10,
    misfire_grace_time=900,
    max_instances=1,
    coalesce=True,
)
def fetch_and_add_emails():
    user_email = os.getenv("IMAP_EMAIL")
    password = os.getenv("IMAP_PASSWORD")
    emails = fetch_emails(user_email, password)

    logger.info(f"Found {len(emails)} new emails")

    with app.app_context():
        for email in emails:
            if Email.query.filter_by(message_id=email["id"]).first():
                continue
            new_email = Email(
                timestamp=email["timestamp"],
                message_id=email["id"],
                index=email["index"],
                sender=email["sender"],
                subject=email["subject"],
            )
            db.session.add(new_email)

            logger.info(f"Processed email {email['id']}")

        db.session.commit()


def log(event: JobExecutionEvent):
    if event.exception:
        logger.error("An error occurred", exc_info=event.exception)
    else:
        logger.info(f"Job {event.job_id} executed successfully")


scheduler.add_listener(log, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)


def tail_log(file_path):
    with open(file_path, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            yield line


@app.route("/logs")
def logs():
    return Response(tail_log("scheduler.log"), mimetype="text/plain")


@app.route("/")
def index():
    emails = Email.query.all()
    message = "No emails found" if not emails else ""
    return render_template("index.html", emails=emails, message=message)


if __name__ == "__main__":
    with open("scheduler.log", "w"):
        pass

    scheduler.start()

    # app.run(debug=True)
    app.run(debug=False)
