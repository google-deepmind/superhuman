---
language:
- en
license: cc-by-4.0
task_categories:
- theorem-proving
tags:
- mathematics
- reasoning
- math-olympiad
- proof
pretty_name: IMO-ProofBench
size_categories:
- n < 1k
---

# IMO-ProofBench

IMO-ProofBench consists of 60 proof-based mathematical problems, vetted by experts. Each problem includes a complete ground-truth solution and specific grading guidelines.

## Dataset Structure

The dataset contains the following columns:

- `Problem ID`: Unique identifier.
- `Problem`: The problem statement in LaTeX format.
- `Solution`: Full reference proof.
- `Grading guidelines`: Step-by-step criteria for scoring.
- `Category`: Main mathematical category.
- `Level`: Difficulty classification (IMO-easy, IMO-medium, IMO-hard).
- `Short Answer`: A brief summary of the final answer/result.
- `Source`: The original competition source.

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
