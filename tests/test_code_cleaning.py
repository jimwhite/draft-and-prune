"""Tests for CodeCleaner and CodeExecutor._parse_pyke_sections."""
import pytest
from reasoners import CodeCleaner, CodeExecutor


# ── CodeCleaner._extract_fenced_block ──────────────────────────────────────

class TestExtractFencedBlock:
    def test_python_fence(self):
        text = "Explanation\n\n```python\nprint(42)\n```\nDone"
        assert CodeCleaner._extract_fenced_block(text, ("python",)) == "print(42)"

    def test_lang_hint_match_is_preferred(self):
        text = "```text\nignore\n```\n\n```python\nkeep\n```"
        assert CodeCleaner._extract_fenced_block(text, ("python",)) == "keep"

    def test_fallback_to_last_block(self):
        text = "```\nfirst\n```\n\n```\nsecond\n```"
        assert CodeCleaner._extract_fenced_block(text, ("python",)) == "second"

    def test_no_fences_returns_none(self):
        assert CodeCleaner._extract_fenced_block("plain text", ("python",)) is None

    def test_empty_hints_uses_last_block(self):
        text = "```rust\nfn main() {}\n```"
        assert CodeCleaner._extract_fenced_block(text, ()) == "fn main() {}"

    def test_multiline_content(self):
        text = "```python\nline1\nline2\nline3\n```"
        assert CodeCleaner._extract_fenced_block(text, ("python",)) == "line1\nline2\nline3"


# ── CodeCleaner.clean_code ─────────────────────────────────────────────────

class TestCleanCodeARLSAT:
    def test_python_fenced(self):
        text = "Here:\n\n```python\nfrom z3 import *\nprint(42)\n```\nDone"
        assert CodeCleaner.clean_code(text, "AR-LSAT") == "from z3 import *\nprint(42)"

    def test_no_fences_passthrough(self):
        text = "from z3 import *\nprint(42)"
        assert CodeCleaner.clean_code(text, "AR-LSAT") == text

    def test_prose_with_python_fence(self):
        text = "Let me solve this step by step.\n\n```python\nsolve()\n```\n\nThe answer is A."
        assert CodeCleaner.clean_code(text, "AR-LSAT") == "solve()"


class TestCleanCodeLogicalDeduction:
    def test_plain_fence(self):
        text = "```\nfrom constraint import *\n```"
        assert CodeCleaner.clean_code(text, "LogicalDeduction") == "from constraint import *"

    def test_python_fence(self):
        text = "```python\nfrom constraint import *\n```"
        assert CodeCleaner.clean_code(text, "LogicalDeduction") == "from constraint import *"


class TestCleanCodeProofWriter:
    def test_canonical_format_preserved(self):
        """When canonical ```facts/```rules/```query blocks exist, keep full text."""
        text = "```facts\nf()\n```\n```rules\nr()\n```\n```query\nq()\n```"
        assert CodeCleaner.clean_code(text, "ProofWriter") == text

    def test_pyke_fence_extracted(self):
        """Single ```pyke fence wrapping bare section labels → extract inner."""
        text = "Explanation text.\n\n```pyke\nfacts\nf1()\n\nrules\nr1()\n\nquery\nq1()\n```\nDone."
        cleaned = CodeCleaner.clean_code(text, "ProofWriter")
        assert "Explanation" not in cleaned
        assert "Done." not in cleaned
        assert cleaned.startswith("facts")

    def test_python_fence_extracted(self):
        """Single ```python fence → extract inner content."""
        text = "Here:\n\n```python\nfacts\nf()\nrules\nr()\nquery\nq()\n```"
        cleaned = CodeCleaner.clean_code(text, "ProofWriter")
        assert cleaned.startswith("facts")

    def test_no_fence_passthrough(self):
        """No fences at all → return as-is."""
        text = "facts\nf()\nrules\nr()\nquery\nq()"
        assert CodeCleaner.clean_code(text, "ProofWriter") == text


