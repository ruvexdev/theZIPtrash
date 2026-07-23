import logging

logger = logging.getLogger(__name__)


def notify(title, message, app_name="theZIPtrash"):
    try:
        from plyer import notification

        notification.notify(
            title=title,
            message=message,
            app_name=app_name,
            timeout=5,
        )
    except Exception as e:
        logger.warning(f"Notification failed: {e}")
