from celery import Celery

from core.models import Stone
from core.serializers import ActivationSerializer, StoneSerializer
from core.settings import CELERY_BROKER_URL
from django.db import transaction
import logging
import time

app = Celery('core', broker=CELERY_BROKER_URL)


@app.task
def asynchronous_task(x, y):
    logger = logging.getLogger(__name__)

    try:
        # Your task code here
        result = x + y
        time.sleep(3)

        # Log a message indicating the task has started
        logger.info(f"Task started with x={x} and y={y}")

        # Log the result of the task
        logger.info(f"Task result: {result}")

        return result
    except Exception as e:
        # Log any exceptions or errors
        logger.error(f"An error occurred: {str(e)}")
        raise


@app.task
def activate_stone(activation_data, stone_id, username):
    logger = logging.getLogger(__name__)

    try:
        with transaction.atomic():
            serializer = ActivationSerializer(data=activation_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            stone_info = Stone.objects.get(Stone_ID=stone_id)

            # Log a message indicating the task has started
            logger.info(f"{username}, has activated {stone_info.Stone_Name}.")

        return 1
    except Exception as e:
        # Log any exceptions or errors
        logger.error(f"An error occurred: {str(e)}")
        raise
