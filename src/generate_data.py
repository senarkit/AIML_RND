"""Generate synthetic customer, agent, and conversation CSV data.

The output files land in ``DATA_DIR`` (see :pymod:`src.config`) and are
consumed downstream by the graph-builder and QA modules.
"""

import csv
import datetime
import random
from pathlib import Path
from typing import Any

from src.config import DATA_DIR, RANDOM_SEED

# ---------------------------------------------------------------------------
# Field definitions
# ---------------------------------------------------------------------------
CUSTOMER_FIELDS: list[str] = [
    "customer_id",
    "customer_name",
    "account_type",
    "customer_segment",
    "region",
    "customer_status",
    "signup_date",
]

CONVERSATION_FIELDS: list[str] = [
    "conversation_id",
    "customer_id",
    "agent_id",
    "call_timestamp",
    "issue_category",
    "call_duration_seconds",
    "transcript",
    "transfer_count",
]

AGENT_FIELDS: list[str] = [
    "agent_id",
    "agent_name",
    "team",
    "skill_level",
    "active_since",
    "total_calls_handled",
    "total_transfers",
]

# ---------------------------------------------------------------------------
# Categorical constants
# ---------------------------------------------------------------------------
ACCOUNT_TYPES: list[str] = ["Checking", "Savings", "Business", "Premium", "Student"]
SEGMENTS: list[str] = ["Retail", "Small Business", "Enterprise", "VIP"]
REGIONS: list[str] = ["North", "South", "East", "West", "Central"]
STATUS_OPTIONS: list[str] = ["Active", "At Risk", "Dormant", "Churned"]
ISSUES: list[str] = [
    "Billing question",
    "Account access issue",
    "Card fraud report",
    "Service upgrade request",
    "Payment dispute",
    "Password reset",
    "Product inquiry",
]
TEAM_NAMES: list[str] = ["Inbound", "Outbound", "Support", "Retention"]
SKILL_LEVELS: list[str] = ["Junior", "Mid", "Senior"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _random_date(start: datetime.date, end: datetime.date) -> str:
    """Return an ISO-format date string for a random day in [start, end]."""
    delta_days = (end - start).days
    chosen = start + datetime.timedelta(days=random.randint(0, delta_days))
    return chosen.isoformat()


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    """Write a list of dicts to *path* as a CSV file."""
    with open(path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def generate_customers(count: int = 100) -> list[dict[str, Any]]:
    """Return *count* synthetic customer rows."""
    rows: list[dict[str, Any]] = []
    for i in range(1001, 1001 + count):
        rows.append(
            {
                "customer_id": str(i),
                "customer_name": f"Customer {i}",
                "account_type": random.choice(ACCOUNT_TYPES),
                "customer_segment": random.choice(SEGMENTS),
                "region": random.choice(REGIONS),
                "customer_status": random.choice(STATUS_OPTIONS),
                "signup_date": _random_date(
                    datetime.date(2020, 1, 1), datetime.date(2023, 12, 31)
                ),
            }
        )
    return rows


def generate_agents(count: int = 12) -> list[dict[str, Any]]:
    """Return *count* synthetic agent rows."""
    rows: list[dict[str, Any]] = []
    for i in range(501, 501 + count):
        rows.append(
            {
                "agent_id": str(i),
                "agent_name": f"Agent {i}",
                "team": random.choice(TEAM_NAMES),
                "skill_level": random.choice(SKILL_LEVELS),
                "active_since": _random_date(
                    datetime.date(2015, 1, 1), datetime.date(2019, 12, 31)
                ),
                "total_calls_handled": 0,
                "total_transfers": 0,
            }
        )
    return rows


def generate_conversations(
    customers: list[dict[str, Any]],
    agents: list[dict[str, Any]],
    count: int = 200,
) -> list[dict[str, Any]]:
    """Return *count* synthetic conversation rows.

    Each conversation references an existing customer and agent.
    """
    rows: list[dict[str, Any]] = []
    for i in range(9001, 9001 + count):
        customer = random.choice(customers)
        agent = random.choice(agents)
        transfer_count = random.choices([0, 1, 2], weights=[0.75, 0.20, 0.05])[0]

        # Pick issue once so transcript and field stay consistent
        issue = random.choice(ISSUES)
        transcript = (
            f"Customer {customer['customer_id']} called about {issue}. "
            f"Agent {agent['agent_id']} handled the interaction."
        )

        call_date = _random_date(
            datetime.date(2025, 1, 1), datetime.date(2025, 12, 28)
        )
        call_time = (
            f"{random.randint(8, 19):02d}:"
            f"{random.randint(0, 59):02d}:"
            f"{random.randint(0, 59):02d}"
        )

        rows.append(
            {
                "conversation_id": str(i),
                "customer_id": customer["customer_id"],
                "agent_id": agent["agent_id"],
                "call_timestamp": f"{call_date} {call_time}",
                "issue_category": issue,
                "call_duration_seconds": random.randint(60, 1800),
                "transcript": transcript,
                "transfer_count": str(transfer_count),
            }
        )
    return rows


def attach_agent_stats(
    agent_rows: list[dict[str, Any]],
    conversations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Aggregate call counts and transfer totals back onto agent rows."""
    handled: dict[str, int] = {agent["agent_id"]: 0 for agent in agent_rows}
    transfers: dict[str, int] = {agent["agent_id"]: 0 for agent in agent_rows}

    for conv in conversations:
        handled[conv["agent_id"]] += 1
        transfers[conv["agent_id"]] += int(conv["transfer_count"])

    for agent in agent_rows:
        agent["total_calls_handled"] = handled[agent["agent_id"]]
        agent["total_transfers"] = transfers[agent["agent_id"]]
    return agent_rows


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def generate_all() -> None:
    """Generate all synthetic CSV files into ``DATA_DIR``."""
    random.seed(RANDOM_SEED)
    customers = generate_customers()
    agents = generate_agents()
    conversations = generate_conversations(customers, agents)
    agents = attach_agent_stats(agents, conversations)

    _write_csv(DATA_DIR / "customers.csv", CUSTOMER_FIELDS, customers)
    _write_csv(DATA_DIR / "agents.csv", AGENT_FIELDS, agents)
    _write_csv(DATA_DIR / "conversations.csv", CONVERSATION_FIELDS, conversations)
    print(
        f"Generated {len(customers)} customers, {len(agents)} agents, "
        f"and {len(conversations)} conversations."
    )


if __name__ == "__main__":
    generate_all()
