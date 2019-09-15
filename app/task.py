from background_task import background
from django.core.mail import EmailMessage
from django.conf import settings
from app.parsers import avito


@background(schedule=60)
def parse_and_report(mails, parsers, types, limit, min_price, max_price):

    # parse
    filepath = ""
    for parser in parsers:
        for type in types:
            filepath = parse(parser, (type, limit, min_price, max_price))
    if filepath != "":
        return

    # send mail
    msg = EmailMessage(
    settings.EMAIL_SUBJECT,
    settings.EMAIL_BODY,
    settings.EMAIL_HOST_USER,
    mails,
    fail_silently=False,)
    msg.attach_file(filepath)


def parse(parser, params):
    if parser = "Avito":
        return parse_avito(params)
    return ""
