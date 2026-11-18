---
name: hcm-grid-writing
description: Write or rewrite pages and posts for The Grid (HCM's intranet, thegrid.hcmdesign.com) in the voice of HCM IT, modelled on the Director of IT's own pages (Emerging Technology, IT Policies, ChatGPT Enterprise Getting Started and FAQ, AI-Assisted Coding Policy) and IT's announcement posts. Use this whenever the user asks for a Grid page, Grid post, intranet article, user guide, FAQ, policy page, course lesson or announcement for HCM staff, or says something "doesn't sound like HCM IT", even if they don't say "Grid". Also use it to review a draft against the HCM IT voice. Not for Hudu (IT-only KB articles), vault docs, SOQs or proposals.
---

# Writing for The Grid in the HCM IT voice

The Grid is read by every employee: architects, designers, planners, BD, HR, accounting. HCM IT's pages on it have a recognizable voice, set by the Director of IT. It is measured, complete, and institutional: IT speaks for the firm as "we", explains *why* before *what*, and never sounds clipped, clever or blaming. Drafts that read like a terse tech-support cheat sheet get rejected as "not the voice of HCM IT", so match this voice even when the user asks for something "simple" or "user friendly". Simple means plain words and clear structure, not short fragments.

First decide which of the three forms you are writing. They share a vocabulary but differ in tone.

| Form | Examples on the Grid | Tone |
|---|---|---|
| **Reference / how-to page** | Getting Started, FAQ, Standard Tools, Approved Tools, course lessons | Formal, helpful, "we recommend", second person for the reader |
| **Policy / philosophy page** | AI-Assisted Coding Policy and Philosophy, Our Approach | Formal and precise; defined terms, numbered rules, "must", "may not", a stated basis |
| **Announcement post** | "ChatGPT Enterprise is HERE!", "Fast Is Easy. Control Is Hard." | Warmer, first person ("I", "we"), may open with a story or analogy, ends with a link and a call to action |

Read `references/examples.md` for short excerpts of each form before writing a long piece.

## Voice rules for every form

- **Open by defining the subject or stating the purpose**, in one or two full sentences, before any steps or lists. Examples: "Approved tools are technologies that have completed evaluation and are available for controlled use within the firm." / "This page will walk you through..."
- **Explain the why.** Every limit, rule or recommendation carries its reason ("to protect HCM's information", "to help manage HCM's shared credit allowance"). Philosophy pages give it a whole section ("Why Structure Is Necessary", "Start with 'Why'").
- **Full, grammatical sentences.** No fragments ("Quick.", "That's switched off at HCM."), no punchy asides, no metaphors on reference or policy pages. Analogies belong in posts only.
- **IT is "we"; the reader is "you"; the organization is "HCM" or "the firm".** "We recommend", "we encourage you", "contact IT before proceeding". Posts may use "I".
- **Measured, non-absolute wording:** "may", "can", "generally", "typically", "significantly", "in many cases". Reserve "must" and "may not" for policy.
- **Never blame or speculate about the reader.** Not "most people who hit their limit were in Work without knowing it"; instead "usage limits are most often reached by working in Work mode".
- **Responsibility language:** "You remain responsible for...", "apply your professional judgment", "human oversight", "keeping judgment with the project team".
- **Serial (Oxford) comma** in lists of three or more on pages.
- **Firm vocabulary:** firmwide, firm-managed, approved, appropriate, intended, "consistent with HCM's [Artificial Intelligence Policy](/page/1311/artificial-intelligence)" (only when the subject involves AI; don't force a policy link onto an unrelated page), "contact IT", "submit a support ticket", AEC examples (school facilities director, RFIs, submittals, CA, specifications, Revit, Bluebeam).
- **Product terms as HCM IT uses them:** "Chat mode" / "Work mode", "monthly usage allowance", "consume credits", "upper-left corner", "select" for clicks.
- **No em-dashes**, ever (a hard rule of the user's). Use a comma, colon, parentheses or two sentences.
- **Never name individual IT staff in the body text.** Contacts go in the Grid's Contact employee block, which the page author adds in the editor.

## Structure and formatting

- **Headings in Title Case that name the topic:** "Understanding Chat and Work Modes", "Making the Most of Your Allowance", "Authorization and Approval". Not conversational headings ("Stuck? Quick fixes", "I want to...").
- **Heading levels on the Grid:** `####` for page sections, `#####` for subsections, `######` for numbered practices inside a lesson. Page titles follow `Area - Topic` (for example "Emerging Technology - ChatGPT Enterprise FAQ", "IT Policies - Standard Tools").
- **Label-colon lists** for categorized items: "**Project Quality and Risk:** Using AI as a first-pass review aid across...". Each label is followed by a full sentence.
- **Bold lead-in sentences** for the key point of a paragraph: "**An important distinction: Work does not inherently provide better answers than Chat.**" followed by the explanation.
- **FAQs** are full questions as headings ("Why can't ChatGPT find a meeting, email or file I know I can access?") answered in two to four sentences.
- **Steps** are numbered, one action each, naming the exact control in bold ("Select **ChatGPT** in the upper-left corner and choose **Chat**").
- Occasional emphasis in caps for one critical word ("NOTE:", "NOT") is in character; use it sparingly.
- **Links** are inline Grid-relative links (`/page/2321/...`), plus a closing "See also" line.
- **Endings:**
  - Reference pages close with the responsible-use reminder when AI is involved ("ChatGPT Enterprise provides a secure, HCM-managed environment, but it does not replace good judgment...") and a "Need Help?" line pointing to IT. Note that a Contact block belongs at the bottom.
  - Policy pages close with "Exceptions and Enforcement" or "The Balance We Are Seeking".
  - Posts close with a link and an invitation ("continue sending ideas...", "stop by and talk with me").

## Policy pages specifically

Use this order: Overview, Scope, the rules (numbered, each starting with a bold or labelled imperative such as "Not share or distribute without review."), Prerequisites, Exceptions and Enforcement. Define roles or terms in their own section ("What Do We Mean by 'Owner'?"). Cite the basis where there is one (NIST, the AI Policy).

## Posts specifically

- A short, catchy title is welcome ("Fast Is Easy. Control Is Hard.", "They Moved the Goalpost...and changed the ball!").
- Open with context, a question to the reader, or a story, then turn it to HCM in one sentence.
- Short punchy lines are allowed here ("The faster the engine, the more important the brakes.") but the body is still full paragraphs.
- Bulleted "Here are just a few examples..." lists use label-colon form.
- A "A few important things to know:" block for the rules.
- End with the action and the link.

## Workflow

1. Identify the form and the audience. If the content touches ChatGPT, the AI Policy or approved tools, check the current Grid pages with The Grid MCP (`search`, `fetch`) so terms, figures and links match what is published. Don't contradict a published course or FAQ; if the facts differ, flag it to the user.
2. Draft in Markdown that pastes cleanly into the Grid editor.
3. Review against the voice rules above: opener, why, full sentences, "we/you", measured wording, no blame, Title Case headings, serial commas, no em-dashes, no staff names.
4. Deliver the page, then a short separate "Notes" section (not part of the page) for anything the author must do in the Grid editor: screenshots, callout styling, the Contact block, where the page should sit, facts to verify.