class TestCleanCodeProntoQA:
    def test_pyke_fence_extracted(self):
        text = "Sure!\n\n```pyke\nfacts\nis_a(\"Sam\", \"cat\", True)\n```"
        cleaned = CodeCleaner.clean_code(text, "ProntoQA")
        assert "Sure!" not in cleaned
        assert 'is_a("Sam"' in cleaned


class TestCleanCodeFOLIO:
    def test_prover9_fence(self):
        text = "Explanation\n\n```prover9\nall x (P(x)).\n```\nEnd"
        assert CodeCleaner.clean_code(text, "FOLIO").strip() == "all x (P(x))."

    def test_no_fence_warning(self, capsys):
        text = "just plain text"
        result = CodeCleaner.clean_code(text, "FOLIO")
        assert result == text
        assert "Warning" in capsys.readouterr().out


# ── CodeExecutor._parse_pyke_sections ──────────────────────────────────────

class TestParsePykeSections:
    def test_canonical_fenced_format(self):
        text = "```facts\nfact1\nfact2\n```\n```rules\nrule1\n```\n```query\nq1\n```"
        facts, rules, query = CodeExecutor._parse_pyke_sections(text)
        assert "fact1" in facts
        assert "rule1" in rules
        assert "q1" in query

    def test_bare_labels_no_colon(self):
        """Section headers without colons (common LLM variant)."""
        text = "facts\nfact1\n\nrules\nrule1\n\nquery\nq1\n"
        facts, rules, query = CodeExecutor._parse_pyke_sections(text)
        assert "fact1" in facts
        assert "rule1" in rules
        assert "q1" in query

    def test_labels_with_colon(self):
        """Section headers with colons."""
        text = "Facts:\nfact1\n\nRules:\nrule1\n\nQuery:\nq1\n"
        facts, rules, query = CodeExecutor._parse_pyke_sections(text)
        assert "fact1" in facts
        assert "rule1" in rules
        assert "q1" in query

    def test_markdown_heading_labels(self):
        """Section headers with markdown #."""
        text = "# Facts:\nfact1\n\n## Rules:\nrule1\n\n### Query:\nq1\n"
        facts, rules, query = CodeExecutor._parse_pyke_sections(text)
        assert "fact1" in facts
        assert "rule1" in rules

    def test_wrapped_in_pyke_fence_bare_labels(self):
        """Content from inside a ```pyke fence, bare labels."""
        text = "facts\nis_cold(\"Bob\", True)\n\nrules\nrule1\n    foreach\n        facts.is_cold($x, True)\n    assert\n        facts.is_warm($x, True)\n\nquery\nfacts.is_warm(\"Bob\", True)\n"
        facts, rules, query = CodeExecutor._parse_pyke_sections(text)
        assert 'is_cold("Bob", True)' in facts
        assert "rule1" in rules
        assert 'is_warm("Bob", True)' in query

    def test_missing_sections_raises(self):
        with pytest.raises(ValueError, match="facts.*rules.*query"):
            CodeExecutor._parse_pyke_sections("nothing useful here")

    def test_partial_missing_raises(self):
        with pytest.raises(ValueError, match="query"):
            CodeExecutor._parse_pyke_sections("```facts\nf\n```\n```rules\nr\n```")

    def test_full_markdown_response_with_pyke_fence(self):
        """Simulate real LLM output: explanation + ```pyke fence with bare labels."""
        text = (
            "Looking at the problem, I need to fix the syntax.\n\n"
            "Here is the corrected code:\n\n"
            "```pyke\n"
            "facts\n"
            'is_kind("Charlie", True)\n'
            "\n"
            "rules\n"
            "rule1\n"
            "    foreach\n"
            '        facts.is_kind($x, True)\n'
            "    assert\n"
            '        facts.is_nice($x, True)\n'
            "\n"
            "query\n"
            'facts.is_nice("Charlie", True)\n'
            "```\n"
            "\nThis should work."
        )
        # After CodeCleaner strips the fence, parse should work
        cleaned = CodeCleaner.clean_code(text, "ProofWriter")
        facts, rules, query = CodeExecutor._parse_pyke_sections(cleaned)
        assert 'is_kind("Charlie", True)' in facts
        assert "rule1" in rules
        assert 'is_nice("Charlie", True)' in query
