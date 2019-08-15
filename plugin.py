###
# Copyright (c) 2019, lod
# All rights reserved.
###

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Giphy')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

import json
from random import randrange

class Giphy(callbacks.Plugin):
    """Queries Giphy for a GIF URL to share related to a given phrase"""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Giphy, self)
        self.__parent.__init__(irc)

        # API KEY from bot config
        self.GIPHY_API_KEY = self.registryValue("API_KEY")
        self.CHOOSE_FROM = 0

        self.url = "https://api.giphy.com/v1/gifs/search"

    def createJson(self, searchString):
        """searches the given phrase on giphy and create json"""

        # get headers from utils and create a referer
        ref = 'https://%s/%s' % (dynamic.irc.server, dynamic.irc.nick)
        headers = dict(utils.web.defaultHeaders)
        headers['Accept-Language'] = 'en-US; q=1.0, en; q=0.5'
        headers['Referer'] = ref

        # compose URL
        url  = self.url + "?"
        url += "api_key="+self.GIPHY_API_KEY
        url += "&" + utils.web.urlencode({'q' : searchString})
        url += '&limit=25'

        # open url and create json
        json_string = utils.web.getUrl(url).decode()
        giphy_json = json.loads(json_string)

        return giphy_json

    def giphy(self, irc, msg, args, opts, text):
        """[--{full,tile,url}] <phrase>
        Returns a gif related to given phrase, Powered By Giphy!
        """

        giphy_error = 0

        try:
            giphyJson = self.createJson(text)

            # get number of results from json
            if giphyJson['meta']['status'] == 200:
                results_count = giphyJson["pagination"]['count']

            # set error message if there aren't any results 
            if results_count == 0:
                giphy_error = "No results found."
            else:
                # choose random gif from resultslist
                randompick = randrange(results_count - 1)
                chosen_one = giphyJson["data"][randompick]["id"]

                giphy_title = giphyJson["data"][randompick]["title"]

        # catch any connection problem and set the error message
        except utils.web.Error as e:
            giphy_error = str(e)

        finally:
            # getting optional parameter
            opts = dict(opts)

            # output: error
            if giphy_error:
                irc.reply(giphy_error)
            # output: based on optional parameter
            elif 'full' in opts:
                irc.reply("%s - https://giphy.com/gifs/%s/fullscreen" % (giphy_title, chosen_one))
            elif 'tile' in opts:
                irc.reply("%s - https://giphy.com/gifs/%s/tile" % (giphy_title, chosen_one))
            elif 'url' in opts:
                irc.reply("%s - https://giphy.com/gifs/%s" % (giphy_title, chosen_one))
            # output: just the gif
            else:
                irc.reply("%s - https://i.giphy.com/media/%s/giphy.gif" % (giphy_title, chosen_one))

    giphy = wrap(giphy, [getopts({'tile':'','full':'','url':''}), 'text'])

Class = Giphy

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
