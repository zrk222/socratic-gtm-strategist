# Contributing to Socratic GTM Strategist

Thank you for your interest in contributing to **Socratic GTM Strategist**!

We welcome contributions of all kinds: bug fixes, documentation improvements, new adversarial stress-testing personas, GTM vector refinements, and integrations with new agentic IDEs.

---

## 🛠️ Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zrk222/socratic-gtm-strategist.git
   cd socratic-gtm-strategist
   ```

2. **Set up Python environment (3.9+):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. **Run the test suite:**
   ```bash
   python -m unittest discover tests
   ```

---

## 🧪 Testing Guidelines

- Always run `python -m unittest discover tests` before opening a pull request.
- If you add or modify a tool or script in `scripts/`:
  - Ensure informational logs are written to `sys.stderr` so that the JSON-RPC stdio transport on `sys.stdout` remains pure.
  - Add corresponding unit tests to `tests/test_socratic_gtm.py`.

---

## 📦 Pull Request Process

1. Create a feature branch (`git checkout -b feature/my-enhancement`).
2. Follow standard conventional commits (e.g., `feat:`, `fix:`, `docs:`, `test:`).
3. Ensure all tests pass in local and GitHub Actions CI.
4. Submit your pull request against the `main` branch.

---

## 📄 License
By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](./LICENSE).
