"""CLI entry-point for the knowledge-graph prototype workflow.

Usage::

    python -m src generate-data [--seed 42]
    python -m src build-graph
    python -m src visualize
    python -m src qa "What type of account does customer 1001 have?"
"""

import argparse
import logging
import sys

from src.generate_data import generate_all
from src.graph_builder import build_graph
from src.visualize_graph import create_visualization
from src.qa import answer_question

logger = logging.getLogger(__name__)


def main() -> None:
    """Parse CLI arguments and dispatch to the appropriate pipeline step."""
    parser = argparse.ArgumentParser(
        description="Knowledge graph prototype workflow.",
    )
    parser.add_argument(
        "command",
        choices=["generate-data", "build-graph", "visualize", "qa"],
        help="Pipeline step to execute.",
    )
    parser.add_argument(
        "question",
        nargs="*",
        help="Question text (required for the 'qa' command).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Override the random seed used by generate-data.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    )

    if args.command == "generate-data":
        if args.seed is not None:
            import src.config as cfg
            cfg.RANDOM_SEED = args.seed
            logger.info("Random seed overridden to %d", args.seed)
        generate_all()

    elif args.command == "build-graph":
        build_graph()

    elif args.command == "visualize":
        create_visualization()

    elif args.command == "qa":
        if not args.question:
            logger.error("Please provide a question after 'qa'.")
            sys.exit(1)
        q = " ".join(args.question)
        print(answer_question(q))


if __name__ == "__main__":
    main()
