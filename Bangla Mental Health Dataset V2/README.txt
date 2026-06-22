Title: Bangla Mental Health Dataset V2

Author: Esfer Sami

---

📘 Overview
This dataset contains 10,000 synthetically generated Bangla mental health conversations. It is designed to support research and development in natural language processing (NLP), particularly for Bangla language applications.

Primary use cases include:

* Large Language Model (LLM) fine-tuning
* Mental health text classification
* Dialogue modeling for conversational AI
* Bangla NLP research and benchmarking

The dataset follows an instruction-based format (input–instruction–output), making it suitable for:

* Alpaca-style datasets
* Supervised Fine-Tuning (SFT)
* LoRA / QLoRA training
* Chat-style conversational fine-tuning

The dataset covers approximately 40 mental health-related conditions, including but not limited to:
মানসিক চাপ (stress), আত্মহত্যা (suicidal ideation), আত্মবিশ্বাস (self-confidence), ভালোবাসাহীনতা (lack of affection), অতিরিক্ত চিন্তা (overthinking), and related psychological states.

---

📚 Source Methodology
This dataset is fully synthetic and does not contain any real user data.

It was generated using structured and guided text generation techniques based on:

* Mental health literature and books
* Newspaper topics and psychological reports
* YouTube discussions and talk shows on mental health
* Articles, blogs, and clinical guidance materials

All samples were constructed through controlled transformations and generation pipelines to ensure diversity and relevance.

---

⚠️ Ethical Note

* This dataset does NOT contain real personal or sensitive data
* It is intended strictly for research and educational purposes
* It MUST NOT be used for clinical diagnosis or medical decision-making

---

📂 Dataset Formats

The dataset is provided in multiple formats for flexibility:

* JSONL → data/dataset.jsonl
  Best for LLM fine-tuning (Alpaca, SFT, QLoRA)

* CSV → data/dataset.csv
  Suitable for analysis and general-purpose use

* Parquet → data/dataset.parquet
  Efficient columnar storage for large-scale processing

* TOON → data/dataset.toon
  Token-optimized binary format for high-performance LLM training

---

📊 Dataset Size

* Total Samples: 10,000

---

⚖️ License
This dataset is released under:
Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)

Users are free to use, share, and adapt the dataset for non-commercial purposes with proper attribution.

---

📌 Citation
If you use this dataset, please cite:

Esfer Sami.
Bangla Mental Health Dataset V2.
Mendeley Data, 2026.
DOI: 

---

🔗 Related Resource
Hugging Face Dataset Repository:
https://huggingface.co/datasets/EsferSami/Bangla-Mental-Health-Dataset-V2

---

📩 Contact
For questions, collaborations, or clarifications, please contact the dataset author.

---
