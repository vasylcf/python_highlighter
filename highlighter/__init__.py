"""Flask module
file: __init__.py
date: 12.12.2012
author smith@example.com
license: MIT"""

from flask import Flask, render_template, request, Markup
import re


def create_app():
    """Create flask app for binding."""
    app = Flask(__name__)

    template_file_name = 'index.html'

    @app.route('/', methods=['GET'])
    def index():
        return render_template(template_file_name)

    @app.route('/', methods=['POST'])
    def process():
        search_text = request.form['search']
        text = request.form['text']
        highlighted_text = highlight_text(text, search_text)
        result = {'text': text,
                  'highlighted_text': Markup(highlighted_text),
                  }
        return render_template(template_file_name, **result)

    def markup_text(text):
        """Markup given text.
        This is supplementary method that helps you to wrap marked text in tags.
        @:param text - string text to be marked
        @:return marked text, e.g., <mark>highlighted text</mark>."""
        result = f'<mark>{text}</mark>'
        return result

    def highlight_text(text, expr):
        """Markup searched string in given text.
        @:param text - string text to be processed (e.g., 'The sun in the sky')
        @:param expr - string pattern to be searched in the text (e.g., 'th')
        @:return marked text, e.g., "<mark>Th</mark>e sun in <mark>th</mark>e sky"."""
        pattern = r'(?i)' + expr
        find = re.finditer(pattern, text)
        test_str = ''
        start_ind = 0
        for i in find:
            test_str += text[start_ind:i.span()[0]] + markup_text(text[i.span()[0]:i.span()[1]])
            start_ind = i.span()[1]
        return test_str + text[start_ind:]

    return app
