---
top_title: pyreveal, a python package for converting markdown to reveal.js slides
project_name: pyreveal
smart_title: a markdown to revealjs engine 
author: wcchin
short_description: a python package for converting markdown to reveal.js slides
keywords: [revealjs, markdown, python]
three_concepts: [':typcn-lightbulb:', ':fab-markdown:', ':fas-chart-area:']
three_desc: [get some idea, write with markdown, and present it]
concept_color: '#33C3F0'
project_url: https://github.com/wcchin/pyreveal
project_url_title: go to project page
theme: skeleton
carlae_dir: carlae_page
---

# pyreveal
**a python package for converting markdown to reveal.js slides**

*Also, check the remark.js alternative as well: [pyremark_slides](https://github.com/wcchin/pyremark_slides). I am using this for my recent internal meeting presentations.*

## a demo
[![pyreveal demo video](http://wcchin.github.io/images/pyrev_demo_vimeo.png)](https://vimeo.com/226295024)



## After some time

About two years ago, I wrote pyreveal to automate the conversion from MD to slides in html powered with reveal.js (with my own flavor of syntax). After that, I was busying on my researches and dissertation writing etc., thus abandoned this project for a while. 

During the two years, I tried some other ways to generate slides. For my formal presentations (my defense and interviews) I used Google Slides, because it is more stable and easy to change (drag and drop etc). For some smaller discussion, I tried Marp (which is a great project). There are quite a lot of alternative out there. I love Marp and even thinking on writing my own theme to use with it. But then I realize that they stop the development and maintenances of Marp desktop app. They are moving forward to newer ecosystem, and the desktop app is part of the future product, i.e. currently no available. Their documentation on using the alternative cloud version is not that complete, I can't find an easy way to do it (like read the instruction and done by 10 mins), so I give up on them for now (and keep the discontinued Marp desktop app for some quick use situation). 

GitPitch is another promising and **seems like** a very good piece of work. The cloud version works as simple as forking the example. But there is some confusion in the documentation. I am trying to use their so called "**GitPitch Desktop Free Edition**" that is listed under the "**Free - The basic plan for everyone on GitHub, GitLab, and Bitbucket - $ 0**. But I wasted 1 hour to read the doc and install docker blablabla.... and to find the *GitPitch Desktop Access Management* for to get the approval for downloading the docker image. After wasted 1 hour on it, I gave up on them. **ALL desktop application leads to the subscribe on non-free plan**. Well, I actually don't like so much on the docker way to start the desktop app also....

So, without other quick way to generate slides from MD for now, I back to my old project. 

This time, I updated the reveal.js version, added some really nice plugin (menu, simple-menu, katex, verticator, pdfexport, and title-footer). The toc plugin is replaced by the menu and simple-menu. To use the simple-menu, I added a new way (syntax, i.e. ---chapter=) to name the chapter in the python script; to use the tex style equation, the katex needed to be copied to the current slide html dir; and of course fixed some small bugs. 

One big change I have done this time is dropped the Phantom.js and decktape.js, to keep things as simple as possible (no need to npm install any thing now). I also copied the docdata into the pyreveal package, because I don't know why pip install docdata will lead to some weird situation. This would be more intuitive and less dependencies nightmare. 

The current dependencies included:

- jinja2
- markdown
- watchdog

## Why another converter?

Previously, I was(am) using jupyter to create a notebook with slides, and convert it using jupyter+nbconvert, and even wrote some codes to customize the output html file~~, and convert to pdf using <a href="https://github.com/astefanutti/decktape" target="blank">phantomjs+decktape</a> automatically~~. So, the nbconvert can do the conversion from notebook to reveal.js. 

But, I don't understand why they keep the cell tags, which make it a pain while customizing the themes, and the custom.css, that following the tutorials or answers from stackoverflow to customize the reveal.js (the js), the codes will not work for the nbconvert version of slides.html. 

Plus, the speaker notes function is still not working for jupyter+nbconvert. ~~not sure about this for now~~

One more thing, if you change the contents in the notebook cell, you will need to run the nbconvert command again to generate the static html file. 
What we need, is that the static html file can be generated automatically, and we can see the result as soon as we change the md file.

Therefore, I decided to write a converter that take a simple md, and convert it to reveal.js slides using jinja2. 

# Getting started

## Demo

a demo is <a href="https://wcc-slides.netlify.com/2017/pyreveal/demo.slides.html#/" target="blank">here</a>. 

The codes that generate the demo slides is in the slide_dir directory.

## Install

```sh

git clone https://github.com/wcchin/pyreveal.git
cd pyreveal
pip install -e .

```

## Using

1. cd your_slides_dir
2. create a file named whatever.md (with .md extension)
3. follow the instruction in the following sections and write the slides content inside the whatever.md 
4. run the command, see the following "usage" section
5. if the '-w' is used in the command, the slides will change according to the modification of the whatever.md file (and custom.css). 
6. done

# Documentation

## slides configuration

pyreveal will read the first several lines of the whatever.md file and get the metadata as the configs, using the <a href="https://github.com/waylan/docdata" target="blank">**docdata**</a> package . 

```markdown

title: reveal.js The HTML Presentation Framework
theme: black
transition: concave
cr_word: author - 2017
cr_color: rgba(205,205,205,0.0)
toc: False
to_pdf: false
reveal_path: reveal.js

```

configs:
- title: will be put at the `<title>` part of the `<head>` of the html
- theme: available: black (default), white, league, sky, beige, simple, serif, blood, night, moon, solarized and... (THERE ARE MORE THEME FROM MY THEME DIR)
- transition: none(default), fade, slide, convex, concave, zoom, page
- cr_word: CopyRight word (optional), the words that appear at the footer
- cr_color: color for the cr_word (optional), default to 'rgba(205,205,205,0.0)'
- toc: use the table of content plugin (not tested yet)
- to_pdf: default to false, if true, will create a pdf version of the slides, using phantomjs. to use the to_pdf function, please check and install phantomjs following the <a href="https://github.com/astefanutti/decktape">decktape instruction</a> and <a href="http://phantomjs.org/" target="blank">phantomjs instruction</a>.
- reveal_path: optional, default to 'reveal.js'(the same directory as the output html)

## the special keyword for generating slides and some other functions

pyreveal use a list of escape keyword to generate the function for reveal.js:

```markdown

---keyword

```

where, the *keyword* include: right, down, data*, style*, fragment, notes

## slides break
there are two types of slides break:

```markdown

---right

```

the following slide will appear at right, i.e. a new slide (section).

OR, 

```markdown

---down

```

the following slide will appear at bottom, i.e. a subslide. 

## slide background and style

```markdown

---data*
---style*

```

just same as the reveal.js, they use data-background or something similar to change the per-slide styles.
Therefore, pyreveal will check if there is a ---data-something, then it will put the data-something into and something like the <section data-something> will be generate. 

The same goes for style. 

For more detail, check the corresponding demo.md file that generate something similar to the demo in the original reveal.js website. 

## fragment

for fragment, pyreveal also use something like this:

```markdown

---fragment
this will appear after right or down is press
---fragment_grow
this will grow next

```

pyreveal will just put the tag after the '---' (with replacing the '_' with a blank space) into the <p class="{{ here }}">. So all kind of fragment styles will be supported as they should be in the reveal.js. 

Just some minor different, that shows in the demo file, the word "highlight" does not sit at there at first.

## speaker notes

finally, the speaker notes. 

the speaker notes should be put at the last of each slide, after the tag.
```markdown

---notes
this is the speaker notes
line 2 
line 3

```



# something new

## to use simple-menu

simple-menu is the links on top of the slide, check this plugin page: [the plugin for a simple and nice top or bottom menu bar](https://github.com/Martinomagnifico/reveal.js-simplemenu).

at the very top of the md file, add:

```markdown
use_simplemenu: true
menu_bottom: false 
```

or true if you want the menu at the bottom, change menu_bottom to: true

if the use_simplemenu is set to false, it will force the slide to ignore the chapter name and not showing them. 

on each top slide, add

```markdown
---chapter=some fancy title
```

the "some fancy title" will be on the top of the slide now

## to use menu

menu is the one that can be toggle by clicking the button at the bottom left, and it appear on the left hand side, as a slides tree. [the plugin for slide-out menu for reveal.js](https://github.com/denehyg/reveal.js-menu).

to use this, simply add

```markdown
use_menu: true
```

at the top setting area. 

## to use katex

if there is any latex equation, remember to add

```markdown
use_katex: true
```

at the top setting area. [Katex for reveal.js plugin](https://github.com/JeremyHeleine/KaTeX-for-reveal.js). 



## to NOT use the footer title 

I just realize in the previous version, it is force to use the footer. So if not using it, remember to set:

```markdown
cr_word: --
```

it is two dashes. This will be recognize as not using them, thus not showing the title as previous version will do. 


# Usage

## run

run this and done.

```sh
pyreveal -i whatever.md -w
#or add python -m in front
```

The two arguments:
- -i: take a markdown file that contain the slides content (i.e. what you have prepared using the guidelines). 
- -w: watch the change (optional), and rerun the function if any changes happened, this is very useful for making the slide. press ctrl+c to exit watch. 

If the md file is in a sub-directory, simple use:

```sh
pyreveal -i subdir/whatever.md -w
#or add python -m in front
```

This will also work. And this is handy if the reveal path is set at the upper level (e.g. "../reveal.js") for share usage. 


## custom.css

Same as the output of the nbconvert, the output of the pyreveal will also try to read a custom.css at the same directory of the output html file. 
So, it is possible and easy to change something for the slides, e.g. change the fonts. 



# Next plan

Next thing to do should be try to read the jupyter notebook file, and convert the slides content from notebook to the reveal.js html. 
Because I still hope that the <cell> tags should be remove, and the speaker notes should be fixed.  


## addition themes
Recently, the material themes were dropped. Added a theme modified from league.css, file name: bstyle.css


Please try.
