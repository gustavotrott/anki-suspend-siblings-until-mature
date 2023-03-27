# Anki - Suspend siblings until mature

It has the intent to prevent both sides of the same card from being shown within a short interval of time. In my opinion it will be much better if it waits until the first side is mature before starting showing the other side. 


With this add-on, when the first time the card is shown, it will look for all siblings and suspend them while the current card is not mature.
Once it achieves the mature level, the next sibling will be unsuspended.

I'm not a Python developer, so I used https://github.com/oakkitten/anki-delay-siblings as base for this project! Thanks a lot for them.