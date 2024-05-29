from django.core.exceptions import ValidationError


# валидатор номера телефона
def phone_number_validator(value):

    if not value.isdigit():
        raise ValidationError(
            "В номере телефона допустимы только цифры!"
        )


# валидатор текстовых полей
def text_validator(value):
    if '=' in value:
        raise ValidationError(
            "Знак '=' не допустим!"
        )
    # заменяем указанные символы разметки гипертекста на их мнемонические коды
    new_value = value.translate(str.maketrans({
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
        '"': '&quot;',
        "'": '&apos;',
        ' ': '&nbsp;'
    }))

    return new_value
