from stix2 import ExternalReference


class Reference(object):
    default_url = "https://attack.mitre.org/"
    default_description = "No description available"

    def __init__(self, external_reference: ExternalReference):
        self.name = external_reference.source_name

        if hasattr(external_reference, 'url'):
            self.url = external_reference = external_reference.url
        else:
            self.url = self.default_url

        if hasattr(external_reference, 'description'):
            self.description = external_reference = external_reference.description
        else:
            self.description = self.default_description

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "description": self.description
        }
