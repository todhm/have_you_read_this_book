from celery import Celery
from celery.schedules import crontab
from application import create_app
from celerytask.tasks import *


def create_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


flask_app = create_app()
celery = create_celery(flask_app)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every hour
    sender.add_periodic_task(
        crontab(minute='0', hour='12'),
        get_all_names_task.s(),
        name="get all names"
    )
    sender.add_periodic_task(
        crontab(minute='30', hour='12'),
        return_best_books_task.s(),
        name="return best books"
    )
    sender.add_periodic_task(
        crontab(minute='0', hour='0'),
        make_similarity_table_task.s(),
        name="make similarity table"
    )
    sender.add_periodic_task(
        crontab(minute='0', hour='1'),
        make_recommendation_task.s(),
        name="make recommendation list"
    )
