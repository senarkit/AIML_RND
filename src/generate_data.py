import csv
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

CUSTOMER_FIELDS = [
    "customer_id",
    "customer_name",
    "account_type",
    "customer_segment",
    "region",
    "customer_status",
    "signup_date",
]

CONVERSATION_FIELDS = [
    "conversation_id",
    "customer_id",
    "agent_id",
    "call_timestamp",
    "issue_category",
    "call_duration_seconds",
    "transcript",
    "transfer_count",
]

AGENT_FIELDS = [
    "agent_id",
    "agent_name",
    "team",
    "skill_level",
    "active_since",
    "total_calls_handled",
    "total_transfers",
]

ACCOUNT_TYPES = ["Checking", "Savings", "Business", "Premium", "Student"]
SEGMENTS = ["Retail", "Small Business", "Enterprise", "VIP"]
REGIONS = ["North", "South", "East", "West", "Central"]
STATUS_OPTIONS = ["Active", "At Risk", "Dormant", "Churned"]
ISSUES = [
    "Billing question",
    "Account access issue",
    "Card fraud report",
    "Service upgrade request",
    "Payment dispute",
    "Password reset",
    "Product inquiry",
]
TEAM_NAMES = ["Inbound", "Outbound", "Support", "Retention"]
SKILL_LEVELS = ["Junior", "Mid", "Senior"]


def _write_csv(path, fieldnames, rows):
    with open(path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_customers(count=100):
    rows = []
    for i in range(1001, 1001 + count):
        rows.append(
            {
                "customer_id": str(i),
                "customer_name": f"Customer {i}",
                "account_type": random.choice(ACCOUNT_TYPES),
                "customer_segment": random.choice(SEGMENTS),
                "region": random.choice(REGIONS),
                "customer_status": random.choice(STATUS_OPTIONS),
                "signup_date": f"202{random.randint(0,3)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            }
        )
    return rows


def generate_agents(count=12):
    rows = []
    for i in range(501, 501 + count):
        rows.append(
            {
                "agent_id": str(i),
                "agent_name": f"Agent {i}",
                "team": random.choice(TEAM_NAMES),
                "skill_level": random.choice(SKILL_LEVELS),
                "active_since": f"201{random.randint(5,9)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                "total_calls_handled": 0,
                "total_transfers": 0,
            }
        )
    return rows


def generate_conversations(customers, agents, count=200):
    rows = []
    for i in range(9001, 9001 + count):
        customer = random.choice(customers)
        agent = random.choice(agents)
        transfer_count = random.choices([0, 1, 2], weights=[0.75, 0.20, 0.05])[0]
        transcript = (
            f"Customer {customer['customer_id']} called about {random.choice(ISSUES)}. "
            f"Agent {agent['agent_id']} handled the interaction."
        )
        rows.append(
            {
                "conversation_id": str(i),
                "customer_id": customer["customer_id"],
                "agent_id": agent["agent_id"],
                "call_timestamp": f"2025-{random.randint(1,12):02d}-{random.randint(1,28):02d} {random.randint(8,19):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}",
                "issue_category": random.choice(ISSUES),
                "call_duration_seconds": random.randint(60, 1800),
                "transcript": transcript,
                "transfer_count": str(transfer_count),
            }
        )
    return rows


def attach_agent_stats(agent_rows, conversations):
    handled = {agent["agent_id"]: 0 for agent in agent_rows}
    transfers = {agent["agent_id"]: 0 for agent in agent_rows}
    for conv in conversations:
        handled[conv["agent_id"]] += 1
        transfers[conv["agent_id"]] += int(conv["transfer_count"])

    for agent in agent_rows:
        agent["total_calls_handled"] = handled[agent["agent_id"]]
        agent["total_transfers"] = transfers[agent["agent_id"]]
    return agent_rows


def generate_all():
    random.seed(42)
    customers = generate_customers()
    agents = generate_agents()
    conversations = generate_conversations(customers, agents)
    agents = attach_agent_stats(agents, conversations)

    _write_csv(DATA_DIR / "customers.csv", CUSTOMER_FIELDS, customers)
    _write_csv(DATA_DIR / "agents.csv", AGENT_FIELDS, agents)
    _write_csv(DATA_DIR / "conversations.csv", CONVERSATION_FIELDS, conversations)
    print(f"Generated {len(customers)} customers, {len(agents)} agents, and {len(conversations)} conversations.")


if __name__ == "__main__":
    generate_all()
