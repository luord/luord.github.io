from feedgenerator.django.utils.xmlutils import SimplerXMLGenerator

from pelican.signals import feed_written

def add_icon(path, context, feed):
    with open(path, 'w') as fp:
        handler = SimplerXMLGenerator(fp, 'utf-8')
        handler.startDocument()
        handler.startElement('feed', feed.root_attributes())
        feed.add_root_elements(handler)
        handler.addQuickElement('icon', context['SITEURL']+context['USER_LOGO_URL'])
        feed.write_items(handler)
        handler.endElement("feed")

def register():
    feed_written.connect(add_icon)