import argparse

from src.generate_data import generate_all
from src.graph_builder import build_graph
from src.visualize_graph import create_visualization
from src.qa import answer_question


def main():
    parser = argparse.ArgumentParser(description="Knowledge graph prototype workflow.")
    parser.add_argument("command", choices=["generate-data", "build-graph", "visualize", "qa"], help="Step to execute")
    parser.add_argument("question", nargs="*", help="Question text for qa command")
    args = parser.parse_args()

    if args.command == "generate-data":
        generate_all()
    elif args.command == "build-graph":
        build_graph()
    elif args.command == "visualize":
        create_visualization()
    elif args.command == "qa":
        if not args.question:
            raise SystemExit("Please provide a question after qa")
        q = " ".join(args.question)
        print(answer_question(q))


if __name__ == "__main__":
    main()
