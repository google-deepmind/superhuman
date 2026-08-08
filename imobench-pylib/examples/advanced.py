"""Advanced usage examples for IMO Bench library.

This script demonstrates more advanced patterns including:
- Custom data directories
- Cross-dataset analysis
- Performance optimization
- Error handling
"""

from pathlib import Path
from typing import Dict, List
from imobench import IMOBenchLoader
from imobench.types import AnswerBenchProblem, ProofBenchProblem, GradingBenchEntry
from imobench.exceptions import ValidationError, DataLoadError


def example_custom_loader():
    """Example 1: Using custom data directory."""
    print("=" * 60)
    print("Example 1: Custom Data Directory")
    print("=" * 60)
    
    # Specify custom location for IMO Bench data
    # Adjust this path to match your setup
    repo_root = Path(__file__).parent.parent.parent
    data_dir = repo_root / "imobench"
    
    try:
        loader = IMOBenchLoader(data_dir=data_dir)
        problems = loader.load_answerbench()
        print(f"\nSuccessfully loaded {len(problems)} problems from: {data_dir}")
    except Exception as e:
        print(f"\nError loading data: {e}")
        print("Adjust the data_dir path to match your setup")


def example_validation():
    """Example 2: Data validation and error handling."""
    print("\n" + "=" * 60)
    print("Example 2: Validation and Error Handling")
    print("=" * 60)
    
    loader = IMOBenchLoader()
    
    # Load with validation enabled (default)
    try:
        problems = loader.load_answerbench(validate=True)
        print(f"\nValidation passed! Loaded {len(problems)} valid problems")
    except ValidationError as e:
        print(f"\nValidation error: {e}")
    except DataLoadError as e:
        print(f"\nData loading error: {e}")
    
    # Disable validation for faster loading (if data is trusted)
    problems_fast = loader.load_answerbench(validate=False)
    print(f"Fast loading (no validation): {len(problems_fast)} problems")


def example_cross_dataset_analysis():
    """Example 3: Analyzing relationships across datasets."""
    print("\n" + "=" * 60)
    print("Example 3: Cross-Dataset Analysis")
    print("=" * 60)
    
    loader = IMOBenchLoader()
    
    # Load datasets
    proof_problems = loader.load_proofbench()
    grading_entries = loader.load_gradingbench()
    
    # Build index of proof problems
    proof_index: Dict[str, ProofBenchProblem] = {
        p.problem_id: p for p in proof_problems
    }
    
    # Analyze gradings per problem
    gradings_per_problem: Dict[str, List[GradingBenchEntry]] = {}
    for entry in grading_entries[:1000]:  # Sample first 1000
        if entry.problem_id not in gradings_per_problem:
            gradings_per_problem[entry.problem_id] = []
        gradings_per_problem[entry.problem_id].append(entry)
    
    print(f"\nAnalyzed {len(gradings_per_problem)} problems with gradings")
    
    # Find problems with most gradings
    top_graded = sorted(
        gradings_per_problem.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )[:5]
    
    print("\nMost graded problems:")
    for problem_id, entries in top_graded:
        if problem_id in proof_index:
            problem = proof_index[problem_id]
            avg_points = sum(e.points for e in entries) / len(entries)
            print(f"  {problem_id} ({problem.level}): "
                  f"{len(entries)} gradings, avg {avg_points:.1f} points")


def example_performance_optimization():
    """Example 4: Performance optimization techniques."""
    print("\n" + "=" * 60)
    print("Example 4: Performance Optimization")
    print("=" * 60)
    
    loader = IMOBenchLoader()
    
    # Strategy 1: Lazy loading for large datasets
    print("\nStrategy 1: Lazy loading")
    print("  Processing gradingbench entries one at a time...")
    
    count = 0
    for entry in loader.load_gradingbench(lazy=True):
        count += 1
        if count >= 1000:
            break
    
    print(f"  Processed {count} entries without loading entire dataset")
    
    # Strategy 2: Filtering at load time
    print("\nStrategy 2: Early filtering")
    print("  Loading only high-scoring entries...")
    
    high_scores = loader.load_gradingbench(min_points=9)
    print(f"  Loaded {len(high_scores)} high-scoring entries")
    
    # Strategy 3: Disable validation for trusted data
    print("\nStrategy 3: Fast loading (validation disabled)")
    
    import time
    start = time.time()
    problems_validated = loader.load_answerbench(validate=True)
    time_validated = time.time() - start
    
    start = time.time()
    problems_fast = loader.load_answerbench(validate=False)
    time_fast = time.time() - start
    
    print(f"  With validation: {time_validated:.3f}s")
    print(f"  Without validation: {time_fast:.3f}s")
    print(f"  Speedup: {time_validated/time_fast:.1f}x")


