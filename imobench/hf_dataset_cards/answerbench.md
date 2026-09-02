---
language:
- en
license: cc-by-4.0
task_categories:
- question-answering
tags:
- mathematics
- reasoning
- math-olympiad
pretty_name: IMO-AnswerBench
size_categories:
- n < 1k
---

# IMO-AnswerBench

IMO-AnswerBench is a dataset of 400 challenging short-answer mathematical problems derived from national, regional, and international Math Olympiads (IMO, IMO Shortlist, USAMO, USAMTS, AIME, etc.). 

It is designed to evaluate the robust mathematical reasoning capabilities of AI models.

## Dataset Structure

The dataset contains the following columns:

- `Problem ID`: Unique identifier for each problem.
- `Problem`: The problem statement in LaTeX format.
- `Short Answer`: The gold standard final answer.
- `Category`: One of the four main IMO categories: Algebra, Combinatorics, Geometry, or Number theory.
- `Level`: Difficulty classification (pre-IMO, IMO-easy, IMO-medium, IMO-hard).
- `Subcategory`: Specific mathematical sub-topic.
- `Source`: The original competition source of the problem.

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
