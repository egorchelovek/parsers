from background_task import background
from django.core.mail import send_mail

@background(schedule=60)
def notify(text):
    send_mail(
    "Math books",
    "Hello, dear Egor! I'm very glad to see you again here. I prepared some books for you...",
    "egor.zamotaev@mail.ru",
    ["egor.zamotaev@mail.ru", "egor.richman@gmail.com"],
    fail_silently=False,)
