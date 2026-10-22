"""Basic usage examples for IMO Bench library.

This script demonstrates the most common use cases for loading and
working with IMO Bench datasets.
"""

from imobench import load_answerbench, load_proofbench, load_gradingbench


def example_basic_loading():
    """Example 1: Basic loading of datasets."""
    print("=" * 60)
    print("Example 1: Basic Loading")
    print("=" * 60)
    
    # Load all short-answer problems
    problems = load_answerbench()
    print(f"\nLoaded {len(problems)} problems from AnswerBench")
    
    # Display first problem
    first = problems[0]
    print(f"\nFirst problem:")
    print(f"  ID: {first.problem_id}")
    print(f"  Category: {first.category}")
    print(f"  Subcategory: {first.subcategory}")
    print(f"  Source: {first.source}")
    print(f"  Problem: {first.problem[:100]}...")
    print(f"  Answer: {first.short_answer}")


def example_filtering():
    """Example 2: Filtering datasets."""
    print("\n" + "=" * 60)
    print("Example 2: Filtering")
    print("=" * 60)
    
    # Filter by category
    algebra_problems = load_answerbench(category="Algebra")
    print(f"\nAlgebra problems: {len(algebra_problems)}")
    
    # Filter by subcategory
    inequalities = load_answerbench(
        category="Algebra",
        subcategory="Inequality"
    )
    print(f"Algebra inequalities: {len(inequalities)}")
    
    # Filter proof problems by difficulty
    easy_proofs = load_proofbench(level="IMO-easy")
    print(f"Easy proof problems: {len(easy_proofs)}")


def example_category_analysis():
    """Example 3: Analyzing category distribution."""
    print("\n" + "=" * 60)
    print("Example 3: Category Analysis")
    print("=" * 60)
    
    problems = load_answerbench()
    
    # Count problems by category
    categories = {}
    for problem in problems:
        categories[problem.category] = categories.get(problem.category, 0) + 1
    
    print("\nProblems by category:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count}")


def example_subcategory_analysis():
    """Example 4: Analyzing subcategories within a category."""
    print("\n" + "=" * 60)
    print("Example 4: Subcategory Analysis")
    print("=" * 60)
    
    # Focus on Algebra problems
    algebra = load_answerbench(category="Algebra")
    
    # Count subcategories
    subcategories = {}
    for problem in algebra:
        subcategories[problem.subcategory] = \
            subcategories.get(problem.subcategory, 0) + 1
    
    print(f"\nAlgebra subcategories ({len(subcategories)} total):")
    for subcat, count in sorted(subcategories.items(), key=lambda x: -x[1]):
        print(f"  {subcat}: {count}")


def example_proofbench():
    """Example 5: Working with ProofBench."""
    print("\n" + "=" * 60)
    print("Example 5: ProofBench Exploration")
    print("=" * 60)
    
    # Load all proof problems
    proofs = load_proofbench()
    print(f"\nTotal proof problems: {len(proofs)}")
    
    # Analyze difficulty levels
    levels = {}
    for proof in proofs:
        levels[proof.level] = levels.get(proof.level, 0) + 1
    
    print("\nDifficulty distribution:")
    for level, count in sorted(levels.items()):
        print(f"  {level}: {count}")
    
    # Show example problem
    if proofs:
        example = proofs[0]
        print(f"\nExample problem ({example.problem_id}):")
        print(f"  Level: {example.level}")
        print(f"  Category: {example.category}")
        print(f"  Problem: {example.problem[:150]}...")


def example_gradingbench_lazy():
    """Example 6: Efficient GradingBench processing with lazy loading."""
    print("\n" + "=" * 60)
    print("Example 6: GradingBench with Lazy Loading")
    print("=" * 60)
    
    # Use lazy loading to process entries one at a time
    print("\nProcessing high-scoring entries (≥8 points)...")
    
    count = 0
    points_sum = 0
    
    for entry in load_gradingbench(min_points=8, lazy=True):
        count += 1
        points_sum += entry.points
        
        # Process first few as examples
        if count <= 3:
            print(f"\n  Entry {count}:")
            print(f"    Grading ID: {entry.grading_id}")
            print(f"    Problem ID: {entry.problem_id}")
            print(f"    Points: {entry.points}/10")
            print(f"    Response: {entry.response[:100]}...")
        
        # Stop after processing 100 for this example
        if count >= 100:
            break
    
    if count > 0:
        avg_points = points_sum / count
        print(f"\nProcessed {count} entries")
        print(f"Average points: {avg_points:.2f}/10")


def example_source_analysis():
    """Example 7: Analyzing problem sources."""
    print("\n" + "=" * 60)
    print("Example 7: Source Analysis")
    print("=" * 60)
    
    problems = load_answerbench()
    
    # Count problems by source
    sources = {}
    for problem in problems:
        sources[problem.source] = sources.get(problem.source, 0) + 1
    
    print(f"\nMost common sources:")
    for source, count in sorted(sources.items(), key=lambda x: -x[1])[:10]:
        print(f"  {source}: {count} problems")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("IMO BENCH LIBRARY - USAGE EXAMPLES")
    print("=" * 60)
    
    try:
        example_basic_loading()
        example_filtering()
        example_category_analysis()
        example_subcategory_analysis()
        example_proofbench()
        example_gradingbench_lazy()
        example_source_analysis()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure the imobench data directory is accessible.")
        print("You may need to specify a custom data directory:")
        print("\n  from imobench import IMOBenchLoader")
        print("  from pathlib import Path")
        print("  loader = IMOBenchLoader(data_dir=Path('/path/to/imobench'))")


if __name__ == "__main__":
    main()
