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
parts = [eval(f"dict({p.strip()[1:-1]})") for p in parts.splitlines() if p.strip()]

def apply_rules(part: dict, rules: list[str]):
    for rule in rules:
        if '>' in rule:
            condition, next_workflow = rule.split(':')
            cat, value = condition.split('>')
            if part[cat] > int(value):
                return next_workflow
        if '<' in rule:
            condition, next_workflow = rule.split(':')
            cat, value = condition.split('<')
            if part[cat] < int(value):
                return next_workflow
        if rule == 'R':
            return rule
        if rule == 'A':
            return rule
    return rules[-1]


def accepted_parts(parts, workflows):
    workflows_rules = {}
    for w in workflows:
        ix = w.find("{")
        workflows_rules[w[:ix]] = w[ix+1:-1].split(",")
    
    accepted = []
    
    for p in parts:
        current = "in"
        while current not in ("A", "R"):
            current = apply_rules(p, workflows_rules[current])
        if current == "A":
            accepted.append(p)
    
    return accepted



final_parts = accepted_parts(parts, workflows)
print(final_parts)

accum = 0
for p in final_parts:
    for v in p.values():
        accum += v
print("result:", accum)
