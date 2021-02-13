from stix2 import Software

from models.reference import Reference


class Tool(object):
    def __init__(self, software: Software):
        self.id = software.id
        self.created = software.created
        self.modified = software.modified
        self.name = software.name
        self.description = software.description
        self.labels = software.labels
        self.references = [
            Reference(r) for r in software.external_references
        ]

    def json(self):
        return {
            "_key": self.id,
            "created": str(self.created),
            "modified": str(self.modified),
            "name": self.name,
            "description": self.description,
            "labels": self.labels,
            "references": [
                r.json() for r in self.references
            ]
        }
