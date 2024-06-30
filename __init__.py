from contextlib import suppress

from anki.cards import Card
from anki.consts import *
from aqt import mw, gui_hooks
from aqt.utils import tooltip

from .configuration import (
    Config,
    run_on_configuration_change,
)

from .tools import (
    get_siblings,
    checkable,
    html_to_text_line,
)


############################################################################### reviewer
########################################################################################

config = Config()
config.load()


@gui_hooks.reviewer_did_answer_card.append
def reviewer_did_answer_card(_, card: Card, ease):
    # Check if the feature is enabled for the current deck
    if not config.enabled_for_current_deck:
        return

    isMature = card.ivl > config.unsuspend_on and card.type == CARD_TYPE_REV and card.queue == QUEUE_TYPE_REV

    siblings = get_siblings(card)
    for sibling in siblings:
        question = html_to_text_line(sibling.question())
        willSuspend = not isMature and sibling.type == CARD_TYPE_NEW and sibling.queue in [QUEUE_TYPE_NEW, QUEUE_TYPE_SIBLING_BURIED]

        # Skip if sibling is ahead in the order
        if sibling.ord < card.ord:
            return

        if mw.col.sched.version < 3:
            # print(f"Using scheduler < 3")
            # Remove sibling from curr queue (rev, new or learn)
            if sibling.id in mw.col.sched._revQueue:
                if not willSuspend:
                    mw.col.sched.bury_cards(ids=[sibling.id], manual=False)
                with suppress(AttributeError, ValueError):
                    mw.col.sched._revQueue.remove(sibling.id)  # noqa

            if sibling.id in mw.col.sched._newQueue:
                if not willSuspend:
                    mw.col.sched.bury_cards(ids=[sibling.id], manual=False)
                with suppress(AttributeError, ValueError):
                    mw.col.sched._newQueue.remove(sibling.id)  # noqa

            if sibling.id in mw.col.sched._lrnQueue:
                if not willSuspend:
                    mw.col.sched.bury_cards(ids=[sibling.id], manual=False)
                with suppress(AttributeError, ValueError):
                    mw.col.sched._lrnQueue.remove(sibling.id)  # noqa
        else:
            # print(f"Using scheduler 3")
            queuedCards = mw.col.sched.get_queued_cards(fetch_limit=10000).cards
            for item in queuedCards:
                if item.card.id == sibling.id:
                    if not willSuspend:
                        mw.col.sched.bury_cards(ids=[sibling.id], manual=False)

        # Don't take any action if the card is RELEARNING (pressed "Again" button)
        if card.type == CARD_TYPE_RELEARNING:
            return

        if willSuspend:
            mw.col.sched.suspend_cards(ids=[sibling.id])
            print(f"Sibling: {question} Suspended!<br>")
            if not config.quiet:
                tooltip(f"Sibling: {question} Suspended!<br>")

        if isMature and sibling.queue == QUEUE_TYPE_SUSPENDED and sibling.ord == card.ord + 1:
            mw.col.sched.unsuspend_cards(ids=[sibling.id])
            mw.col.sched.bury_cards(ids=[sibling.id], manual=False)
            question = html_to_text_line(sibling.question())
            print(f"Sibling: {question} UNSuspended!<br>")
            if not config.quiet:
                tooltip(f"Sibling: {question} UNSuspended!<br>")


########################################################################################
################################################################ menus and configuration
########################################################################################

def set_enabled_for_this_deck(checked):
    config.enabled_for_current_deck = checked

def set_quiet(checked):
    config.quiet = checked

menu_enabled_for_this_deck = checkable(
    title="Enable suspend siblings until mature for this deck",
    on_click=set_enabled_for_this_deck
)

mw.form.menuTools.addSeparator()
mw.form.menuTools.addAction(menu_enabled_for_this_deck)
menu_for_all_decks = mw.form.menuTools.addMenu("For all decks")
menu_for_all_decks.addSeparator()

def adjust_menu():
    if mw.col is not None:
        menu_enabled_for_this_deck.setEnabled(mw.state in ["overview", "review"])
        menu_enabled_for_this_deck.setChecked(config.enabled_for_current_deck)


@gui_hooks.state_did_change.append
def state_did_change(_next_state, _previous_state):
    adjust_menu()


@run_on_configuration_change
def configuration_changed():
    config.load()
    adjust_menu()
