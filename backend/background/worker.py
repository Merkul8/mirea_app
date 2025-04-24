import asyncio

from celery import Celery
import config
from app.notification.sender import Sender


celery_app = Celery(
    "celery_app",
    backend=config.REDIS_URL,
    broker=config.REDIS_URL
)

celery_app.conf.broker_connection_retry_on_startup = True
# celery_app.conf.beat_schedule = {
#     ...
# }


@celery_app.task(name="send_email")
def send_email(subject, to_email, content):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Sender.send(subject=subject, to_email=to_email, content=content))
