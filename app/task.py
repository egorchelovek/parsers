from background_task import background
from django.core.mail import EmailMessage
from django.conf import settings
from app.parsers.avito import parse_avito


@background(schedule=60)
def parse_and_report(mailing_list, source_sites, objects_types, objects_amount, \
city, room_area_min, room_area_max, \
min_price_rent, max_price_rent, min_price_sell, max_price_sell):

    for site in source_sites:
        for objects_type in objects_types:

            min_price = min_price_sell
            max_price = max_price_sell
            if objects_type == 0:
                min_price = min_price_rent
                max_price = max_price_rent

            # parse site
            document_path = parse(site, (int(objects_type), int(objects_amount), \
            city, int(room_area_min), int(room_area_max),\
            int(min_price), int(max_price)))

            # send mail
            if document_path != "":
                send_mail(mailing_list, document_path)

def parse(site, params):
    if settings.SOURCE_SITES[site] == "Avito":
        return parse_avito(params)
    elif settings.SOURCE_SITES[site] == "Youla":
        return parse_youla(params)
    elif settings.SOURCE_SITES[site] == "Move":
        return parse_move(params)
    else
        pass
    return ""

def send_mail(mailing_list, attach_file_path):
    # send mail
    message = EmailMessage(
    settings.EMAIL_SUBJECT,
    settings.EMAIL_BODY,
    settings.EMAIL_HOST_USER,
    mailing_list.split(','))
    message.attach_file(attach_file_path)
    message.send()
