from stix2 import AttackPattern, KillChainPhase


class Technique(object):
    def __init__(self, attack_pattern: AttackPattern):
        self.id = attack_pattern.id
        self.name = attack_pattern.name
        self.created = attack_pattern.created
        self.modified = attack_pattern.modified
        self.description = attack_pattern.description
        self.kill_chain_phases = [p.phase_name for p in attack_pattern.kill_chain_phases]

    def json(self):
        return {
            "_key": self.id,
            "name": self.name,
            "created": str(self.created),
            "modified": str(self.modified),
            "description": self.description,
            "kill_chain_phases": self.kill_chain_phases
        }
