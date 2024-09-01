# Pythoml  
[![Tests](https://github.com/NixonInnes/pythoml/actions/workflows/tests.yml/badge.svg)](https://github.com/NixonInnes/pythoml/actions/workflows/tests.yml)  

Generate HTML with Python.  

Pythoml provides a set of classes which render into HTML tags, allowing you to define HTML in code.


> ⚠️ **CAUTION**  
> It is important to sanitise any strings from an external source (e.g. a user input or database) which are used to render anything in a browser (e.g. HTML).  
> Pythoml **does not** provide any sanitisation. It is up to the developer to include that where necessary. 

## Useage

The `Pythoml.html` module contains `Tag` classes for each [HTML5 tag](https://www.w3schools.com/TAGS/default.asp).  
The class names match their respective HTML tags, for example: `html.A` for `<a>...</a>` and `html.Div` for `<div>...</div>`.  
For the complete list please see [html.py](/src/pythoml/html.py).  

Creating a `Tag`:
```python
from Pythoml import html

ex = html.P("This is a paragraph")
```

Calling `render()` on a `Tag` will return the HTML string:
```python
print(ex.render())
```
Will print the following:
```html
<p>
  This is a paragraph
</p>
```

### Tag Construction
A `Tag` constructor accepts any number of arguments and keyword arguments (i.e. `*args, **kwargs`).

#### Arguments

Arguments (`*args`) are used for "content" which is nested inside the HTML tag.  

For example, in the code above we passed the string "*This is a paragraph*" to `html.P`, so it was rendered inside the HTML tag `<p>...</p>`.  

#### Keyword Arguments
Keyword Arguments (`**kwargs`) are used for the HTML tag attributes and flags.

When a keyword argument value is a string, it will be used as an attribute of the HTML tag. For example setting an attribute `name` on a `Div`:  
```python
ex = html.Div(name="myDiv")

print(ex.render())
"""
<div name="myDiv">
</div>
"""
```

> ℹ️ **INFO**  
> There are some special keys to avoid collisions with Python keywords (most notably `class_` for setting a tag class attribute).  
> Below is a list of the special keys, listed as `Python` -> `HTML`:  
> - `class_` -> `class`
> - `for_` -> `for`
> - `id_` -> `id`
> - `type_` -> `type`  


When a keyword argument value is a boolean, it will be used as a flag on the HTML tag. For example setting a `dialog` as open:
```python
ex = html.Dialog(open=True)

print(ex.render())
"""
<dialog open>
</dialog>
"""
```

### Nesting
`Tags` can be added to the "content" of other `Tags` to achieve the typical nesting of HTML:
```python
ex = html.Html(
    html.Body(
        html.H1("This is my Site"),
        html.Hr(),
        html.Div(
            html.P("Welcome to my website!")
        )
    )
)

print(ex.render())
"""
<html>
  <body>
    <h1>
      This is my Site
    </h1>
    <hr>
    <div>
      <p>
        Welcome to my website!
      </p>
    </div>
  </body>
</html>
"""
```

> ℹ️ **INFO**  
> `Tags` which represent "[void elements](https://www.w3.org/TR/2011/WD-html-markup-20110113/syntax.html#void-element)" do not support adding content.  
> If you add content to such a `Tag`, you will recieve a warning.


### Lazy Content & Attributes
You can lazily `add` content or `set` attributes on a `Tag`:
```python
ex = html.Div()
ex.add("Some content")
ex.set(name="myDiv")
print(ex.render())
"""
<div name="myDiv">
  Some content
</div>
"""
```

The `add` and `set` methods both return `Self`, which allows you to chain them:
```python
ex = html.Div()
ex.add("Some content").set(name="myDiv")
print(ex.render())
"""
<div name="myDiv">
  Some content
</div>
"""
```

Alternatively, you can also call the instanciated `Tag` to update the content and attributes simultaneously:
```python
ex = html.Div()
ex("Some content", name="myDiv")
print(ex.render())
"""
<div name="myDiv">
  Some content
</div>
"""
```

#### Alternative Syntax
The syntax shown up until now only uses the constructor to populate the `Tag` content and attributes. Since the examples have been relatively simple, it does not highlight a minor grievance (at least to me...) with this approach.  
Consider the following:  
```python
ex = html.Div(
    html.H1("Title", class_="display-4")
    html.Div(
        html.H3("Subtitle"),
        html.Div(
            html.P("Some content"),
            class_="card"
        ),
    ),
    class_="container p-3" # <-- who does this belong to?
)
```
With big ugly nests like this, it gets difficult to determine which `Tag` the attributes are associated with.  
Since we can lazily add content, an alternative to the above is:
```python
ex = html.Div(class_="container p-3")(
    html.H1("Title", class_="display-4"),
    html.Div(
        html.H3("Subtitle"),
        html.Div(class_="card")(
            html.P("Some content"),
        ),
    ),
)
```
