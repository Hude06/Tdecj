# Tdeck

circuitpython fun with the tdeck


`perftest.py` draws increasing numbers of circles to test the graphics performance

`inputtest.py` prints keyboard and trackball events to the terminal

`soundtest.py` generates a one-second sine wave tone



## Browser

This repo contains a tiny experimental webbrowser. It understands only blocks of text and links.
It does not support css or javascript or images and it barely understands HTML text. You probably
shouldn't use it.


The parser takes in a giant text string and yields a stream of blocks. A block is
either a text block or a header.  The block contains a list of spans. A span
can be either plain text or styled (link, bold, etc). Nested spans are not supported and
will be flattened.


The core parser algorithm works like this:

* look at each character in the input text
* if an element is being opened
  * parse the rest of the open element's attributes
  * put the element on the element stack
  * advance the cursor
* if text (not inside an element) then
  * append a span to the current span list
* if an element is being closed
  * pop the element off of the stack
  * put all of the current runs inside the element
  * return the element


* `<b>text</b>` -> `['b',{},'text']`
* `<p>some\nmultiline\ntext</p>` -> `['p',{},['some multiline text']`
* `<p>before <b>during</b> after</p>` -> `['p', {}, ['text',{},'before', ['b',`

```
<b>bold text</b> -> ['b', ['text','bold text']]

<p>some
multiline
text</p> -> ['p', ['text','some multiline text']]


['p', {}, [
  ['text','before',{}],
  ['b','during',{}],
  ['text','after',]
]]


<html>
<body>
<div>
before text
<p>some text</p>
<p>some more text</p>
and inbetween text
<p>some more text</p>
the finishing text
</div>
</body>
</html>

->

['block',['text,'before text']]
['p',['text','some text']]
['p',['some more text']]
['text',['and inbetween text']]
['p',['some more text']]
['block',['text','the finishing text']]



```



## line breaker takes in chunks

