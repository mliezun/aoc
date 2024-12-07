workflows_parts = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


workflows_parts = open("input.txt", "r").read().strip()


workflows, parts = workflows_parts.split("\n\n")
workflows = [w.strip() for w in workflows.splitlines() if w.strip()]

CATEGORY_RANGE = (1, 4000)


class GenericPart:
    def __init__(self, x, m, a, s):
        self.part = {
            "x": x,
            "m": m,
            "a": a,
            "s": s,
        }

    def apply_rule(self, rule: str):
        if ">" in rule:
            condition, next_workflow = rule.split(":")
            cat, value = condition.split(">")
            new_part = GenericPart(**self.part)
            new_part.part[cat] = (int(value) + 1, self.part[cat][1])
            self.part[cat] = (self.part[cat][0], int(value))
            return new_part, next_workflow
        if "<" in rule:
            condition, next_workflow = rule.split(":")
            cat, value = condition.split("<")
            new_part = GenericPart(**self.part)
            new_part.part[cat] = (self.part[cat][0], int(value) - 1)
            self.part[cat] = (int(value), self.part[cat][1])
            return new_part, next_workflow
        if rule == "R":
            return GenericPart((0, 0), (0, 0), (0, 0), (0, 0)), rule
        if rule == "A":
            return GenericPart(**self.part), rule
        return GenericPart(**self.part), rule

    def __repr__(self) -> str:
        return f"{self.part}"

    def __str__(self) -> str:
        return repr(self)

    def sum(self):
        accum = 1
        for _, (min_val, max_val) in self.part.items():
            range_length = max_val - min_val + 1
            if range_length > 0:
                accum *= range_length
        return accum


def accepted_parts(workflows):
    workflows_rules = {}
    for w in workflows:
        ix = w.find("{")
        workflows_rules[w[:ix]] = w[ix + 1 : -1].split(",")

    accepted = []
    queue = [(GenericPart((1, 4000), (1, 4000), (1, 4000), (1, 4000)), "in")]
    while queue:
        part, current = queue.pop(0)
        for rule in workflows_rules[current]:
            new_part, next_workflow = part.apply_rule(rule)
            if next_workflow == "A":
                accepted.append(new_part)
            elif next_workflow != "R":
                queue.append((new_part, next_workflow))

    return accepted


ap = accepted_parts(workflows)
# print(ap)

print("result:", sum(map(lambda p: p.sum(), ap)))
