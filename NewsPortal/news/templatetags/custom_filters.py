from django import template

register = template.Library()


@register.filter()
def censor(text):
    with open(r'./news/templatetags/filter_profanity_russian_cached.txt', 'r', encoding='utf-8') as file:
        bad_words = file.read().splitlines()
    words = text.split()
    for i, word in enumerate(words):
        check_word = word.lower()
        if check_word in bad_words:
            words[i] = word[0] + '*' * (len(word) - 1)
    return ' '.join(words)
