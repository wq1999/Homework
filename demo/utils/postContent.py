import re
from textrank4zh import TextRank4Sentence


def clean(content):
    reg = re.compile('<[^>]*>')
    content = reg.sub('', content).replace('\n', '')
    return content


def get_summary(text):
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source='all_filters')
    item = tr4s.get_key_sentences(num=1)
    summary = item[0].sentence
    return summary
