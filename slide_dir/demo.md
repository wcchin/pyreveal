title: reveal.js The HTML Presentation Framework
theme: bstyle
transition: concave
cr_word: pyreveal - Benny
cr_color: rgba(205,205,205,0.0)
toc: False
to_pdf: false


# pyreveal
#### converting markdown and using python-jinja2 into 
### The HTML Presentation Framework

demo slides modified by Benny/@wcchin  
check [github/pyreveal](https://github.com/wcchin/pyreveal)

---right

## Hello There

reveal.js enables you to create beautiful interactive slide decks using HTML. This presentation will show you examples of what it can do.

---right

## Vertical Slides

Slides can be nested inside of each other.

Use the *Space* key to navigate through all slides.

<a href="#" class="navigate-down">
<img width="178" height="238" data-src="https://s3.amazonaws.com/hakim-static/reveal-js/arrow.png" alt="Down arrow">
</a>

---down

## Basement Level 1

Nested slides are useful for adding additional detail underneath a high level horizontal slide.

---down

## Basement Level 2

That's it, time to go back up.

<a href="#/2">
<img width="178" height="238" data-src="https://s3.amazonaws.com/hakim-static/reveal-js/arrow.png" alt="Up arrow" style="transform: rotate(180deg); -webkit-transform: rotate(180deg);">
</a>

---right

## Slides

Not a coder? Not a problem. There's a fully-featured visual editor for authoring these, try it out at <a href="http://slides.com" target="_blank">http://slides.com</a>.

---right

## Point of View

Press <strong>ESC</strong> to enter the slide overview.

Hold down alt and click on any element to zoom in on it using <a href="http://lab.hakim.se/zoom-js">zoom.js</a>. Alt + click anywhere to zoom back out.

---right

## Touch Optimized

Presentations look great on touch devices, like mobile phones and tablets. Simply swipe through your slides.

---right
---data-markdown
<script type="text/template">
    ## Markdown support

    Write content using inline or external Markdown.
    Instructions and more info available in the [readme](https://github.com/hakimel/reveal.js#markdown).

    ```
    <section data-markdown>
      ## Markdown support

      Write content using inline or external Markdown.
      Instructions and more info available in the [readme](https://github.com/hakimel/reveal.js#markdown).
    </section>
    ```
</script>

---right

## Fragments
Hit the next arrow...  
---fragment
...to step through ...  
---fragment
... a
---fragment
 fragmented
---fragment
 slide.

---notes
This slide has fragments which are also stepped through in the notes window.

---down

## Fragment Styles

There's different types of fragments, like:
---fragment_grow
grow
---fragment_shrink
shrink
---fragment_fade-out
fade-out
---fragment_fade-up
fade-up (also down, left and right!)
---fragment_current-visible
current-visible
---fragment_close
Highlight
---fragment_highlight-red
red
---fragment_highlight-blue
blue
---fragment_highlight-green
green

---right

## Transition Styles

You can select from different transitions, like: <br>
<a href="?transition=none#/8">None</a> -
<a href="?transition=fade#/8">Fade</a> -
<a href="?transition=slide#/8">Slide</a> -
<a href="?transition=convex#/8">Convex</a> -
<a href="?transition=concave#/8">Concave</a> -
<a href="?transition=zoom#/8">Zoom</a>

---right

## Themes

reveal.js comes with a few themes built in: <br>
<!-- Hacks to swap themes after the page has loaded. Not flexible and only intended for the reveal.js demo deck. -->
<a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/black.css'); return false;">Black (default)</a> -
<a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/white.css'); return false;">White</a> -
<a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/league.css'); return false;">League</a> -
<a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/sky.css'); return false;">Sky</a> -
<a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/beige.css'); return false;">Beige</a> -
<a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/simple.css'); return false;">Simple</a> <br>
<a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/serif.css'); return false;">Serif</a> -
<a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/blood.css'); return false;">Blood</a> -
<a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/night.css'); return false;">Night</a> -
<a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/moon.css'); return false;">Moon</a> -
<a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/solarized.css'); return false;">Solarized</a>

---right
---data-background="#dddddd"
## Slide Backgrounds

Set <code>data-background="#dddddd"</code> on a slide to change the background color. All CSS color formats are supported.
<a href="#" class="navigate-down">
<img width="178" height="238" data-src="https://s3.amazonaws.com/hakim-static/reveal-js/arrow.png" alt="Down arrow">
</a>

---down
---data-background="https://s3.amazonaws.com/hakim-static/reveal-js/image-placeholder.png"

## Image Backgrounds
<pre><code class="hljs">&lt;section data-background="image.png"&gt;</code></pre>

---down
---data-background="https://s3.amazonaws.com/hakim-static/reveal-js/image-placeholder.png"
---data-background-repeat="repeat"
---data-background-size="100px"

## Tiled Backgrounds
<pre><code class="hljs" style="word-wrap: break-word;">&lt;section data-background="image.png" data-background-repeat="repeat" data-background-size="100px"&gt;</code></pre>

---down
---data-background-video="https://s3.amazonaws.com/static.slid.es/site/homepage/v1/homepage-video-editor.mp4,https://s3.amazonaws.com/static.slid.es/site/homepage/v1/homepage-video-editor.webm"
---data-background-color="#000000"

<div style="background-color: rgba(0, 0, 0, 0.9); color: #fff; padding: 20px;">
    <h2>Video Backgrounds</h2>
    <pre><code class="hljs" style="word-wrap: break-word;">&lt;section data-background-video="video.mp4,video.webm"&gt;</code></pre>
</div>

---down
---data-background="http://i.giphy.com/90F8aUepslB84.gif"

## ... and GIFs!

---right
---data-transition="slide"
---data-background="#4d7e65"
---data-background-transition="zoom"

## Background Transitions

Different background transitions are available via the backgroundTransition option. This one's called "zoom".

<pre><code class="hljs">Reveal.configure({ backgroundTransition: 'zoom' })</code></pre>

---right
---data-transition="slide"
---data-background="#b5533c"
---data-background-transition="zoom"

## Background Transitions

You can override background transitions per-slide.

<pre><code class="hljs" style="word-wrap: break-word;">&lt;section data-background-transition="zoom"&gt;</code></pre>

---right

## Pretty Code
<pre><code class="hljs" data-trim contenteditable>
function linkify( selector ) {
  if( supports3DTransforms ) {

    var nodes = document.querySelectorAll( selector );

    for( var i = 0, len = nodes.length; i &lt; len; i++ ) {
      var node = nodes[i];

      if( !node.className ) {
        node.className += ' roll';
      }
    }
  }
}
</code></pre>

Code syntax highlighting courtesy of <a href="http://softwaremaniacs.org/soft/highlight/en/description/">highlight.js</a>.

---right
## Marvelous List
- No order here
- Or here
- Or here
- Or here

---down
## Fantastic Ordered List
1. One is smaller than...
2. Two is smaller than...
3. Three!

---right

## Tabular Tables

<table>
    <tr>
        <th>Item</th>
        <th>Value</th>
        <th>Quantity</th>
    </tr>
    <tr>
        <td>Apples</td>
        <td>1</td>
        <td>7</td>
    </tr>
    <tr>
        <td>Lemonade</td>
        <td>2</td>
        <td>18</td>
    </tr>
    <tr>
        <td>Bread</td>
        <td>3</td>
        <td>2</td>
    </tr>
</table>

---right

## Clever Quotes

These guys come in two forms, inline: <q cite="http://searchservervirtualization.techtarget.com/definition/Our-Favorite-Technology-Quotations"> 
&ldquo;The nice thing about standards is that there are so many to choose from&rdquo;</q> and block:
</p>
<blockquote cite="http://searchservervirtualization.techtarget.com/definition/Our-Favorite-Technology-Quotations">
    &ldquo;For years there has been a theory that millions of monkeys typing at random on millions of typewriters would
    reproduce the entire works of Shakespeare. The Internet has proven this theory to be untrue.&rdquo;
</blockquote>

> a markdown based block
> quote test

---right

## Intergalactic Interconnections

You can link between slides internally,<a href="#/2/3">like this</a>.

---right

## Speaker View

There's a <a href="https://github.com/hakimel/reveal.js#speaker-notes">speaker view</a>. It includes a timer, preview of the upcoming slide as well as your speaker notes.

Press the <em>S</em> key to try it out.

---notes
Oh hey, these are some notes. 
They'll be hidden in your presentation, but you can see them if you open the speaker notes window 
(hit 's' on your keyboard).

---right
## Export to PDF

Presentations can be <a href="https://github.com/hakimel/reveal.js#pdf-export">exported to PDF</a>, here's an example:</p>
<iframe data-src="https://www.slideshare.net/slideshow/embed_code/42840540" width="445" height="355" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:3px solid #666; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe>

---right

## Global State

Set <code>data-state="something"</code> on a slide and <code>"something"</code>
will be added as a class to the document element when the slide is open. This lets you
apply broader style changes, like switching the page background.

---right
---data-state="customevent"

## State Events
Additionally custom events can be triggered on a per slide basis by binding to the <code>data-state</code> name.

<pre><code class="javascript" data-trim contenteditable style="font-size: 18px;">
Reveal.addEventListener( 'customevent', function() {
	console.log( '"customevent" has fired' );
} );
</code></pre>

---right

## Take a Moment

Press B or . on your keyboard to pause the presentation. This is helpful when you're on stage and want to take distracting slides off the screen.

---right

## Much more

<ul>
    <li>Right-to-left support</li>
    <li><a href="https://github.com/hakimel/reveal.js#api">Extensive JavaScript API</a></li>
    <li><a href="https://github.com/hakimel/reveal.js#auto-sliding">Auto-progression</a></li>
    <li><a href="https://github.com/hakimel/reveal.js#parallax-background">Parallax backgrounds</a></li>
    <li><a href="https://github.com/hakimel/reveal.js#keyboard-bindings">Custom keyboard bindings</a></li>
</ul>

---right
---style="text-align: left;"

# THE END

- <a href="http://slides.com">Try the online editor</a> <br>
- <a href="https://github.com/hakimel/reveal.js">Source code &amp; documentation</a>


