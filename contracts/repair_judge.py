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

    def __init__(self):
        self.owner = gl.message.sender_address
        self.case_count = u256(0)

    @gl.public.write
    def open_case(self, problem: str) -> str:
        if len(problem.strip()) < 8:
            raise Exception("problem is too short")
        self.case_count = self.case_count + u256(1)
        case_id = str(self.case_count)
        self.problems[case_id] = problem.strip()
        self.before_url[case_id] = ""
        self.after_url[case_id] = ""
        self.status[case_id] = "open"
        self.reasons[case_id] = ""
        return case_id

    @gl.public.write
    def submit_before(self, case_id: str, url: str) -> str:
        if case_id not in self.problems:
            raise Exception("case not found")
        if self.status[case_id] != "open":
            raise Exception("case is not open")
        if not (url.startswith("http://") or url.startswith("https://")):
            raise Exception("before must be a link")
        self.before_url[case_id] = url.strip()
        self.status[case_id] = "before"
        return "before"

    @gl.public.write
    def submit_after(self, case_id: str, url: str) -> str:
        if case_id not in self.problems:
            raise Exception("case not found")
        if self.status[case_id] != "before":
            raise Exception("submit before first")
        if not (url.startswith("http://") or url.startswith("https://")):
            raise Exception("after must be a link")
        self.after_url[case_id] = url.strip()
        self.status[case_id] = "ready"
        return "ready"

    @gl.public.write
    def resolve(self, case_id: str) -> str:
        if case_id not in self.problems:
            raise Exception("case not found")
        if self.status[case_id] != "ready":
            raise Exception("submit both links first")
        problem = self.problems[case_id]
        before = self.before_url[case_id]
        after = self.after_url[case_id]

        def get_input() -> str:
            before_page = gl.nondet.web.render(before, mode="text")[:4000]
            after_page = gl.nondet.web.render(after, mode="text")[:4000]
            return (
                "Problem:\n" + problem
                + "\n\nBefore page:\n" + before_page
                + "\n\nAfter page:\n" + after_page
            )

        verdict = gl.eq_principle.prompt_non_comparative(
            get_input,
            task="Decide if the repair fixed the problem. First line must be FIXED, PARTIAL, or FAILED. Second line is one short reason.",
            criteria="The first line is exactly FIXED, PARTIAL, or FAILED. Use only the problem and the two pages.",
        )
        first = verdict.strip().splitlines()[0].strip().upper()
        if "FIXED" in first:
            self.status[case_id] = "fixed"
        elif "PARTIAL" in first:
            self.status[case_id] = "partial"
        else:
            self.status[case_id] = "failed"
        self.reasons[case_id] = verdict.strip()
        return self.status[case_id]

    @gl.public.view
    def get_case(self, case_id: str) -> str:
        if case_id not in self.problems:
            return ""
        return (
            self.status[case_id]
            + "|"
            + self.problems[case_id]
            + "|"
            + self.reasons[case_id]
        )

    @gl.public.view
    def get_case_count(self) -> str:
        return str(self.case_count)
