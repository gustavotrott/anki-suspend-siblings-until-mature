import jsonschema

from typing import Sequence

from aqt import mw

from .tools import get_current_deck_id


ENABLED_FOR_DECKS = "enabled_for_decks"
QUIET = "quiet"
UNSUSPEND_ON = "unsuspend_on"
VERSION = "version"

tag = mw.addonManager.addonFromModule(__name__)


def load_config():
    return mw.addonManager.getConfig(tag)

def load_default_config():
    return mw.addonManager.addonConfigDefaults(tag)

def save_config(data):
    mw.addonManager.writeConfig(tag, data)

def validate_config(data):
    jsonschema.validate(data, mw.addonManager._addon_schema(tag))

def run_on_configuration_change(function):
    mw.addonManager.setConfigUpdatedAction(__name__, lambda *_: function())


########################################################################################


# noinspection PyAttributeOutsideInit
class Config:
    def load(self):
        self.data = load_config()

    def save(self):
        save_config(self.data)

    @property
    def enabled_for_deck_ids(self) -> Sequence[str]:
        return [deck_id for deck_id, enabled in self.data[ENABLED_FOR_DECKS].items() if enabled is True]

    @property
    def enabled_for_current_deck(self):
        return str(get_current_deck_id()) in self.enabled_for_deck_ids

    @enabled_for_current_deck.setter
    def enabled_for_current_deck(self, value):
        self.data[ENABLED_FOR_DECKS][str(get_current_deck_id())] = value
        self.save()

    @property
    def unsuspend_on(self):
        return self.data[UNSUSPEND_ON]

    @unsuspend_on.setter
    def unsuspend_on(self, value):
        self.data[UNSUSPEND_ON] = value
        self.save()

    @property
    def quiet(self):
        return self.data[QUIET]

    @quiet.setter
    def quiet(self, value):
        self.data[QUIET] = value
        self.save()

