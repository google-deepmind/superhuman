# IMO Bench

See https://imobench.github.io for more info.

## Usage

*   IMO-AnswerBench: [answerbench_v2.csv](answerbench_v2.csv)
*   IMO-ProofBench: [proofbench_v2.csv](proofbench_v2.csv)
*   IMO-GradingBench: [gradingbench.csv](gradingbench.csv)
*   IMO-LeanProofBench: [lean_proof_bench.csv](lean_proof_bench.csv)

As of 05/29/2025, we updated IMO-ProofBench with `proofbench_v2.csv` to fix a
typo in PB-Advanced-022.
The previous version [proofbench.csv](proofbench.csv) is now deprecated.

As of 02/12/2026, we updated IMO-Answerbench with `answerbench_v2.csv` to fix
some problems that had ambiguous problem statements or incorrect answers.
The previous version [answerbench.csv](answerbench.csv) is now deprecated.

## Dataset Validation

To validate the integrity and schema of the IMO Bench CSV files, run:

```bash
python3 imobench/validate_imobench.py
...


## Acknowledgments

We would like to thank Mirek Olšák, Ashley Aragorn Khoo, Edward Lockhart,
Paul Lezeau, Calle Sönne, and Moritz Firsching for formalizing the Lean
problem statements in IMO-LeanProofBench.

We would like to thank Ashley Aragorn Khoo for spotting the typo in
IMO-ProofBench.

We would like to thank Xujie from Tsinghua University, Aiden Jung and Hyunwoo
Choi from MIT, Youngbeom Jin from Caltech, Jiwon Kang from Seoul National
University, and Vineet Gupta and Pranjal Awasthi from Google DeepMind for
helping identify the issues with IMO-AnswerBench!

## Citing this work

```
@inproceedings{luong-etal-2025-towards,
    title = "Towards Robust Mathematical Reasoning",
    author  = {Thang Luong and Dawsen Hwang and Hoang H. Nguyen and Golnaz Ghiasi and Yuri Chervonyi and Insuk Seo and Junsu Kim and Garrett Bingham and Jonathan Lee and Swaroop Mishra and Alex Zhai and Clara Huiyi Hu and Henryk Michalewski and Jimin Kim and Jeonghyun Ahn and Junhwi Bae and Xingyou Song and Trieu H. Trinh and Quoc V. Le and Junehyuk Jung},
    booktitle = "Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing",
    year = "2025",
    url = "https://aclanthology.org/2025.emnlp-main.1794/",
}
```

## License and disclaimer

Copyright 2025 Google LLC

All software is licensed under the Apache License, Version 2.0 (Apache 2.0); you
may not use this file except in compliance with the Apache 2.0 license. You may
obtain a copy of the Apache 2.0 license at:
https://www.apache.org/licenses/LICENSE-2.0

All other materials are licensed under the Creative Commons Attribution 4.0
International License (CC-BY). You may obtain a copy of the CC-BY license at:
https://creativecommons.org/licenses/by/4.0/legalcode

Unless required by applicable law or agreed to in writing, all software and
materials distributed here under the Apache 2.0 or CC-BY licenses are
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the licenses for the specific language governing
permissions and limitations under those licenses.

This is not an official Google product.
