import logging

logger = logging.getLogger(__name__)


def notificar(titulo, mensaje, app_name="theZIPtrash"):
    try:
        from plyer import notification

        notification.notify(
            title=titulo,
            message=mensaje,
            app_name=app_name,
            timeout=5,
        )
    except Exception as e:
        logger.warning(f"Notification failed: {e}")
