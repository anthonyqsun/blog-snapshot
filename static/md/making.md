(04/14/2023)
@devlog @project @vue @sql @python @flask

# Making this site

>GH [See this project on Github](https://github.com/anthonyqsun/blog-snapshot/tree/main)

Documenting my projects is something I've always wanted to do, both to serve as a personal knowledgebase and to start building a presence online. However, previous attempts usually just stopped at some HTML/CSS with a few hyperlinks and images. It's been a year since I've last touched such a project, and I've picked up many useful things along the way, so I decided to have another go at it while documenting my process to serve as motivation to actually complete it.

## Vision
### Core:
- Homepage
- Blog template
- Markdown parser + SQL database
- Flask backend

### Extra:
- Tagging system
- Search on homepage
- Filter by tag on homepage
- Mobile-friendly

### Nice to haves:
- rtf implementation for subtitle
- comment section with votes (hide negative posts to croudsource spam protection)

## Specifics
### Markdown
Although I can customize the parser however I want, I'm going to stick with basic markdown alongside a tagging system inspired by [Spaces](https://spaceswriting.com/). I will also have a date published and date last modified. H1 headings (#) will be unique and be used as the title of the blog post. H2-H4 headings (## to ####) serve as subheadings. Dashes for lists (indents matter), brackets and parentheses for links, exclamation mark + bracket + parentheses for images, backticks for inline and block code, and some assortment of underscores and asterisks for text formatting. Double slashes (//) will denote comments. I'm also considering custom symbols for those "did you know?" or "in a nutshell" sections you might see in textbooks.

Normally, Markdown doesn't distinguish between a newline and other whitespace unless you add double spaces or escape the newline. I don't like that, so my implementation will allow for newlines out of the box.

### Blog template
The vision is for each subheading to have an accessible anchor link similar to how some [code documentation websites](https://docs.python.org/3/library/stdtypes.html#truth-value-testing) work. If commenting is available, there can be an option to refer to a specific block. Under the title, there will be a list of tags and the date last edited. There isn't much discretion to have here — it will be themed similarly to the homepage, and have a nice sans-serif font.

Both the homepage and blog template will make use of Jinja2 templating.

### Tags
This unassuming component will likely be the hardest to implement for me. I'm envisioning a row of tags underneath each blog post in the directory, with a sidebar that has a tag search, tag selection, and a show more button if the column eventually exceeds 10 tags.

## Process
I don't expect anything too groundbreaking to happen while making this project. It'll serve a more practical than educational purpose, save for perhaps learning Vue basics for reactive components. I was considering serving the markdown with the site and rendering the page entirely through frontend JS, but it won't load for browsers with javascript disabled and I don't particularly want my markdown files to be accessible client-side in case I comment something sensitive. Scrappy Python will do.

Originally when writing the specifics, I didn't consider using a database. However, when met with the need to retrieve titles and tags for each page, I figured enumerating a blog directory and parsing each file within it whenever I wanted to render the homepage's blog post directory wasn't efficient. To solve for the problem of not having an up-to-date database, I'll just rebuild it whenever the app is initialized; when I want to push new changes, I will upload my markdown file and restart the app to update.

//insert github link
---
### Day 1
I decided to get started on the more core component first: the markdown parser module. It involved creating a Database class, with some methods for adding blog posts and accessing specific data. I already began to feel the inefficiency of base sqlite3, as lists needed to be converted to strings to be stored in the database; that meant the tags list and the content of the post (after removing lines for date and tags) had to be converted back and forth. SQL is really useful for sorting, though, which is one of the reasons I picked it. Among the table columns is i_date_created that stores the value of an ordinal, which is something like the number of days since a specific moment in time. Converting the date to an integer makes it really easy to sort posts by chronological order later on. At this moment, I'm second guessing the possibility of implementing javascript as I wasn't sure how it would interface with the database.

This is probably my first time using so many instances of list comprehension. It's really nice for code readability when you are actually able to pull it off. Also, it sucks that Python classes don't have method overloading.

**Progress Summary:**
- Made database getting and setting logic
- Wrote procedure for populating database for a given markdown file, with components like ordinal dates for future features

---
### Day 2
Instead of storing the markdown lines back in the sql table as a string, I converted them into HTML and stored it that way instead. In the blog template, the body will just be rendered in a single jinja field. There were minor bugs here and there, but this was a relatively streamlined process. By the end, I had an unstyled version of my markdown as HTML.
![my mvp](static/md/imgs/making/mvppage.png)

Building the homepage was pretty straightforward as well. I drew on my prior experience using CSS grids to build the layout, and passed a list of the title, tags, and date created to the homepage (which has jinja template fields) using flask's `render_template()`.
![finished homepage](static/md/imgs/making/homepage.png)

As for the color of the tags, I used a method to convert the characters in the tag string to ASCII, and performed a modulo to get a hue number. I kept saturation and light constant so that every tag has a constant feel to it.
```
# util.py

OFFSET = -59

def colorGen(tag: str) -> str:
    h = int(''.join(str(ord(c)) for c in tag))
    return f"hsl({(h-OFFSET)%360}, 75%, 70%)"
```
![colored tags](static/md/imgs/making/tagcolored.png)

**Progress Summary:**
- Wrote markdown -> HTML parser
- Made homepage w/ blog directory
- Made flask app to serve homepage & interface w/ backend

---
### Day 3
The next step just constitutes playing with numbers until the styling of the blog post looks right. A lot of the work has already been done, like the tag list and the date display. I also added a `>GH` tag in my markdown parser to display the github logo.

I'm not quite sure how to implement syntax highlighting, though. I'll probably use a library for that later.

After working on this for a few days, I have a better idea of what I want to do next:
- syntax highlighting for block code
- img captions
- img click to enlarge
- redirect user to blog post when clicking on entry in directory
- back to top button
- 404 page
- scroll progress bar
- homepage directory search & filter by tag functionality
- comments
- "click to add description" rich text format buttons (make it work like a google docs field)
- anchor links to headings

Honestly, it sounds like a lot of things to worry about that aren't necessities before publishing this site. Perhaps I'll split half of it into a separate project. 

I made image captions right away, as that was pretty easy to check off the list. The redirect is simple too — I just needed to call a js function:
```
# html
onclick="redirect('{{post[0]}}')"

# js
function redirect(x) {
    window.location.href = x;
}
```

I also noticed that my previous implementation to handle whitespace in block code was incorrect — it only handled the first instance:
```
# markdownparser.py

# INCORRECT
def populate(self, filename: str) -> None:
    content = self.read(filename).split("\n")

    # findBounds(list, symbol1, symbol2) -> (first occurrence, second occurrence)
    blockBounds = self.findBounds(content, '```', '```')
    lines = [content[i] for i in range(len(content)) if content[i]!="" or (i>=blockBounds[0] and i<=blockBounds[1])]
    ...
     

# CORRECT
def populate(self, filename: str) -> None:
    content = self.read(filename).split("\n")
        
    blockLines = self.findAllIndicesWithin(content, "```")
    lines = [content[i] for i in range(len(content)) if content[i]!="" or i in blockLines]
    ...
```

The last core step is the 404 page.
![It's not a shameless plug if it's on my page.](static/md/imgs/making/404.png)

And that's it! I have a functional blog site.