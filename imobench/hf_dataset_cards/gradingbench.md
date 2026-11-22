---
language:
- en
license: cc-by-4.0
task_categories:
- evaluation
tags:
- mathematics
- reasoning
- auto-grading
- human-evaluation
pretty_name: IMO-GradingBench
size_categories:
- 10k < n < 100k
---

# IMO-GradingBench

IMO-GradingBench is a large dataset designed to advance automatic evaluation of mathematical proofs. It contains over 186,000 grading entries (with a subset of 1,000 high-quality human gradings) for model-generated solutions to IMO Bench problems.

## Dataset Structure

The dataset contains the following columns:

- `Grading ID`: Unique identifier for the grading entry.
- `Problem ID`: Reference to the problem being graded.
- `Problem`: The problem statement.
- `Solution`: Reference ground-truth solution.
- `Grading guidelines`: Criteria used for grading.
- `Response`: The model-generated output being evaluated.
- `Points`: Numeric score assigned (0-10 or 0-7 scale depending on configuration).
- `Reward`: Qualitative category (Correct, Partial, Incorrect, etc.).
- `Problem Source`: Original competition source.

## Citation

```latex
@inproceedings{luong-etal-2025-towards,
    title = "Towards Robust Mathematical Reasoning",
    author  = {Thang Luong and Dawsen Hwang and Hoang H. Nguyen and Golnaz Ghiasi and Yuri Chervonyi and Insuk Seo and Junsu Kim and Garrett Bingham and Jonathan Lee and Swaroop Mishra and Alex Zhai and Clara Huiyi Hu and Henryk Michalewski and Jimin Kim and Jeonghyun Ahn and Junhwi Bae and Xingyou Song and Trieu H. Trinh and Quoc V. Le and Junehyuk Jung},
    booktitle = "Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing",
    year = "2025",
    url = "https://aclanthology.org/2025.emnlp-main.1794/",
}
```
