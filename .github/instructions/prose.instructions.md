---
name: 'No-slop prose'
description: 'Plain-English rules for text a human will read: prose files, README, docstrings, code comments, commit messages.'
applyTo: '**'
---

# Prose rules

Applies to any text a reader sees: Markdown, README, docstrings, code comments,
commit messages. Not to chat replies.

Write declaratively. Claim first, then evidence. One idea per sentence. Never
write a sentence whose job is rhythm, suspense, or emphasis rather than
information.

Test each sentence: delete it. If no fact was lost, it was decoration.

## What slop is

Silbey and Hartzog define AI slop as the output of a generative probabilistic
system produced with little exertion, which asymmetrically burdens its
recipients and degrades the domain it lands in ("AI Slop", 2026 draft, Boston
University School of Law). The three parts are separate tests. A blog post is
slop if it fails any one of them.

**Negligible exertion.** The text was produced without the choices that writing
normally requires: structure, tone, diction, what to leave out. First output,
shared unrevised. A draft you did not reread is slop regardless of how it
scores on every rule below.

**Asymmetrical imposition.** The text moves work from the writer to the reader.
Shaib et al. call the axis Information Utility. A reader who has to reread a
paragraph to find its point, fill in a gap you left, or check a claim you did
not source is paying for effort you declined to spend. If you could not be
bothered to write it, do not expect anyone to read it.

**Domain degradation.** Silbey and Hartzog name three mechanisms. Slop crowds
out human work by being cheap to produce. It cheapens effort by making the
signals of care (a worked example, a measured number, a real citation)
unreliable. It introduces errors: fabricated references, misattributed quotes,
plausible but false claims. Madsen and Puyt call this last one the Verification
dimension. It is the one a technical blog post fails most often.

## What you owe the reader

These are obligations, not style preferences. The linter cannot check most of
them.

1. Verify every citation. Open the paper. A reference that you did not open is
   a fabricated reference until proven otherwise. Link it, or delete it.
2. Run every number. State how it was measured, on what hardware, over how many
   trials. An unmeasured quantity is an expectation, and must be labelled as
   one.
3. Run every code block you publish. Untested code is slopware.
4. Own the claims. If you cannot defend a sentence when questioned, it is not
   yours and it does not belong in the post.
5. Revise. The first draft is the input to the work, not the output.
6. Disclose substantive AI assistance in the post, naming what the model did
   (drafting, editing, code, literature search).

## Banned

1. Negate-then-reattribute: "It's not X. It's Y." / "A isn't the problem, B is."
2. "not just X, but Y"
3. Reveal framing: "here's the kicker", "but there's a catch", "the most
   instructive part", "and that's where it gets interesting"
4. Reduction closers: "it all comes down to", "at bottom", "the thing to carry
   away"
5. A short punchy sentence appended to end a paragraph on a beat
6. A trailing punchy clause after a comma for emphasis
7. Metaphor as a noun phrase: "the load-bearing assumption", "the connective
   tissue", "the secret sauce"
8. Anecdote as authority: "I've lost more time to X than to Y"
9. Four or more consecutive very short sentences used for cadence
10. Second-person hype: "you'll never look at X the same way"
11. Em dash as a dramatic pause. Ceiling: two per thousand words.
12. Formulaic openers and segues: "in the world of", "in today's fast-paced",
    "let's dive in", "buckle up", "without further ado", "as we all know", "by
    the end of this post you will"
13. Assistant register: "great question", "I hope this helps", "happy coding",
    "feel free to reach out", "let me know if you have any questions"
14. Hedge presented as fact: "studies have shown", "experts agree", "it is
    widely believed", "it goes without saying". Name the study and link it, or
    make the claim in your own voice and defend it.
15. Citation-shaped text with nothing behind it: "Smith et al. (2021)" with no
    link, "according to a recent study", "[3]" with no reference list.
16. Padding: "it is important to note", "it should be noted", "due to the fact
    that", "as mentioned earlier", "when it comes to"
17. Non-answers: "there is no one-size-fits-all", "your mileage may vary", "it
    depends on your use case", "both approaches have their pros and cons". Give
    the condition that decides it.
18. Restating the same claim in successive sentences with the nouns swapped.
    Say it once.
19. Bullet lists where every item is a bolded label followed by one sentence.
    Either the items carry content, in which case write paragraphs, or they do
    not, in which case delete the list.

Filler words: genuinely, simply, actually, essentially, fundamentally, truly,
notably, importantly, it's worth noting, delve, leverage (verb), seamless,
crucial, pivotal, robust, unlock, elevate, deep dive, game-changer, journey,
transformative, in today's world.

Use any banned word when it is the precise technical term (a *robust*
estimator). Precision beats the ban; decoration does not.

## Before you finish

Run `.github/tools/slop-lint.py <changed files>` and report the exit status. Non-zero means
fix the text. If a hit is a false positive, say so and explain why.

A clean exit does not make a post publishable. The linter checks cadence tics,
padding, repetition, and unsourced citations. It cannot check whether you read
the paper you cited, ran the code you pasted, or reread the draft. Confirm
those separately.

<!-- slop-lint-disable-file : quotes the banned constructions as examples -->