from django.shortcuts import render
from .tasks import notify_customers
# from django.core.mail import BadHeaderError
# from templated_mail.mail import BaseEmailMessage


def say_hello(request):

    notify_customers.delay('Hello')
    # try:
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': "Hassaan"}
    #     )
    #     message.send(['hassaan.202202563@gcuf.edu.pk'])
    # except BadHeaderError:
    #     pass
    return render(request, "hello.html", {"name": "Hassaan"})