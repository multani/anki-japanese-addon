Yet another Japanese helper addon for Anki
==========================================

It focuses mostly on automating the followings:

* to retrieve the translation information out of [Jisho](https://jisho.org).

  This focuses especially on Hiragana, Katakana and their Romaji interpretation
  for now.

* the autogeneration of Japanese sounds using [Amazon
  Polly](https://aws.amazon.com/polly/)

  You will need credentials to access AWS and configure them in `config.json`
  to use this addon.


See also
--------

There are a bunch of other addons to help learning Japanese available on [the
official Anki addons webpage](https://ankiweb.net/shared/addons/).
They are probably more mature and I expect the developers to know more what
they are doing than me :)


Dependencies
------------

This addon requires the following libraries:

* [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/) to interact
  with Amazon Polly
* it bundles `romkan.py` from
  [python-romkan](https://github.com/soimort/python-romkan/blob/f92106a37d388c62d871210aee2ec46eb5e5cef2/src/romkan/common.py)
