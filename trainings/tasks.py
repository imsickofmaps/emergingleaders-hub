from django.conf import settings
from celery.task import Task
from celery.utils.log import get_task_logger
from celery.exceptions import SoftTimeLimitExceeded
from requests.exceptions import HTTPError
from go_http.send import HttpApiSender


logger = get_task_logger(__name__)


class Send_Message(Task):

    """
    Task to send a message via Vumi
    """
    name = "emergingleaders_hub.trainings.tasks.send_message"

    class FailedEventRequest(Exception):

        """
        The attempted task failed because of a non-200 HTTP return
        code.
        """

    def vumi_client(self):
        return HttpApiSender(
            api_url=settings.VUMI_API_URL,
            account_key=settings.VUMI_ACCOUNT_KEY,
            conversation_key=settings.VUMI_CONVERSATION_KEY,
            conversation_token=settings.VUMI_ACCOUNT_TOKEN
        )

    def run(self, to_addr, message, **kwargs):
        """
        Sends a message via Vumi go_http
        """
        l = self.get_logger(**kwargs)

        l.info("Sending message")
        try:
            sender = self.vumi_client()
            try:
                vumiresponse = sender.send_text(to_addr, message,
                                                session_event="new")
                l.info("Sent text message to <%s>" % to_addr)
            except HTTPError as e:
                # retry message sending if in 500 range (3 default retries)
                if 500 < e.response.status_code < 599:
                    l.info("HTTPError in 500 range, retrying message send")
                    raise self.retry(exc=e)
                else:
                    raise e
            return vumiresponse

        except SoftTimeLimitExceeded:
            logger.error(
                'Soft time limit exceed processing location search \
                 via Celery.',
                exc_info=True)


send_message = Send_Message()
