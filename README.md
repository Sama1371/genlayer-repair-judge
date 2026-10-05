# RepairJudge

GenLayer intelligent contract that judges whether a repair fixed the reported problem.

The buyer opens a case. The seller submits a before link and an after link. Resolve fetches both pages and returns fixed, partial, or failed with a short reason.

Deployed contract:
https://explorer-studio.genlayer.com/address/0xEA5FCFAb6143B5F5e05E2e36eCe96867F890AB09

Tested flow: open_case, submit_before, submit_after, resolve, get_case.
Case 1 returned failed because the two sample pages showed no repair.
