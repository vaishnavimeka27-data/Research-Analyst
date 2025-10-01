# Task_07_Decision_Making: Ethical Implications of Generative Video

## Project Overview

This repository contains the materials for Research Task 7, an analysis of the ethical and practical implications of using generative AI video models like Google's Veo 3 for institutional content.

The core of this project is the `Decision_Report.pdf`, which provides actionable, risk-tiered recommendations to the iSchool's Communications Director based on a test case of creating a short educational video.

---

## Repository Structure
├── Decision_Report.pdf         # The final stakeholder-facing report.
├── README.md                   # This file.
├── outputs/
│   └── final_video.mp4         # (Link) The final video output from the test.
└── prompts/
└── veo_prompt_final.txt        # The original prompt used for the main test.

---

## Key Files

* **`Decision_Report.pdf`**: This is the main deliverable. It includes the project's findings, ethical analysis, and a three-tiered set of recommendations.
* **`prompts/veo_prompt_final.txt`**: The exact prompt used to generate the video, serving as the primary "data" for the analysis.

---

## How to Replicate

The analysis is based on Google's Veo 3 model. The methodology can be applied to other text-to-video models.

1.  Use the prompt in the `/prompts` folder to generate a video.
2.  Perform a qualitative analysis of the output, checking for prompt adherence, visual quality, and demographic representation.
3.  **Note:** To properly assess reliability and bias, it is recommended to run the same prompt multiple times and document any variations.

---

## Summary of Findings

* **High Visual Fidelity:** The model excels at creating visually impressive and coherent video clips that follow complex instructions.
* **Unknown Reliability:** A single successful test doesn't guarantee future performance. The potential for errors means **100% human review** of all generated content is essential.
* **Potential for Bias:** The single test run generated a stereotypical character, raising concerns about the model's default behavior. **Further testing is required** to determine the extent of this bias.
* **Factual Unreliability:** The model cannot be trusted to generate accurate information. Any educational audio must be **created and verified by a human**.

* **Link to Task 6 for more Info:** https://github.com/vaishnavimeka27-data/Research-Analyst/tree/main/09_01_2025_Submission_RA/Task_06_Deep_Fake