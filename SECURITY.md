# Security Policy

AiExponent is committed to ensuring the security, integrity, and regulatory robustness of our open-source AI compliance tooling suite.

---

## Supported Versions

We actively maintain and provide security patches for the latest release branch of each organization tool:

| Repository / Tool | Package / Artifact | Supported Version | Status |
| :--- | :--- | :--- | :--- |
| [`litmusai`](https://github.com/aiexponent/litmusai) | `litmus-screener` (PyPI) | `v1.0.x` | ✅ Active Security Support |
| [`license-compliance-checker`](https://github.com/aiexponent/license-compliance-checker) | `license-compliance-checker` (PyPI) | `v2.0.x` | ✅ Active Security Support |
| [`rag-benchmarking`](https://github.com/aiexponent/rag-benchmarking) | `rag-benchmarking` (PyPI) | `v1.0.x` | ✅ Active Security Support |
| [`riskforge`](https://github.com/aiexponent/riskforge) | `riskforge` (PyPI) | `v1.1.x` | ✅ Active Security Support |
| [`agentic-document-analyser`](https://github.com/aiexponent/agentic-document-analyser) | Container / Microservices | `latest` (`main`) | ✅ Active Security Support |

---

## Reporting a Vulnerability

**Please do NOT open public GitHub issues or discussions for security vulnerabilities.**

If you discover a potential security flaw, vulnerability, or sensitive data leakage, report it privately to our security engineering team:

📧 **Email:** [security@aiexponent.com](mailto:security@aiexponent.com)

### What to Include
To help us triage and resolve the issue quickly, please provide:
1. **Tool & Version**: The affected tool name, repository, and version/commit hash.
2. **Vulnerability Type**: e.g., prompt injection, SSRF, dependency vulnerability, command injection, path traversal.
3. **Reproduction Steps**: Step-by-step instructions or minimal proof-of-concept (PoC) code.
4. **Impact Assessment**: Description of potential attack vectors, exploitability, and affected data/systems.
5. **Remediation Suggestion**: If you have identified a potential patch or mitigation.

### Response Timelines & SLA
- **Initial Acknowledgment**: Within **48 hours**.
- **Triage & Preliminary Assessment**: Within **5 business days**.
- **Coordinated Disclosure**: We aim to release security patches within 30 days of triage confirmation.

---

## Safe Harbor & Coordinated Disclosure

We believe in responsible, coordinated vulnerability disclosure. If you make a good faith effort to comply with this policy during your security research:
- We will not pursue legal action against you.
- We ask that you give us reasonable time to patch the issue before public disclosure.
- Do not exploit the vulnerability beyond what is necessary to demonstrate it.
- Do not access, modify, or destroy any other user's or customer's data.

### Researcher Credit
Unless you prefer to remain anonymous, we will gladly acknowledge and credit your contribution in the corresponding GitHub Security Advisory and release notes.
