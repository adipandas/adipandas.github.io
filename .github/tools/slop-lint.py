#!/usr/bin/env python3
"""
slop_lint.py - deterministic check for AI slop in prose.

Slop, after Silbey and Hartzog: output produced with little exertion that
shifts the work onto the reader and degrades the domain. Most of that is
unmachine-checkable. What this script checks is the residue: LLM cadence tics,
padding, self-restatement, and citations with nothing behind them.

Instruction files are advisory; a model can drift past them in a long context.
This is the part that actually binds.

Usage:
    python tools/slop_lint.py FILE [FILE ...]
    python tools/slop_lint.py --strict docs/          # warnings fail too
    python tools/slop_lint.py --list-rules

Exit codes:
    0  clean
    1  at least one ERROR (or, with --strict, at least one WARN)
    2  bad invocation

Masking: fenced code blocks, indented code blocks, inline code spans, YAML
frontmatter, link targets, and HTML comments are blanked before matching, so
code and quoted material never trip a rule.

Suppression: put `<!-- slop-lint-disable-line -->` at the end of a line, or
`<!-- slop-lint-disable-file -->` anywhere in the file. Suppressions are
reported at the end so they cannot be used silently.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PROSE_SUFFIXES = {".md", ".mdx", ".rst", ".txt", ".adoc"}

# --------------------------------------------------------------------------
# Rules
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Rule:
    rid: str
    level: str  # "error" | "warn"
    pattern: re.Pattern
    message: str


def _rx(p: str) -> re.Pattern:
    return re.compile(p, re.IGNORECASE)


RULES: list[Rule] = [
    # --- structural: these are errors -------------------------------------
    Rule(
        "S001", "error",
        _rx(r"\b(it|that|this|the \w+)\s*(?:'s|s| is| was)?\s*(?:is|was)?\s*n[o']t\s+"
            r"[^.!?;—]{1,70}[.;—]\s*(?:it|that|this)\s*(?:'s| is)"),
        "negate-then-reattribute ('It's not X. It's Y.') - state the positive claim once",
    ),
    Rule(
        "S001b", "error",
        _rx(r"\b(nothing|no\s+\w+|none of (this|that|it))\s+[^.!?]{1,70}[.!?]\s+"
            r"(the|that)\s+\w+\s+(belongs to|lies (in|with)|is (in|with|the)|comes from)\b"),
        "negate-then-reattribute across two sentences - state the positive claim once",
    ),
    Rule(
        "S001c", "error",
        _rx(r"\b(?:nothing|neither|no\s+(?!longer|more|less|doubt|matter)\w+)\s+"
            r"[^.!?]{0,60},\s+(?:and|but)\s+(?:it|that|this|they)\s+\w+"),
        "negate-then-reattribute inside one sentence - drop the negated half",
    ),
    Rule(
        "S002", "error",
        _rx(r"\bnot\s+(just|only|merely|simply)\b[^.!?]{1,90}\bbut\b"),
        "'not just X, but Y' - say what it is",
    ),
    Rule(
        "S003", "error",
        _rx(r"\b(here'?s the (kicker|catch|thing|rub|twist|punchline)"
            r"|but here'?s (the|where|why)"
            r"|the (real|really |most )?(interesting|instructive|surprising|important|telling)"
            r"\s+(part|thing|bit|story|question|detail)"
            r"|and that'?s (where|when) it gets"
            r"|what'?s (really )?going on here"
            r"|therein lies)\b"),
        "suspense/reveal framing - put the finding in the first clause",
    ),
    Rule(
        "S004", "error",
        _rx(r"\b(comes? down to|boils? down to|at bottom,|the thing to (carry away|remember)"
            r"|the (key |main )?takeaway (here )?is|it all reduces to|reduces? to one"
            r"|out of (just )?one (fact|idea|observation)|the whole (thing|story) is)\b"),
        "reduction closer - a summary is a summary, do not frame it as a distilled insight",
    ),
    Rule(
        "S004b", "error",
        _rx(r"\bthat is (?:the|what|why|how)\b[^.!?]{0,70},\s+"
            r"and (?:it|that) is (?:why|what|how|the reason)\b"),
        "explanatory closer - the derivation already showed this, do not narrate it back",
    ),
    Rule(
        "S005", "error",
        _rx(r",\s+(none|all|each|both|neither|any)\s+of\s+which\s+[^.!?]{1,50}[.!?]\s*$"),
        "trailing punchy clause - a comma is not a drumroll",
    ),
    Rule(
        "S005b", "error",
        _rx(r",\s+(?:without\s+\w+ing\s+any"
            r"|and\s+(?:the\s+)?\w+\s+is\s+easy\s+to\s+(?:miss|overlook|spot|get\s+wrong)"
            r"|though\s+not\s+\w+"
            r"|which\s+is\s+\w+\s+enough"
            r"|and\s+that\s+is\s+(?:why|what|one\s+reason)"
            r")\b[^.!?]{0,60}[.!?]\s*$"),
        "trailing emphasis clause - state the consequence or delete the clause",
    ),
    Rule(
        "S006", "error",
        _rx(r"\b(load[- ]bearing (assumption|claim|idea|piece|part)"
            r"|the connective tissue|the beating heart|the secret sauce"
            r"|the (real )?magic (here )?is|a masterclass in|the north star)\b"),
        "metaphor promoted to a noun phrase - name the actual thing",
    ),
    Rule(
        "S007", "error",
        _rx(r"\b(i(?:'ve| have) (lost|spent|burned) more (time|hours|days)"
            r"|i can'?t count how many times"
            r"|i(?:'ve| have) seen this (go wrong|fail) more times)\b"),
        "anecdote used as authority - state the claim, cite or measure it",
    ),
    Rule(
        "S007b", "error",
        _rx(r"\b(?:the one|the first thing|what)\s+i(?:'d| would)\s+"
            r"(?:worry about|reach for|start with|check|look at|do|pick)\b"),
        "personal preference used as evidence - give the reason that makes it true",
    ),
    Rule(
        "S008", "error",
        _rx(r"\b(you'?ll never (look at|think about) \w+ the same"
            r"|this (will )?change[sd]? (how|everything|the (whole )?game)"
            r"|and that changes everything"
            r"|welcome to the (world|era) of)\b"),
        "second-person hype",
    ),
    Rule(
        "S009", "error",
        _rx(r"\b(think of (it|this) as|imagine (for a moment|if)|picture this)\b"),
        "invited-analogy opener - give the analogy directly or drop it",
    ),
    Rule(
        "S013", "error",
        _rx(r"\b(in (the|a) (world|realm|age|era) of"
            r"|in today'?s fast[- ]paced"
            r"|let'?s (dive|jump) (in|into)"
            r"|buckle up"
            r"|without further ado"
            r"|in this (post|article|guide),? (we'?ll|we will|i'?ll|you'?ll)"
            r"|by the end of this (post|article|guide)"
            r"|as we all know"
            r"|at the end of the day)\b"),
        "formulaic opener or segue - open with the claim",
    ),
    Rule(
        "S014", "error",
        _rx(r"\b(great question"
            r"|you'?re absolutely right"
            r"|i hope this helps"
            r"|happy (coding|hacking|learning)"
            r"|let me know if you (have any|need)"
            r"|feel free to (reach out|ask|explore)"
            r"|as an ai (language )?model)\b"),
        "assistant register - a post is not a chat reply",
    ),
    Rule(
        "S015", "error",
        _rx(r"\b(?:it is|it'?s)\s+(?:widely|generally|commonly|well)[- ]?"
            r"(?:known|believed|accepted|understood|agreed)\b"
            r"|\b(?:experts|researchers|scientists|practitioners)\s+(?:broadly\s+)?agree\b"
            r"|\b(?:studies|research|papers|the literature)\s+(?:have\s+|has\s+)?"
            r"(?:shown|show|shows|suggest|suggests|indicate|indicates)\b"
            r"|\bit goes without saying\b"
            r"|\bas (?:is )?well[- ]known\b"),
        "hedge presented as fact - name the source and link it, or claim it in your own voice",
    ),
    # --- vocabulary: warnings ---------------------------------------------
    Rule(
        "W001", "warn",
        _rx(r"\b(genuinely|truly|incredibly|remarkably|fundamentally|essentially"
            r"|arguably|simply put|needless to say|it'?s worth noting"
            r"|importantly|notably|of course,)\b"),
        "filler intensifier or hedge - delete it and check nothing was lost",
    ),
    Rule(
        "W002", "warn",
        _rx(r"\b(delve|tapestry|testament to|the realm of|the landscape of"
            r"|navigating the|leverage[ds]?\s+(?!ratio|point)|seamless(ly)?"
            r"|game[- ]?chang(er|ing)|paradigm shift|deep dive|cutting[- ]edge"
            r"|ever[- ]evolving|transformative|supercharge|turbocharge"
            r"|harness(ing)? the power|unlock(s|ing)? the|elevate your"
            r"|see(?:ing)? the light of day"
            r"|in today'?s (world|landscape))\b"),
        "register marker - use the precise technical term instead",
    ),
    Rule(
        "W003", "warn",
        _rx(r"\b(crucial|pivotal|vital|robust|powerful|elegant|beautiful)\b"),
        "evaluative filler - keep only if it is the precise technical term",
    ),
    Rule(
        "W004", "warn",
        _rx(r"^\s*(And|But|Which|Because|So|Yet)\b[^.!?]{0,45}[.!?]\s*$"),
        "sentence fragment used for cadence",
    ),
    Rule(
        "W005", "warn",
        _rx(r"\b(?:tens|hundreds|thousands)\s+of\s+(?:milli|micro|nano)?seconds\b"
            r"|\ban order of magnitude\b"
            r"|\b(?:most|many|nearly all)\s+"
            r"(?:airframes|implementations|firmware|libraries|practitioners)\b"
            r"|\byou (?:see|find) in real (?:firmware|code|systems|hardware)\b"),
        "unsourced empirical claim - measure it, cite it, or mark it as your expectation",
    ),
    Rule(
        "W006", "warn",
        _rx(r"(?:^|[.!?]\s+)(?:this|that|it)\s+(?:can be|is|gets)\s+"
            r"(?:confusing|tricky|subtle|counter-?intuitive|easy to get wrong)\s*\."),
        "evaluative sentence with no content - say what is confusing and why",
    ),
    Rule(
        "W007", "warn",
        _rx(r"\b(?:it is|it'?s) important to (?:note|remember|understand|realize)\b"
            r"|\bit should be noted\b"
            r"|\bdue to the fact that\b"
            r"|\bas (?:mentioned|noted|discussed) (?:earlier|above|previously)\b"
            r"|\bone of the most important (?:things|aspects|parts)\b"
            r"|\bwhen it comes to\b"),
        "padding - delete the phrase and keep the claim",
    ),
    Rule(
        "W008", "warn",
        _rx(r"\bthere is no (?:one[- ]size[- ]fits[- ]all|silver bullet|single (?:right )?answer)\b"
            r"|\byour mileage may vary\b"
            r"|\b(?:it|that) (?:really )?depends on (?:your|the) (?:use case|needs|situation)\b"
            r"|\bboth (?:approaches|methods|options) have\b"
            r"|\bpros and cons\b"),
        "non-answer - give the condition that decides it",
    ),
]


# --------------------------------------------------------------------------
# Masking
# --------------------------------------------------------------------------

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
DISPLAY_MATH = re.compile(r"\$\$.*?\$\$", re.DOTALL)
MATH = re.compile(r"\$[^$]*\$|\\\[.*?\\\]|\\\(.*?\\\)", re.DOTALL)


def _blank(m: re.Match) -> str:
    """Blank a span but keep its newlines, so line numbers do not shift."""
    return re.sub(r"[^\n]", " ", m.group(0))


def mask_lines(text: str) -> list[str]:
    """Blank out everything a rule must not see, preserving line numbering."""
    text = HTML_COMMENT.sub(_blank, text)
    text = DISPLAY_MATH.sub(_blank, text)
    text = MATH.sub(_blank, text)

    lines = text.split("\n")
    out: list[str] = []
    in_fence = False
    in_frontmatter = False

    for i, line in enumerate(lines):
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            out.append("")
            continue
        if in_frontmatter:
            if line.strip() in ("---", "..."):
                in_frontmatter = False
            out.append("")
            continue
        if FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence or line.startswith("    ") or line.startswith("\t"):
            out.append("")
            continue
        masked = INLINE_CODE.sub(lambda m: " " * len(m.group(0)), line)
        masked = LINK_TARGET.sub(lambda m: " " * len(m.group(0)), masked)
        out.append(masked)

    return out


# --------------------------------------------------------------------------
# Cadence and punctuation checks
# --------------------------------------------------------------------------

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
EM_DASH_PER_1000 = 2.0
SHORT_RUN_LEN = 4
SHORT_MAX_WORDS = 8
PARA_CLOSE_MAX_WORDS = 8
PARA_CLOSE_MIN_MEAN = 15.0

# The tic restates something already said, so it opens by pointing back at it.
# Requiring that opener is what keeps sign-offs, imperatives and cross-checks out.
PARA_CLOSE_OPENER = re.compile(r"^(This|That|These|Those|The|It)\b")


def check_cadence(masked: list[str]) -> list[tuple[int, str, str, str]]:
    """Flag runs of very short sentences used for rhythm.

    Operates on blank-line-separated paragraphs, not raw lines: prose is
    hard-wrapped, and splitting per line turns one long sentence into several
    apparent short ones.
    """
    findings = []
    for start, _end, para in iter_paragraphs(masked):
        if re.match(r"^(#|>|[-*+]\s|\d+\.\s|\|)", para.strip()):
            continue
        run = 0
        for sent in SENT_SPLIT.split(para):
            words = len(sent.split())
            if 0 < words <= SHORT_MAX_WORDS:
                run += 1
                if run == SHORT_RUN_LEN:
                    findings.append((
                        start, "S010", "warn",
                        f"{SHORT_RUN_LEN} consecutive sentences of <= "
                        f"{SHORT_MAX_WORDS} words - cadence drumbeat",
                    ))
            else:
                run = 0
    return findings


def check_paragraph_close(masked: list[str]) -> list[tuple[int, str, str, str]]:
    """Flag a curt sentence appended to the end of a paragraph of long ones.

    The tic lands a beat rather than a fact. A short closer after equally short
    sentences is ordinary prose, so the preceding sentences have to average well
    above the closer before this fires, and the closer has to point backwards.
    """
    findings = []
    for start, _end, para in iter_paragraphs(masked):
        if re.match(r"^(#|>|[-*+]\s|\d+\.\s|\|)", para.strip()):
            continue
        sents = [s for s in SENT_SPLIT.split(para) if s.split()]
        if len(sents) < 3:
            continue
        closer = sents[-1].strip()
        if closer.endswith(":"):  # a lead-in to a display equation or list
            continue
        if not PARA_CLOSE_OPENER.match(closer):
            continue
        last = len(closer.split())
        head = [len(s.split()) for s in sents[:-1]]
        mean_head = sum(head) / len(head)
        if last <= PARA_CLOSE_MAX_WORDS and mean_head >= PARA_CLOSE_MIN_MEAN:
            findings.append((
                start, "S012", "warn",
                f"paragraph ends on a {last}-word sentence after a mean of "
                f"{mean_head:.0f} - fold it into the sentence before, or cut it",
            ))
    return findings


def check_em_dashes(masked: list[str]) -> list[tuple[int, str, str, str]]:
    body = "\n".join(masked)
    words = len(body.split())
    dashes = body.count("\u2014")
    if words < 150:
        return []
    rate = dashes * 1000.0 / words
    if rate > EM_DASH_PER_1000:
        return [(
            1, "S011", "error",
            f"{dashes} em dashes in {words} words ({rate:.1f}/1000, "
            f"ceiling {EM_DASH_PER_1000}) - use a colon, comma, or period",
        )]
    return []


# --------------------------------------------------------------------------
# Slop checks: repetition, list padding, unverifiable citations
# --------------------------------------------------------------------------

DUP_MIN_WORDS = 12
DUP_JACCARD = 0.85
WORD = re.compile(r"[a-z0-9]+")


def check_repetition(masked: list[str]) -> list[tuple[int, str, str, str]]:
    """Flag a sentence that restates an earlier one with the nouns swapped.

    Only compares across paragraphs: parallel construction inside a paragraph
    ("the x component ... the y component ...") is ordinary technical prose.
    """
    seen: list[tuple[int, int, set[str]]] = []  # (para_index, lineno, tokens)
    findings = []
    for para_index, (start, _end, para) in enumerate(iter_paragraphs(masked)):
        if re.match(r"^(#|>|\|)", para.strip()):
            continue
        for sent in SENT_SPLIT.split(para):
            toks = WORD.findall(sent.lower())
            if len(toks) < DUP_MIN_WORDS:
                continue
            tset = set(toks)
            for prev_para, prev_line, prev in seen:
                if prev_para == para_index:
                    continue
                union = len(tset | prev)
                if union and len(tset & prev) / union >= DUP_JACCARD:
                    findings.append((
                        start, "S020", "warn",
                        f"restates the sentence at line {prev_line} - say it once",
                    ))
                    break
            seen.append((para_index, start, tset))
    return findings


BULLET_LABEL = re.compile(r"^\s*[-*+]\s+\*\*[^*]+\*\*\s*[:.\u2014-]")
BULLET_RUN_LEN = 3


def check_bullet_labels(masked: list[str]) -> list[tuple[int, str, str, str]]:
    """Flag a run of bullets that are each a bolded label plus one sentence."""
    findings = []
    run, run_start = 0, 0
    for lineno, line in enumerate(masked, 1):
        if BULLET_LABEL.match(line):
            run += 1
            if run == 1:
                run_start = lineno
            if run == BULLET_RUN_LEN:
                findings.append((
                    run_start, "S021", "warn",
                    f"{BULLET_RUN_LEN} consecutive bolded-label bullets - write "
                    "paragraphs if the items carry content, otherwise cut the list",
                ))
        elif line.strip():
            run = 0
    return findings


CITATION_SHAPED = re.compile(
    r"\b[A-Z][\w'\u2019-]+\s+et al\.?,?\s*\(?(?:19|20)\d{2}"
    r"|\baccording to (?:a|the|one|recent)\s+"
    r"(?:recent\s+)?(?:study|paper|report|survey|analysis|review)"
    r"|\b(?:shown|demonstrated|reported|proven)\s+in\s+\[\d{1,3}\]"
)
EVIDENCE = re.compile(r"\]\(|https?://|doi\.org|arxiv|\[\^|<a\s+href", re.IGNORECASE)


def check_citations(raw_lines: list[str],
                    masked: list[str]) -> list[tuple[int, str, str, str]]:
    """Flag citation-shaped text with no link, DOI, or footnote behind it.

    A reference the reader cannot follow is indistinguishable from one the
    model invented, which is the failure mode this file exists to prevent.
    """
    findings = []
    for start, end, para in iter_paragraphs(masked):
        m = CITATION_SHAPED.search(para)
        if not m:
            continue
        raw = "\n".join(raw_lines[start - 1:end])
        if EVIDENCE.search(raw):
            continue
        snippet = " ".join(m.group(0).split())
        findings.append((
            start, "S022", "error",
            f"citation with nothing behind it - link it or drop it  [{snippet!r}]",
        ))
    return findings


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

# Require the full HTML-comment form, so a document that merely *mentions* the
# token (like this one) is not accidentally exempted.
DISABLE_LINE = re.compile(r"<!--[^>]*slop-lint-disable-line[^>]*-->")
DISABLE_FILE = re.compile(r"<!--[^>]*slop-lint-disable-file[^>]*-->")


def strip_code_spans(text: str) -> str:
    """Remove fenced blocks and inline code so a doc that *documents* the
    suppression markers is not accidentally suppressed by them."""
    text = re.sub(r"^\s*(```|~~~).*?^\s*(```|~~~)", "", text, flags=re.S | re.M)
    return INLINE_CODE.sub(" ", text)


def iter_paragraphs(masked: list[str]):
    """Yield (start_lineno, end_lineno, joined_text) per blank-line-separated block."""
    buf: list[str] = []
    start = end = 0
    for lineno, line in enumerate(masked, 1):
        if line.strip():
            if not buf:
                start = lineno
            end = lineno
            buf.append(line.strip())
        elif buf:
            yield start, end, " ".join(buf)
            buf = []
    if buf:
        yield start, end, " ".join(buf)


def lint_file(path: Path) -> tuple[list[str], int, int, int]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if DISABLE_FILE.search(strip_code_spans(raw)):
        return ([f"{path}: skipped via slop-lint-disable-file"], 0, 0, 1)

    raw_lines = raw.split("\n")
    masked = mask_lines(raw)

    found: list[tuple[int, str, str, str]] = []
    seen: set[tuple[int, str]] = set()

    def record(lineno: int, rule: Rule, m: re.Match) -> None:
        key = (lineno, rule.rid)
        if key in seen:
            return
        seen.add(key)
        snippet = " ".join(m.group(0).split())
        found.append((lineno, rule.rid, rule.level, f"{rule.message}  [{snippet!r}]"))

    # Per-line pass.
    for lineno, line in enumerate(masked, 1):
        if not line.strip():
            continue
        for rule in RULES:
            m = rule.pattern.search(line)
            if m:
                record(lineno, rule, m)

    # Paragraph pass: prose is usually hard-wrapped, so constructions that span
    # a line break are invisible to the per-line pass above.
    for start, _end, para in iter_paragraphs(masked):
        for rule in RULES:
            if rule.rid.startswith("W"):
                continue  # word-level rules gain nothing from joining
            m = rule.pattern.search(para)
            if m:
                record(start, rule, m)

    found.extend(check_cadence(masked))
    found.extend(check_paragraph_close(masked))
    found.extend(check_em_dashes(masked))
    found.extend(check_repetition(masked))
    found.extend(check_bullet_labels(masked))
    found.extend(check_citations(raw_lines, masked))

    report, errors, warns, suppressed = [], 0, 0, 0
    for lineno, rid, level, msg in sorted(found):
        if DISABLE_LINE.search(strip_code_spans(raw_lines[lineno - 1])):
            suppressed += 1
            continue
        report.append(f"{path}:{lineno}: {level.upper()} {rid}: {msg}")
        if level == "error":
            errors += 1
        else:
            warns += 1
    return report, errors, warns, suppressed


def collect(targets: list[str]) -> list[Path]:
    paths: list[Path] = []
    for t in targets:
        p = Path(t)
        if p.is_dir():
            paths += [q for q in sorted(p.rglob("*")) if q.suffix.lower() in PROSE_SUFFIXES]
        elif p.is_file():
            paths.append(p)
        else:
            print(f"slop_lint: no such path: {t}", file=sys.stderr)
    return paths


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic prose slop linter.")
    ap.add_argument("targets", nargs="*", help="files or directories")
    ap.add_argument("--strict", action="store_true", help="warnings fail too")
    ap.add_argument("--list-rules", action="store_true")
    args = ap.parse_args()

    if args.list_rules:
        for r in RULES:
            print(f"{r.rid}  {r.level:<5}  {r.message}")
        print(f"S010  warn   cadence drumbeat ({SHORT_RUN_LEN} consecutive short sentences)")
        print("S011  error  em dash rate above ceiling")
        print(f"S012  warn   paragraph closed by a backward-pointing sentence of <= "
              f"{PARA_CLOSE_MAX_WORDS} words after long ones")
        print("S020  warn   sentence restates an earlier one in another paragraph")
        print(f"S021  warn   {BULLET_RUN_LEN} consecutive bolded-label bullets")
        print("S022  error  citation-shaped text with no link, DOI, or footnote")
        return 0

    if not args.targets:
        ap.print_usage(sys.stderr)
        return 2

    total_e = total_w = total_s = 0
    for path in collect(args.targets):
        report, e, w, s = lint_file(path)
        for line in report:
            print(line)
        total_e += e
        total_w += w
        total_s += s

    print(f"\nslop_lint: {total_e} error(s), {total_w} warning(s), {total_s} suppressed")
    if total_s:
        print("slop_lint: suppressions were used - review them before merging")

    if total_e or (args.strict and total_w):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
