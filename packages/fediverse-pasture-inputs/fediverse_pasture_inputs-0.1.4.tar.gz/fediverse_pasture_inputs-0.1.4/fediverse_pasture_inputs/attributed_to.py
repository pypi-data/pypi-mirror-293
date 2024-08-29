# SPDX-FileCopyrightText: 2024 Helge
#
# SPDX-License-Identifier: MIT

from .types import InputData

attributed_to_examples = [
    {"attributedTo": "http://pasture-one-actor/actor", "content": "single element"},
    {
        "attributedTo": ["http://pasture-one-actor/actor"],
        "content": "single element as list",
    },
    {
        "attributedTo": [
            "http://pasture-one-actor/actor",
            "http://pasture-one-actor/second",
        ],
        "content": "two elements as list",
    },
]


data = InputData(
    title="attributedTo",
    frontmatter="""
""",
    filename="attributed_to.md",
    examples=attributed_to_examples,
    detail_table=False,
    support_table=False,
)
