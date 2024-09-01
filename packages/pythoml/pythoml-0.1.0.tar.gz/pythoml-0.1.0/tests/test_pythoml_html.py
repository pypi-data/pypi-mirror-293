import unittest

from pythoml import html

class PythomlHTMLTestCase(unittest.TestCase):
    def test_html_a(self):
        render = html.A("Visit W3Schools.com!", href="https://www.w3schools.com").render()
        expected = \
"""<a href="https://www.w3schools.com">
  Visit W3Schools.com!
</a>"""
        self.assertEqual(render, expected)

    def test_html_basic_site(self):
        render = html.make_html_doc(
            html.Html(
                html.Head(),
                html.Body(
                    html.H1("Heading"), 
                    html.Div(
                        html.P("This is a paragraph."),
                        class_="divclass"
                    ),
                )
            )
        )
        expected = \
"""<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <h1>
      Heading
    </h1>
    <div class="divclass">
      <p>
        This is a paragraph.
      </p>
    </div>
  </body>
</html>"""
        self.assertEqual(render, expected)

    def test_html_basic_site_html_syntax(self):
        render = html.make_html_doc(
            html.Html()(
                html.Head(),
                html.Body()(
                    html.H1("Heading"), 
                    html.Div(class_="divclass")(
                        html.P("This is a paragraph."),
                    ),
                )
            )
        )
        expected = \
"""<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <h1>
      Heading
    </h1>
    <div class="divclass">
      <p>
        This is a paragraph.
      </p>
    </div>
  </body>
</html>"""
        self.assertEqual(render, expected)