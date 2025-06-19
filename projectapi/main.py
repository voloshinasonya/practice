From fastapi import FastAPI
Import wikipedia
Import random

App = FastAPI()
Wikipedia.set_lang(«uk»)

# Ключевые слова для тем
Keywords_by_topic = {
    «дата»: [
        «січня», «лютого», «березня», «квітня», «травня», «червня»,
        «липня», «серпня», «вересня», «жовтня», «листопада», «грудня»
    ],
    «місце»: [
        «область», «місто», «замок», «монастир», «село», «фортеця»,
        «район», «урочище», «парк», «місцевість», «регіон»
    ],
    «персона»: [
        «поет», «письменник», «гетьман», «князь», «політик», «журналіст»,
        «композитор», «актор», «революціонер», «церковний діяч», «художник»,
        «філософ», «співак», «науковець», «військовик», «президент», «патріарх»,
        «лікар», «хірург», «педіатр», «невролог», «психіатр»
    ],
    «подія»: [
        «битва», «революція», «війна», «повстання», «катастрофа»,
        «маніфестація», «злочин», «реформа», «злука», «вибори», «референдум»,
        «протест», «вбивство», «демонстрація»
    ],
    «термін»: [
        «ідеологія», «політика», «націоналізм», «комунізм», «республіка»,
        «федерація», «автокефалія», «колонія», «імперія», «парламент»,
        «лібералізм», «автономія», «демократія», «соціалізм», «державність»,
        «право», «свобода», «конституція»
    ]
}

@app.get(«/wiki/{topic}»)
Def get_random_article(topic: str):
    Topic = topic.lower()
    If topic not in keywords_by_topic:
        Return {«error»: «Невідома тема»}

    For _ in range(15):  # максимум 15 спроб знайти релевантну статтю
        Try:
            Keyword = random.choice(keywords_by_topic[topic])
            Search_results = wikipedia.search(keyword)
            If not search_results:
                Continue

            Title = random.choice(search_results)
            Page = wikipedia.page(title)
            Summary = wikipedia.summary(title, sentences=3)
            Categories = [cat.lower() for cat in page.categories]

            # Фільтрація за категоріями
            If topic == «персона»:
                If not any(x in cat for cat in categories for x in [«персоналії», «народились», «люди»]):
                    Continue
            Elif topic == «подія»:
                If not any(x in cat for cat in categories for x in [«події», «битви», «революції», «війни»]):
                    Continue
            Elif topic == «термін»:
                If not any(x in cat for cat in categories for x in [«поняття», «визначення», «терміни»]):
                    Continue
            Elif topic == «місце»:
                If not any(x in cat for cat in categories for x in [«населені пункти», «географія», «області україни»]):
                    Continue
            Elif topic == «дата»:
                If not any(x in cat for cat in categories for x in [«дата», «події за роками», «хронологія»]):
                    Continue

            Return {
                «title»: page.title,
                «summary»: summary,
                «url»: page.url
            }

        Except Exception:
            Continue

    Return {«error»: «Не вдалося знайти відповідну статтю»}
