###
# Copyright (c) 2019, lod
# All rights reserved.
###

from supybot import conf, registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Giphy')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Giphy', True)


Giphy = conf.registerPlugin('Giphy')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Giphy, 'someConfigVariableName',
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))

conf.registerGlobalValue(Giphy, 'API_KEY',
     registry.String("dc6zaTOxFJmzC", _("""API KEY for giphy.com""")))
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
