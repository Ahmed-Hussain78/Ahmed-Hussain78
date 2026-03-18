#!/usr/bin/env python3
"""MCQ Score Calculator

Calculate and display a score summary for multiple-choice question results.

Usage:
    python score.py <correct> <wrong> [--total <n>] [--negative <penalty>]

Examples:
    python score.py 33 5
    python score.py 33 5 --total 38
    python score.py 33 5 --total 40 --negative 0.25
"""

import argparse
import sys


def calculate_score(correct: int, wrong: int, total: int = 0, negative: float = 0.0) -> dict:
    """Calculate the MCQ score summary.

    Args:
        correct:  Number of correct answers.
        wrong:    Number of wrong answers.
        total:    Total number of questions (derived from correct + wrong if 0 or not supplied).
        negative: Marks deducted per wrong answer (default 0).

    Returns:
        A dictionary with keys: correct, wrong, total, skipped,
        raw_marks, final_marks, percentage.
    """
    if correct < 0 or wrong < 0:
        raise ValueError("correct and wrong counts must be non-negative")
    if negative < 0:
        raise ValueError("negative marking penalty must be non-negative")

    derived_answered = correct + wrong
    if total == 0:
        total = derived_answered
    elif total < derived_answered:
        raise ValueError(
            f"total ({total}) cannot be less than correct + wrong ({derived_answered})"
        )

    skipped = total - derived_answered
    raw_marks = float(correct)
    penalty = negative * wrong
    final_marks = raw_marks - penalty
    percentage = (final_marks / total * 100) if total > 0 else 0.0

    return {
        "correct": correct,
        "wrong": wrong,
        "skipped": skipped,
        "total": total,
        "raw_marks": raw_marks,
        "penalty": penalty,
        "final_marks": final_marks,
        "percentage": percentage,
    }


def format_summary(result: dict, negative: float = 0.0) -> str:
    """Return a human-readable score summary string."""
    lines = [
        "=" * 38,
        "       MCQ SCORE SUMMARY",
        "=" * 38,
        f"  Correct answers : {result['correct']}",
        f"  Wrong answers   : {result['wrong']}",
        f"  Skipped         : {result['skipped']}",
        f"  Total questions : {result['total']}",
        "-" * 38,
        f"  Raw marks       : {result['raw_marks']:.2f}",
    ]
    if negative > 0:
        lines.append(f"  Penalty (-{negative} x {result['wrong']}) : -{result['penalty']:.2f}")
    lines += [
        f"  Final marks     : {result['final_marks']:.2f}",
        f"  Percentage      : {result['percentage']:.2f}%",
        "=" * 38,
    ]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Calculate MCQ score summary with optional negative marking.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("correct", type=int, help="Number of correct answers")
    parser.add_argument("wrong", type=int, help="Number of wrong answers")
    parser.add_argument(
        "--total",
        type=int,
        default=0,
        metavar="N",
        help="Total number of questions (default: correct + wrong)",
    )
    parser.add_argument(
        "--negative",
        type=float,
        default=0.0,
        metavar="PENALTY",
        help="Marks deducted per wrong answer, e.g. 0.25 (default: 0)",
    )

    args = parser.parse_args(argv)

    try:
        result = calculate_score(args.correct, args.wrong, args.total, args.negative)
    except ValueError as exc:
        parser.error(str(exc))

    print(format_summary(result, args.negative))


if __name__ == "__main__":
    main()
