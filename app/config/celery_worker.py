# from celery import Celery
# from config.config import settings

# celery_app = Celery(
#     "worker",
#     broker=settings.REDIS_BROKER_URL,
#     backend=settings.REDIS_RESULT_BACKEND,
# )

# celery_app.conf.task_routes = {
#     "tasks.send_registration_email": {"queue": "emails"},
# }

# from celery import Celery
# from config.config import settings

# celery_app = Celery(
#     "worker",
#     broker=settings.REDIS_BROKER_URL,
#     backend=settings.REDIS_RESULT_BACKEND,
# )

# celery_app.conf.task_routes = {
#     "util.emails.send_registration_email": {"queue": "emails"},
# }

from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",  # Redis as broker
    backend="redis://localhost:6379/0",  # Optional: result backend
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)