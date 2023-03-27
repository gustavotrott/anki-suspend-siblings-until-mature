from typing import Sequence, Callable

from anki.cards import Card
from aqt import mw
from aqt.qt import QAction

try:
    from anki.utils import html_to_text_line
except ImportError:
    from anki.utils import htmlToTextLine as html_to_text_line  # noqa


def get_current_deck_id() -> int:
    return mw.col.decks.get_current_id()


def get_siblings(card: Card) -> Sequence[Card]:
    card_ids = card.col.db.list("select id from cards where nid=? and id!=?",
                                card.nid, card.id)
    return [mw.col.get_card(card_id) for card_id in card_ids]


# A tiny helper for menu items, since type checking is broken there
def checkable(title: str, on_click: Callable[[bool], None]) -> QAction:
    action = QAction(title, mw, checkable=True)  # noqa
    action.triggered.connect(on_click)  # noqa
    return action

