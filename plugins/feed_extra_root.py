from feedgenerator.django.utils.xmlutils import SimplerXMLGenerator

from pelican import signals

def add_tags(path, context, feed):
    with open(path, 'w') as fp:
        handler = SimplerXMLGenerator(fp, 'utf-8')
        handler.startDocument()
        handler.startElement('feed', feed.root_attributes())
        feed.add_root_elements(handler)
        for tag in context.get("FEED_EXTRA_ROOT_TAGS", []):
            handler.addQuickElement(**tag)
        feed.write_items(handler)
        handler.endElement("feed")

def register():
    signals.feed_written.connect(add_tags)
