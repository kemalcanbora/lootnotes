from newspaper import Article


class TextParser:
    def __init__(self, url, lang):
        self.url = url
        self.article = Article(url, language=lang)
        self.article.download()
        self.article.parse()

    def parse_text(self):
        return self.article.text

    def parse_title(self):
        return self.article.title

    def parse_url(self):
        return self.url


def language_controller(url):
    lang_controller = TextParser(url, lang="en").parse_text()
    if len(lang_controller) == 0:
        return "tr"
    else:
        return "en"
