from django import template
from django.utils.safestring import mark_safe

register = template.Library()

STRONG_WORDS = [
    'состав',
    'бжу',
    'калорийность',
]


@register.filter()
def strong(value):
    try:
        list_ = value.split()
    except AttributeError:
        print('Ошибка! Неверный тип данных - должна быть строка!')
    else:
        new_list = []
        for word in list_:
            word_strip = word.strip('".,:;!?<>()')
            if word_strip.lower() in STRONG_WORDS:
                strong_word = f'<br><strong>{word}</strong>'
                new_list.append(strong_word)
            else:
                new_list.append(word)
        value = ' '.join(new_list)
    return mark_safe(value)


@register.filter()
def get_user(value):
    try:
        list_ = value.split('/')
    except AttributeError:
        print('Ошибка! Неверный тип данных - должна быть строка!')
    else:
        return list_[-1]
