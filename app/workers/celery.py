# from celery import Celery

# celery = Celery(
#     "web_scraper",
#     # broker="redis://localhost:6379/0",  # Update if Redis is running on another host/port
#     # backend="redis://localhost:6379/0",
#     # broker="redis://a325d6614300:6379/0",
#     # backend="redis://a325d6614300:6379/0",
#     # broker_url = "redis://host.docker.internal:6379/0",
#     # result_backend = "redis://host.docker.internal:6379/0",
#     broker_url = 'redis://127.0.0.1:6379/0',
#     result_backend = 'redis://127.0.0.1:6379/0',


# )

# celery.conf.update(
#     task_routes={
#         "app.workers.tasks.*": {"queue": "web_scraper_queue"},
#     }
# )
from celery import Celery

celery = Celery(
    "web_scraper",
    broker="redis://redis_container:6379/0",  # Use the service name from docker-compose
    backend="redis://redis_container:6379/0",
)

celery.conf.update(
    task_routes={
        "app.workers.tasks.*": {"queue": "web_scraper_queue"},
    }
)