def example_statistical_analysis():
    """Example 5: Statistical analysis of datasets."""
    print("\n" + "=" * 60)
    print("Example 5: Statistical Analysis")
    print("=" * 60)
    
    loader = IMOBenchLoader()
    problems = loader.load_answerbench()
    
    # Analyze answer formats
    answer_types = {
        'numeric': 0,
        'algebraic': 0,
        'interval': 0,
        'set': 0,
        'other': 0,
    }
    
    for problem in problems:
        answer = problem.short_answer.strip()
        if answer.isdigit() or (answer.startswith('-') and answer[1:].isdigit()):
            answer_types['numeric'] += 1
        elif '$' in answer:
            answer_types['algebraic'] += 1
        elif 'infty' in answer or '[' in answer or '(' in answer:
            answer_types['interval'] += 1
        elif '{' in answer or '}' in answer:
            answer_types['set'] += 1
        else:
            answer_types['other'] += 1
    
    print("\nAnswer format distribution:")
    for format_type, count in sorted(answer_types.items(), key=lambda x: -x[1]):
        pct = 100 * count / len(problems)
        print(f"  {format_type}: {count} ({pct:.1f}%)")
    
    # Analyze problem statement lengths
    lengths = [len(p.problem) for p in problems]
    avg_length = sum(lengths) / len(lengths)
    min_length = min(lengths)
    max_length = max(lengths)
    
    print(f"\nProblem statement statistics:")
    print(f"  Average length: {avg_length:.0f} characters")
    print(f"  Shortest: {min_length} characters")
    print(f"  Longest: {max_length} characters")


def example_difficulty_analysis():
    """Example 6: Analyzing difficulty patterns in GradingBench."""
    print("\n" + "=" * 60)
    print("Example 6: Difficulty Analysis")
    print("=" * 60)
    
    loader = IMOBenchLoader()
    
    # Sample grading entries
    entries = loader.load_gradingbench()[:5000]
    
    # Score distribution
    score_dist = {i: 0 for i in range(11)}
    for entry in entries:
        score_dist[entry.points] += 1
    
    print("\nScore distribution (0-10 points):")
    print("  Score | Count | Percentage | Bar")
    print("  " + "-" * 50)
    
    max_count = max(score_dist.values())
    for score, count in sorted(score_dist.items()):
        pct = 100 * count / len(entries)
        bar_length = int(30 * count / max_count)
        bar = "█" * bar_length
        print(f"  {score:5d} | {count:5d} | {pct:6.1f}%   | {bar}")
    
    # Average scores by problem
    problem_scores: Dict[str, List[int]] = {}
    for entry in entries:
        if entry.problem_id not in problem_scores:
            problem_scores[entry.problem_id] = []
        problem_scores[entry.problem_id].append(entry.points)
    
    problem_avgs = {
        pid: sum(scores) / len(scores)
        for pid, scores in problem_scores.items()
    }
    
    # Find hardest and easiest problems
    sorted_problems = sorted(problem_avgs.items(), key=lambda x: x[1])
    
    print(f"\nEasiest problems (avg score):")
    for pid, avg in sorted_problems[-3:]:
        print(f"  {pid}: {avg:.2f}/10")
    
    print(f"\nHardest problems (avg score):")
    for pid, avg in sorted_problems[:3]:
        print(f"  {pid}: {avg:.2f}/10")


def main():
    """Run all advanced examples."""
    print("\n" + "=" * 60)
    print("IMO BENCH LIBRARY - ADVANCED EXAMPLES")
    print("=" * 60)
    
    try:
        example_custom_loader()
        example_validation()
        example_cross_dataset_analysis()
        example_performance_optimization()
        example_statistical_analysis()
        example_difficulty_analysis()
        
        print("\n" + "=" * 60)
        print("All advanced examples completed!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
