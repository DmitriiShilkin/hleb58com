import asyncio

from django.shortcuts import render, redirect

from .forms import MessageForm, DealerForm
from .services import send_message, handle_uploaded_file


# Представление для отображения информации о компании
def about_view(request):
    return render(request, "about.html")


# Представление для отображения контактов
def contacts_view(request):
    return render(request, "contacts.html")


# Представление для отправки сообщения
def send_message_view(request):

    if request.method == 'POST':
        form = MessageForm(request.POST or None)
        if form.is_valid():
            title = 'Написать нам'
            # берем данные из формы
            full_name = form.cleaned_data.get('full_name')
            phone_number = form.cleaned_data.get('phone_number')
            email = form.cleaned_data.get('email')
            text = form.cleaned_data.get('text')
            # отправляем их в виде сообщения в телеграм
            asyncio.run(
                send_message(title, full_name, phone_number, email, text)
            )

            return redirect('product_list')
    else:
        form = MessageForm()

    context = {
        'form': form,
    }

    return render(request, 'send_message.html', context)


# Представление для отправки сообщения стать партнером
def become_dealer_view(request):

    if request.method == 'POST':
        form = DealerForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            title = 'Стать поставщиком'
            # берем данные из формы
            company_name = form.cleaned_data.get('company_name')
            phone_number = form.cleaned_data.get('phone_number')
            text = form.cleaned_data.get('text')
            proposal = handle_uploaded_file(company_name, request.FILES.get('proposal'))
            # отправляем их в виде сообщения в телеграм
            asyncio.run(
                send_message(title, company_name, phone_number, proposal, text)
            )

            return redirect('product_list')
    else:
        form = DealerForm()

    context = {
        'form': form,
    }

    return render(request, 'become_dealer.html', context)
