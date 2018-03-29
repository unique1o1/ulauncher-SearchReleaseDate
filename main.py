from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.event import PreferencesEvent
from ulauncher.api.shared.event import PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction


import requests
import logging

logger = logging.getLogger(__name__)
api_key = 'f0987a1113ab1a3b6cc3ac4b3cc29770'
url_movie = 'https://api.themoviedb.org/3/search/movie'
url_person = 'https://api.themoviedb.org/3/search/person'
# class PreferencesUpdateEventListener(EventListener):
#     def on_event(self, event, extension):
#         if event.id == 'limit':
#             getupdate.option = event.new_value

#         elif event.id == 'options':

#             getupdate.option = event.new_value
#             if getupdate.option == 'offline':
#                 getdictionary.init_dictionary()


# class PreferencesEventListener(EventListener):
#     def on_event(self, event, extension):
#         getupdate.limit = event.preferences['limit']
#         getupdate.option = event.preferences['options']

#         if event.preferences['options'] == 'offline':

#             getdictionary.init_dictionary()


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        # self.subscribe(PreferencesEvent, PreferencesEventListener())
        # self.subscribe(PreferencesUpdateEvent,
        #                PreferencesUpdateEventListener())
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
            args = arg.split(' ')
            if args[0] == 'p':
                result = requests.get(url_person, params={
                    'api_key': api_key, 'language': 'en-US', 'query': arg[1:], 'page': 1, 'include_adult': True}).json()
                name = result['results'][0]['name']
                result = result['results'][0]['known_for']

            else:

                result = requests.get(url_movie, params={
                    'api_key': api_key, 'language': 'en-US', 'query': arg[0:], 'page': 1, 'include_adult': True}).json()
                result = result['results']
            try:

                for i in range(8 if len(result) > 8 else len(result)):

                    items.append(ExtensionResultItem(icon='images/icon.png',
                                                     name=name if args[0] == 'p' else result[i]['title'],
                                                     description=result[i]['title'] if args[0] == 'p' else result[i]['release_date']
                                                     ))

            except Exception as e:
                logger.warning(e)
                error_info = "Coundn't find release data for {}".format(arg)
                items = [ExtensionSmallResultItem(icon='images/error.png',
                                                  name=error_info,
                                                  on_enter=CopyToClipboardAction(error_info))]
        return RenderResultListAction(items)


if __name__ == '__main__':
    DemoExtension().run()
