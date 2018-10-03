from celery.schedules import crontab

from backoffice.celery import app as celery_app
from base.business.learning_units.automatic_postponement import fetch_learning_unit_to_postpone

celery_app.conf.beat_schedule.update({
    'Extend learning units': {
        'task': 'base.tasks.extend_learning_units',
        'schedule': crontab(day_of_week=15, month_of_year=7)
    },
})


@celery_app.task
def extend_learning_units():
    results, errors = fetch_learning_unit_to_postpone()
    return errors