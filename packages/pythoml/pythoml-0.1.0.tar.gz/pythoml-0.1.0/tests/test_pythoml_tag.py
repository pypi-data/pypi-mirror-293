import unittest

from pythoml.tag import Tag, tag_factory

class PytmlTagTestCase(unittest.TestCase):
    def test_tag_factory_output(self):
        # Test tag_factory with default settings
        TestTag = tag_factory(tag="test")
        self.assertIsInstance(TestTag, type)
        self.assertTrue(issubclass(TestTag, Tag))
    
    def test_tag_factory_output_with_custom_settings_braces(self):
        # Test tag_factory with custom settings
        TestTag = tag_factory(tag="test", braces=("{", "}"))
        test_tag = TestTag()
        self.assertEqual(test_tag.render(), "{test}\n{/test}")

    def test_tag_factory_output_with_custom_settings_content_delimiter(self):
        # Test tag_factory with custom settings
        TestTag = tag_factory(tag="test", content_delimiter="\t")
        test_tag = TestTag("foo", "bar")
        self.assertEqual(test_tag.render(), "<test>\t  foo\t  bar\t</test>")

    def test_tag_factory_output_with_custom_settings_indentation(self):
        # Test tag_factory with custom settings
        TestTag = tag_factory(tag="test", indentation="    ")
        test_tag = TestTag("content")
        self.assertEqual(test_tag.render(), "<test>\n    content\n</test>")

    def test_tag_factory_output_with_custom_settings_has_closer(self):
        # Test tag_factory with custom settings
        TestTag = tag_factory(tag="test", has_closer=False)
        test_tag = TestTag()
        self.assertEqual(test_tag.render(), "<test>")

    def test_tag_basic_render(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag()
        self.assertEqual(test_tag.render(), "<test>\n</test>")

    def test_tag_with_content_render(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag("Hello, world!")
        self.assertEqual(test_tag.render(), "<test>\n  Hello, world!\n</test>")

    def test_tag_with_kwargs_render(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag(id_="test-id")
        self.assertEqual(test_tag.render(), '<test id="test-id">\n</test>')

    def test_tag_with_flags_render(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag(disabled=True)
        self.assertEqual(test_tag.render(), '<test disabled>\n</test>')

    def test_tag_with_flags_disabled_render(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag(disabled=False)
        self.assertEqual(test_tag.render(), "<test>\n</test>")

    def test_tag_with_content_kwargs_and_flags_render(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag("Hello, world!", id_="test-id", disabled=True)
        self.assertEqual(test_tag.render(), '<test id="test-id" disabled>\n  Hello, world!\n</test>')

    def test_tag_with_nested_tags_render(self):
        TestTag = tag_factory(tag="test")
        NestTag = tag_factory(tag="nest")
        test_tag = TestTag(NestTag("Hello, world!"))
        self.assertEqual(test_tag.render(), "<test>\n  <nest>\n    Hello, world!\n  </nest>\n</test>")

    def test_tag_add_method(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag()
        test_tag.add("Hello, world!")
        self.assertEqual(test_tag.render(), "<test>\n  Hello, world!\n</test>")

    def test_tag_set_method(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag()
        test_tag.set(id_="test-id")
        self.assertEqual(test_tag.render(), '<test id="test-id">\n</test>')

    def test_tag_set_method_with_flags(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag()
        test_tag.set(disabled=True)
        self.assertEqual(test_tag.render(), '<test disabled>\n</test>')

    def test_tag_set_method_with_flags_disabled(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag()
        test_tag.set(disabled=False)
        self.assertEqual(test_tag.render(), "<test>\n</test>")

    def test_tag_call_method(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag()
        test_tag("Hello, world!")
        self.assertEqual(test_tag.render(), "<test>\n  Hello, world!\n</test>")

    def test_tag_call_method_with_kwargs(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag()
        test_tag(id_="test-id")
        self.assertEqual(test_tag.render(), '<test id="test-id">\n</test>')

    def test_tag_call_method_with_flags(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag()
        test_tag(disabled=True)
        self.assertEqual(test_tag.render(), '<test disabled>\n</test>')

    def test_tag_call_method_with_flags_disabled(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag()
        test_tag(disabled=False)
        self.assertEqual(test_tag.render(), "<test>\n</test>")

    def test_tag_call_method_with_content_kwargs_and_flags(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag()
        test_tag("Hello, world!", id_="test-id", disabled=True)
        self.assertEqual(test_tag.render(), '<test id="test-id" disabled>\n  Hello, world!\n</test>')

    def test_tag_call_method_chain(self):
        TestTag = tag_factory(tag="test")
        test_tag = TestTag()
        test_tag("Hello, world!").set(id_="test-id").add("Another line.")
        self.assertEqual(test_tag.render(), '<test id="test-id">\n  Hello, world!\n  Another line.\n</test>')

    def test_tag_html_like_syntax(self):
        TestTag = tag_factory(tag="test")
        NestTag = tag_factory(tag="nest")
        test_tag = TestTag(id_="test-id", disabled=True)(
            "Hello, world!",
            NestTag("Nested content.")
        )
        self.assertEqual(test_tag.render(), '<test id="test-id" disabled>\n  Hello, world!\n  <nest>\n    Nested content.\n  </nest>\n</test>')
