from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction


import requests
import logging

logger = logging.getLogger(__name__)
api_key = 'f0987a1113ab1a3b6cc3ac4b3cc29770'
url_movie = 'https://api.themoviedb.org/3/search/movie'
url_person = 'https://api.themoviedb.org/3/search/person'


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def __help(self):
        items = [ExtensionSmallResultItem(icon='images/info.png',
                                          name="Type your movie name for it's release date", on_enter=HideWindowAction())]
        return items

    def on_event(self, event, extension):
        items = []
        arg = event.get_argument()
        if arg is None:
            items = self.__help()
        else:
            try:
                args = arg.split(' ')
                if args[0] == 'p':
                    result = requests.get(url_person, params={
                        'api_key': api_key, 'language': 'en-US', 'query': " ".join(args[1:]), 'page': 1, 'include_adult': True}).json()
                    if len(result['results']) == 0:
                        raise ValueError('Result not found')

                    name = result['results'][0]['name']
                    result = result['results'][0]['known_for']

                else:

                    result = requests.get(url_movie, params={
                        'api_key': api_key, 'language': 'en-US', 'query': " ".join(args[0:]), 'page': 1, 'include_adult': True}).json()
                    if len(result['results']) == 0:
                        raise ValueError('Result not found')
                    result = result['results']

                for i in range(8 if len(result) > 8 else len(result)):
                    if 'title' in result[i]:
                        title = result[i]['title']
                    else:
                        title = result[i]['name']
                    items.append(ExtensionResultItem(icon='images/icon.png',
                                                     name=name if args[0] == 'p' else result[i]['title'],
                                                     description=title if args[0] == 'p' else result[i]['release_date'], on_enter=CopyToClipboardAction(title if args[0] == 'p' else result[i]['release_date'])
                                                     ))

            except Exception as e:
                logger.warning(e)
                error_info = "Coundn't find release data for {}".format(
                    " ".join(args[1:]) if args[0] == 'p' else " ".join(args[0:]))
                items = [ExtensionSmallResultItem(icon='images/error.png',
                                                  name=error_info,
                                                  on_enter=CopyToClipboardAction(error_info))]
        return RenderResultListAction(items)


if __name__ == '__main__':
    DemoExtension().run()
