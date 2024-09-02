import markdown2


# https://github.com/trentm/python-markdown2/wiki/Extras
extras = [
    'header-ids',
    'tables',
    'fenced-code-blocks',
    'cuddled-lists',
    'footnotes',
    'nofollow',
    'pyshell',
    'smarty-pants',
    'mermaid',
]


markdowner = markdown2.Markdown(extras=extras)
