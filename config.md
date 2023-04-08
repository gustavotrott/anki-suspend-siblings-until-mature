<style>
    version {
        font-weight: normal;
        font-size: medium;
    }
</style>

# Suspend siblings until mature <version>v1</version>

This add-on will look for Siblings of the current Card and suspend all of them.
When the current card is very mature, it will Unsuspend its siblings.
Anki considers a card Mature when its due value is greater or equal 21. But I consider this interval too short and I use due value 35 as default.


"unsuspend_on": Due value used to unsuspend a card's siblings

"quiet": Show tooltip warning when a card is Suspended or Unsuspended?