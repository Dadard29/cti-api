from stix2 import IntrusionSet

from models.reference import Reference


class Group(object):
    def __init__(self, intrusion_set: IntrusionSet):
        self.id = intrusion_set.id
        self.created = intrusion_set.created
        self.modified = intrusion_set.modified
        self.name: str = intrusion_set.name
        self.description: str = intrusion_set.description
        self.aliases: list = intrusion_set.aliases
        self.references = [
            Reference(r) for r in intrusion_set.external_references
        ]

    def json(self):
        return {
            "_key": self.id,
            "created": str(self.created),
            "modified": str(self.modified),
            "name": self.name,
            "description": self.description,
            "aliases": self.aliases,
            "references": [
                ref.json() for ref in self.references
            ]
        }
