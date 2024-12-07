from collections import defaultdict
from typing import Optional


pages = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

pages = open("input.txt", "r").read().strip()

page_ordering = []
page_updates = []
for l in pages.splitlines():
    l = l.strip()
    if "|" in l:
        page_ordering.append([int(v) for v in l.split("|")])
    if "," in l:
        page_updates.append([int(v) for v in l.split(",")])


def page_is_correct(page_order: list[int], page_update: list[int]):
    a, b = page_order
    try:
        return page_update.index(a) <= page_update.index(b)
    except ValueError:
        return True


def middle_item(page: list[int]):
    if len(page) % 2 == 0:
        return (page[len(page) // 2] + page[len(page) // 2 + 1]) / 2
    return page[len(page) // 2]


def check_page_ordering(page_update, page_ordering):
    for page_order in page_ordering:
        if not page_is_correct(page_order, page_update):
            return page_order
    return None


def fix_page(page_update: list[int], page_order: list[int]):
    page_update = page_update.copy()
    try:
        a, b = page_order
        page_update.remove(a)
        page_update.insert(page_update.index(b), a)
    except ValueError:
        pass
    return page_update


result = 0
for page_update in page_updates:
    did_fail = False
    while page_order := check_page_ordering(page_update, page_ordering):
        did_fail = True
        page_update = fix_page(page_update, page_order)
    if did_fail:
        result += middle_item(page_update)

print(result)
