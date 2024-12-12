from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from emails import fetch_emails
from models import Email, db

import os
from dotenv import load_dotenv

load_dotenv()


jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")}
scheduler = BackgroundScheduler(jobstores=jobstores)


# scheduler.add_job(
#     fetch_and_add_emails,
#     "interval",
#     minutes=1,
#     id="fetch_emails",
#     replace_existing=True,
#     args=[os.getenv("IMAP_EMAIL"), os.getenv("IMAP_PASSWORD")],
# )


def test():
    print("test")


# scheduler.add_job(test, "interval", seconds=5, id="test", replace_existing=True)

if __name__ == "__main__":
    scheduler.start()
    print("Scheduler started")
    input("Press any key to exit\n")
