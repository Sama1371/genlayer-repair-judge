# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class RepairJudge(gl.Contract):
    owner: Address
    case_count: u256
    problems: TreeMap[str, str]
    before_url: TreeMap[str, str]
    after_url: TreeMap[str, str]
    status: TreeMap[str, str]
    reasons: TreeMap[str, str]
    case_owner: TreeMap[str, Address]
    evidence_submitter: TreeMap[str, Address]

    def __init__(self):
        self.owner = gl.message.sender_address
        self.case_count = u256(0)

    def _is_authorized(self, case_id: str) -> bool:
        sender = gl.message.sender_address
        return sender == self.case_owner[case_id] or sender == self.evidence_submitter[case_id
