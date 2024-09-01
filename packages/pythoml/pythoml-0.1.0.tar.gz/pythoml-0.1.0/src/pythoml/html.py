from typing import Callable, Type

from pythoml.tag import Tag, tag_factory


def make_html_doc(root_tag: Tag) -> str:
    return "<!DOCTYPE html>\n" + root_tag.render()


A: Type[Tag] = tag_factory(tag="a")

Abbr: Type[Tag] = tag_factory(tag="abbr")

Address: Type[Tag] = tag_factory(tag="address")

Area: Type[Tag] = tag_factory(tag="area")

Article: Type[Tag] = tag_factory(tag="article")

Aside: Type[Tag] = tag_factory(tag="aside")

Audio: Type[Tag] = tag_factory(tag="audio")

B: Type[Tag] = tag_factory(tag="b")

Base: Type[Tag] = tag_factory(tag="base", has_closer=False)

Bdi: Type[Tag] = tag_factory(tag="bdi")

Bdo: Type[Tag] = tag_factory(tag="bdo")

Blockquote: Type[Tag] = tag_factory(tag="blockquote")

Body: Type[Tag] = tag_factory(tag="body")

Br: Type[Tag] = tag_factory(tag="br", has_closer=False)

Button: Type[Tag] = tag_factory(tag="button")

Canvas: Type[Tag] = tag_factory(tag="canvas")

Caption: Type[Tag] = tag_factory(tag="caption")

Center: Type[Tag] = tag_factory(tag="center")

Cite: Type[Tag] = tag_factory(tag="cite")

Code: Type[Tag] = tag_factory(tag="code")

Col: Type[Tag] = tag_factory(tag="col", has_closer=False)

Colgroup: Type[Tag] = tag_factory(tag="colgroup")

Comment: Callable[[str], str] = lambda x: f"<!-- {x} -->" # noqa E731 - lambda is used for a simple function
# tag_factory(tag="", braces=("<!--", "-->"), has_closer=False)

Data: Type[Tag] = tag_factory(tag="data")

Datalist: Type[Tag] = tag_factory(tag="datalist")

Dd: Type[Tag] = tag_factory(tag="dd")

Del: Type[Tag] = tag_factory(tag="del")

Details: Type[Tag] = tag_factory(tag="details")

Dfn: Type[Tag] = tag_factory(tag="dfn")

Dialog: Type[Tag] = tag_factory(tag="dialog")

Div: Type[Tag] = tag_factory(tag="div")

Dl: Type[Tag] = tag_factory(tag="dl")

Dt: Type[Tag] = tag_factory(tag="dt")

Em: Type[Tag] = tag_factory(tag="em")

Embed: Type[Tag] = tag_factory(tag="embed", has_closer=False)

Fieldset: Type[Tag] = tag_factory(tag="fieldset")

Figcaption: Type[Tag] = tag_factory(tag="figcaption")

Figure: Type[Tag] = tag_factory(tag="figure")

Footer: Type[Tag] = tag_factory(tag="footer")

Form: Type[Tag] = tag_factory(tag="form")

H1: Type[Tag] = tag_factory(tag="h1")

H2: Type[Tag] = tag_factory(tag="h2")

H3: Type[Tag] = tag_factory(tag="h3")

H4: Type[Tag] = tag_factory(tag="h4")

H5: Type[Tag] = tag_factory(tag="h5")

H6: Type[Tag] = tag_factory(tag="h6")

Head: Type[Tag] = tag_factory(tag="head")

Header: Type[Tag] = tag_factory(tag="header")

Hgroup: Type[Tag] = tag_factory(tag="hgroup")

Hr: Type[Tag] = tag_factory(tag="hr", has_closer=False)

Html: Type[Tag] = tag_factory(tag="html")

I: Type[Tag] = tag_factory(tag="i") #noqa E741 - ambiguous variable name. 'I' is used to represent the 'i' tag

Iframe: Type[Tag] = tag_factory(tag="iframe")

