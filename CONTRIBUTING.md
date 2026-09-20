# Contributing to AiExponent

Thank you for your interest in contributing to AiExponent! We build open-source, deterministic compliance engineering tools for the EU AI Act, NIST AI RMF, and ISO/IEC 42001.

All AiExponent tools are distributed under the **Apache License 2.0**. We welcome contributions from software engineers, compliance officers, AI researchers, and legal technologists.

---

## ⚡ 10-Minute Low-Code Contribution Tracks

AI compliance requires legal precision and domain knowledge, not just code. You can make an immediate, high-impact contribution **without writing a single line of Python** by editing straightforward YAML and JSON configuration files:

| Track | Target Repository | What You Contribute | How to Contribute (< 10 Mins) |
| :--- | :--- | :--- | :--- |
| **Risk Question Bank** | [`riskforge`](https://github.com/aiexponent/riskforge) | Risk assessment questions, Annex III criteria, ISO 42001 mappings | Edit or add questions in [`src/riskforge/_data/question_bank/`](https://github.com/aiexponent/riskforge/tree/main/src/riskforge/_data/question_bank) (e.g., `discrimination.yaml`, `human_oversight.yaml`). |
| **License Policies** | [`license-compliance-checker`](https://github.com/aiexponent/license-compliance-checker) | Regulatory license profiles, RAIL restrictions, model licenses | Add or tune policy rules in [`policy/templates/`](https://github.com/aiexponent/license-compliance-checker/tree/main/policy/templates) (e.g., `eu_ai_act.yaml`, `ai_research.yaml`). |
| **RAG Golden Datasets** | [`rag-benchmarking`](https://github.com/aiexponent/rag-benchmarking) | Domain-specific Q&A evaluation pairs, retrieval ground-truth | Add realistic question-context-answer JSONL entries to [`data/golden/qa.jsonl`](https://github.com/aiexponent/rag-benchmarking/blob/main/data/golden/qa.jsonl). |
| **Prohibited Practice Cases** | [`litmusai`](https://github.com/aiexponent/litmusai) | Article 5 screening edge cases and test portfolios | Add test scenarios to [`tests/fixtures/portfolio/`](https://github.com/aiexponent/litmusai/tree/main/tests/fixtures/portfolio) (e.g., social scoring, vulnerability exploitation). |

---

## 🏷️ Looking for Your First Issue?

We curate beginner-friendly tasks across all repositories labeled **`good first issue`**:

👉 **[Browse Good First Issues Across AiExponent](https://github.com/search?q=org%3Aaiexponent+is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)**

---

## 🛠️ Development & PR Workflow

For code enhancements, bug fixes, or performance optimizations:

### 1. Fork & Branch
```bash
# Clone your fork
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# Create a focused feature branch
git checkout -b feat/add-iso-control-mapping
```

### 2. Commit Message Standards
We follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` new feature, CLI flag, or policy capability
- `fix:` bug fix or regulatory citation correction
- `docs:` documentation or README enhancements
- `test:` test cases, fixtures, or synthetic evaluation datasets
- `chore:` dependency updates, packaging, or CI maintenance

### 3. Verification & Testing
Before opening a pull request, run the repository's automated test suite:
```bash
# Python repositories (pytest)
pytest -v

# Code formatting & style
ruff check .
ruff format --check .
```

### 4. Open a Pull Request
1. Push your branch to your fork: `git push -u origin feat/your-feature`
2. Open a Pull Request against `main` in the target `aiexponent` repository.
3. Fill in the PR template detailing your changes, regulatory rationale, and testing evidence.

---

## 🤝 Community & Support

- **Discussions & Q&A**: Join our asynchronous developer discussions at **[litmusai/discussions](https://github.com/aiexponent/litmusai/discussions)**.
- **Code of Conduct**: All participants are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).
- **Security Inquiries**: For confidential vulnerability disclosures, follow [SECURITY.md](SECURITY.md) and contact [security@aiexponent.com](mailto:security@aiexponent.com).
- **General Inquiries**: [hello@aiexponent.com](mailto:hello@aiexponent.com).