Img: Type[Tag] = tag_factory(tag="img", has_closer=False)

Input: Type[Tag] = tag_factory(tag="input", has_closer=False)

Ins: Type[Tag] = tag_factory(tag="ins")

Kbd: Type[Tag] = tag_factory(tag="kbd")

Label: Type[Tag] = tag_factory(tag="label")

Legend: Type[Tag] = tag_factory(tag="legend")

Li: Type[Tag] = tag_factory(tag="li")

Link: Type[Tag] = tag_factory(tag="link", has_closer=False)

Main: Type[Tag] = tag_factory(tag="main")

Map: Type[Tag] = tag_factory(tag="map")

Mark: Type[Tag] = tag_factory(tag="mark")

Menu: Type[Tag] = tag_factory(tag="menu")

Meta: Type[Tag] = tag_factory(tag="meta", has_closer=False)

Meter: Type[Tag] = tag_factory(tag="meter")

Nav: Type[Tag] = tag_factory(tag="nav")

Noscript: Type[Tag] = tag_factory(tag="noscript")

Object: Type[Tag] = tag_factory(tag="object")

Ol: Type[Tag] = tag_factory(tag="ol")

Optgroup: Type[Tag] = tag_factory(tag="optgroup")

Option: Type[Tag] = tag_factory(tag="option")

Output: Type[Tag] = tag_factory(tag="output")

P: Type[Tag] = tag_factory(tag="p")

Param: Type[Tag] = tag_factory(tag="param", has_closer=False)

Picture: Type[Tag] = tag_factory(tag="picture")

Pre: Type[Tag] = tag_factory(tag="pre")

Progress: Type[Tag] = tag_factory(tag="progress")

Q: Type[Tag] = tag_factory(tag="q")

Rp: Type[Tag] = tag_factory(tag="rp")

Rt: Type[Tag] = tag_factory(tag="rt")

Ruby: Type[Tag] = tag_factory(tag="ruby")

S: Type[Tag] = tag_factory(tag="s")

Samp: Type[Tag] = tag_factory(tag="samp")

Script: Type[Tag] = tag_factory(tag="script")

Search: Type[Tag] = tag_factory(tag="search")

Section: Type[Tag] = tag_factory(tag="section")

Select: Type[Tag] = tag_factory(tag="select")

Small: Type[Tag] = tag_factory(tag="small")

Source: Type[Tag] = tag_factory(tag="source", has_closer=False)

Span: Type[Tag] = tag_factory(tag="span")

Strong: Type[Tag] = tag_factory(tag="strong")

Style: Type[Tag] = tag_factory(tag="style")

Sub: Type[Tag] = tag_factory(tag="sub")

Summary: Type[Tag] = tag_factory(tag="summary")

Sup: Type[Tag] = tag_factory(tag="sup")

Svg: Type[Tag] = tag_factory(tag="svg")

Table: Type[Tag] = tag_factory(tag="table")

Tbody: Type[Tag] = tag_factory(tag="tbody")

Td: Type[Tag] = tag_factory(tag="td")

Template: Type[Tag] = tag_factory(tag="template")

Textarea: Type[Tag] = tag_factory(tag="textarea")

Tfoot: Type[Tag] = tag_factory(tag="tfoot")

Th: Type[Tag] = tag_factory(tag="th")

Thead: Type[Tag] = tag_factory(tag="thead")

Time: Type[Tag] = tag_factory(tag="time")

Title: Type[Tag] = tag_factory(tag="title")

Tr: Type[Tag] = tag_factory(tag="tr")

Track: Type[Tag] = tag_factory(tag="track", has_closer=False)

U: Type[Tag] = tag_factory(tag="u")

Ul: Type[Tag] = tag_factory(tag="ul")

Var: Type[Tag] = tag_factory(tag="var")

Video: Type[Tag] = tag_factory(tag="video")

Wbr: Type[Tag] = tag_factory(tag="wbr", has_closer=False)
