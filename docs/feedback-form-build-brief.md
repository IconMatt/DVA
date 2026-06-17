# Build brief: Feedback form (revised flow)

## Context

Multi-step feedback form for the Veteran and Family Wellbeing Agency. Users can submit a compliment, suggestion, or complaint — anonymously or with contact details. This brief replaces the previous 7/8-step flow with a streamlined version: 4 steps for compliments and suggestions, 6 steps for complaints.

Use our existing design system components (radio groups, text inputs, selects, textareas, buttons, progress indicator, info/alert banners, review summary). Do not introduce custom styling beyond layout composition.

---

## Global rules

1. **Branching sets the step count.** The total number of steps is fixed the moment feedback type is chosen on Step 1: compliments and suggestions = 4 steps, complaints = 6 steps. The progress indicator shows "Step x of y" plus a progress bar and never changes its total mid-flow.
2. **Identity is asked last, not first.** No personal details are requested until the Response preference step (the second-to-last step). Date of birth is never collected. DVA file number is optional and only shown on the Response preference step.
3. **Anonymity and response preference are one question.** A single "Would you like a response to your feedback?" question replaces the old separate "Do you wish to remain anonymous?" and "How would you like us to respond?" steps. Anonymous users are never asked for contact details or response method anywhere in the flow.
4. **Conditional reveal, not separate screens.** Selecting an option that needs more detail expands fields inline on the same screen (accordion/progressive disclosure), exactly one level deep. Collapsing a section clears its values after a confirm if any field was filled.
5. **State persistence.** All answers persist in client state across Back/Continue. Provide save-and-resume: persist draft to localStorage (or session API if available) and offer "Resume your draft?" on return. Drafts expire after 14 days.
6. **Back behaviour.** Every step except the landing page has a Back button (top-left of the button row). Back never loses data. When a user reaches a step via an Edit link from the Review screen, the Continue button reads "Save and return to review" and returns them directly to Review.
7. **Validation.** Validate on Continue, not on blur. Show inline errors below the field plus an error summary at the top of the step that links (anchor + focus) to each invalid field. Error messages state what to do, e.g. "Enter your email address in the format name@example.com".
8. **Required/optional convention.** Most fields are required, so mark only optional fields with "(optional)" after the label. Do not use asterisks.
9. **Dates.** All date inputs use three separate fields (day / month / year) or the design system's date component, with the hint "For example, 27 3 2026". Approximate dates are acceptable wherever dates appear in this form — say so in the hint.
10. **Urgent help is always reachable.** A persistent banner or footer link "Get urgent help now" (links to Open Arms 1800 011 046 and Lifeline 13 11 14) appears on the landing page and on every step, not just the confirmation.
11. **Accessibility.** WCAG 2.2 AA. One question per screen heading (h1). Radio groups use fieldset/legend. Focus moves to the h1 on step change. All conditional reveals are announced (aria-expanded / aria-live as appropriate). Form works fully with keyboard only.
12. **Free-text limits.** All textareas have a 2,500-character limit with a live character counter that appears once 75% is consumed.
13. **Phone alternative.** The landing page offers the phone channel (1800 789 789) as an equal alternative to the form, and the footer of every step repeats it.
14. **Naming.** Every screen header reads "Feedback form". (The previous build mislabelled the review screen "Referral form" — do not reproduce this.)
15. **Spam protection (anti-automation).** The form carries layered, server-validated anti-automation:
    - **Honeypot / timing trap — always on, zero friction.** An off-screen decoy field plus a minimum submit-time check that silently reject bots. Invisible to real users and assistive tech (`aria-hidden`, `tabindex="-1"`, `autocomplete="off"`).
    - **Accessible CAPTCHA on the final submit — defence-in-depth.** Must meet WCAG 2.2 AA: no image-only or audio-only-fallback challenge. Prefer an invisible/score-based or checkbox challenge with a working non-visual path. Renders on Review and submit, above the Submit button, and must not break keyboard focus order (rule 11).
    - **Server-side is authoritative.** The client never decides whether a submission is human; a failed challenge returns the user to Review with all answers preserved (rule 7 error pattern) and a clear, non-leaky message.
    - **Compensating controls.** WAF and rate limiting are expected at the infrastructure layer; the CAPTCHA is additional, not a substitute. Implementation/configuration is Drupal-side (CAPTCHA / Honeypot / Antibot on the Webform); this brief requires only that the protection exists and is accessible. If the security owner accepts the risk on WAF + rate limiting alone, record that decision here.
    *(Addresses a pen-test Low-severity finding: no anti-automation on the feedback form.)*

---

## Flow map

```
Landing
  └─ Step 1: Feedback type
       ├─ Compliment / Suggestion ──────────────┐
       └─ Complaint                              │
            ├─ Step 2: On behalf of a client?    │
            └─ Step 3: Raised elsewhere?         │
                                                 ▼
       Step 2 or 4: Your feedback
       Step 3 or 5: Response preference
       Step 4 or 6: Review and submit
       Confirmation
```

Step numbering shown to the user:
- Compliment/suggestion path: Feedback type (1/4) → Your feedback (2/4) → Response preference (3/4) → Review (4/4)
- Complaint path: Feedback type (1/6) → On behalf (2/6) → Raised elsewhere (3/6) → Your feedback (4/6) → Response preference (5/6) → Review (6/6)

---

## Screen 0 — Landing page

No step indicator.

**Heading:** Your feedback helps us improve our services for veterans, serving members, and their families.

**Body copy:** Whether it's a compliment, suggestion, or complaint, we want to hear from you. The form takes about 5–10 minutes. You can save your progress and come back later, and you can choose to stay anonymous.

**Primary action:** Button — "Start feedback form".

**Secondary channel:** Divider with "or", then: "Prefer to talk to someone? Call us on **1800 789 789**" (tel: link).

**Urgent help banner:** "If you or someone you know needs urgent support, call Open Arms on 1800 011 046 or Lifeline on 13 11 14." (links)

---

## Screen 1 — Feedback type (Step 1 of 4 or 1 of 6)

**Question (h1):** What type of feedback are you providing?

**Field:** Radio group, required.
| Option | Hint text |
|---|---|
| Compliment | Tell us what we did well |
| Suggestion | An idea to improve our services |
| Complaint | Something didn't meet your expectations |

**Validation:** "Select the type of feedback you are providing."

**Logic:** Compliment or Suggestion → step total becomes 4, next screen is Your feedback. Complaint → step total becomes 6, next screen is On behalf of a client. Changing this answer later (via Review edit) re-routes and re-numbers; previously entered answers on complaint-only steps are retained in state but excluded from submission and review if the user switches away from Complaint.

**Buttons:** Back (to landing) / Continue.

---

## Screen 2 — On behalf of a client? (complaints only, Step 2 of 6)

**Question (h1):** Are you making this complaint on behalf of an Agency client?

**Info banner (above options):** We can usually only accept a complaint from a third party (e.g. a family member) if the client has given their permission, unless relevant Privacy or Guardianship rules allow us to act without it.

**Field:** Radio group, required.
| Option | Hint text |
|---|---|
| No, the complaint is about my own experience | — |
| Yes, I am complaining on behalf of someone else | We'll ask for their details |

**Conditional reveal (when "Yes" is selected):**
- Sub-heading: Family member or client details
- `client_first_name` — text input, label "Their first name", required
- `client_surname` — text input, label "Their surname", required
- `client_relationship` — text input, label "Your relationship to them (optional)", e.g. "Daughter, carer, advocate"
- `consent_confirmed` — single checkbox, required: "I confirm this person knows I am making this complaint and has given their permission, or I believe permission rules do not apply in this case." Validation: "Confirm you have permission to complain on this person's behalf."

**Validation (Yes path):** first name and surname required: "Enter their first name" / "Enter their surname".

**Buttons:** Back / Continue.

---

## Screen 3 — Raised elsewhere? (complaints only, Step 3 of 6)

**Question (h1):** Have you raised this complaint with anyone else?

**Hint (below h1):** This helps us coordinate with other offices and avoid asking you to repeat yourself. It does not affect how seriously we treat your complaint.

**Field:** Radio group, required.
| Option |
|---|
| No, this is the first time I'm raising it |
| Yes, I've raised it with someone else |

**Conditional reveal (when "Yes" is selected):**
- `raised_with` — checkbox group (multiple allowed), label "Who did you contact?", required: Minister / Local MP / Commonwealth Ombudsman / Other
- If "Other" checked: `raised_with_other` — text input, label "Who else did you contact?", required
- `raised_date` — date input, label "When did you contact them? (optional)", hint "An approximate date is fine. For example, 3 2026."

**Validation:** "Select who you contacted" / "Tell us who else you contacted".

**Buttons:** Back / Continue.

---

## Screen 4 — Your feedback (Step 2 of 4 or 4 of 6)

**Heading (h1):** Your feedback

**Fields, in order:**

1. `feedback_detail` — textarea, label "Tell us about your feedback", required. Hint: "Include what happened, when, and who or which service was involved. Don't include anyone else's personal information unless it's needed." Validation: "Tell us about your feedback."
2. `outcome_sought` — textarea, label "What outcome would you like to see? (optional)". Hint: "For example, an apology, a decision reviewed, or a process improved."
3. `ill_treatment` — select, label "Does your feedback relate to ill treatment?", required, default option "Please select". Options: No / Yes / Not sure. *(Confirm the option list against the current production form — the source design was ambiguous here.)* If Yes or Not sure is selected, show inline info banner: "Thank you for telling us. Reports involving ill treatment are reviewed with priority." Validation: "Select whether your feedback relates to ill treatment."
4. `provider_details` — textarea, label "Provider or contractor details (optional)". Hint: "If your feedback relates to a specific provider or contractor, include their name and location."

**Buttons:** Back / Continue.

---

## Screen 5 — Response preference (Step 3 of 4 or 5 of 6)

**Question (h1):** Would you like a response to your feedback?

**Hint (below h1):** You can stay anonymous. If you do, we won't be able to contact you or let you know the outcome.

**Field:** Radio group, required.
| Option | Hint text |
|---|---|
| No, I want to remain anonymous | Your feedback is recorded without personal details |
| Yes, contact me about my feedback | We'll use the details below to follow up |

**When "No" is selected:** show info banner: "We'll still act on your feedback, but we won't be able to update you on what happens next." No further fields. All contact fields below are hidden and excluded from submission.

**Conditional reveal (when "Yes" is selected):**

1. `first_name` — text input, label "First name", required. Validation: "Enter your first name."
2. `surname` — text input, label "Surname", required. Validation: "Enter your surname."
3. `contact_method` — checkbox group (multi-select), label "How should we contact you?", hint "Select all that apply.", required (at least one): Email / Phone / Post. Validation: "Select how we should contact you." One of the following detail blocks renders per selected method:
   - Email → `email` — email input, label "Email address", required. Hint: "We'll only use this to respond to your feedback." Validation: format check.
   - Phone → `phone` — tel input, label "Phone number", required. Hint: "We may call from a private or blocked number." Validation: AU phone format, accept landline and mobile.
   - Post → `postal_address` — address fields per design system (address lines, suburb, state select, postcode), required. Hint: "Written responses can take 2–3 weeks to arrive."
4. `dva_file_number` — text input, label "DVA file number (optional)". Hint: "Providing this helps us link your feedback to your records faster."
5. **Complaints on behalf of someone else only** (Screen 2 answered "Yes"): `response_recipient` — radio group, label "Who should we respond to?", required: "Me" / "The person I'm complaining for". If the latter, reuse the same contact_method + detail field pattern for their contact details.

**Buttons:** Back / Continue.

---

## Screen 6 — Review and submit (Step 4 of 4 or 6 of 6)

**Heading (h1):** Review and submit your feedback

**Info banner:** Check your answers before submitting. Use Change to edit any answer.

**Summary list** (design system summary/review component), one row per answered question, in flow order, each with a "Change" link that opens the relevant step in edit mode (Continue becomes "Save and return to review"). Sections:

1. Feedback type
2. On behalf of a client? (complaints only — include the person's details and consent confirmation if applicable)
3. Raised elsewhere? (complaints only — include who and when if applicable)
4. Your feedback (all four fields; truncate long text to ~6 lines with "Show more")
5. Response preference — if anonymous, show "Anonymous — no response will be sent". If contact details given, show name, the selected methods, and the relevant detail per selected method only (never show fields for unselected methods).

Skipped/hidden questions never appear. Optional questions left blank show "Not provided".

**Declaration (above submit):** checkbox, required: "The information I have provided is true to the best of my knowledge." Validation: "Confirm your information is true to the best of your knowledge."

**Spam protection:** A Honeypot/timing trap runs invisibly throughout the flow; the accessible CAPTCHA/challenge (global rule 15) renders here, above the Submit button, without disrupting keyboard focus order.

**Buttons:** Back / "Submit feedback" (primary). On submit: disable button, show loading state, handle API failure with a retryable error banner that preserves all data.

---

## Screen 7 — Confirmation

No step indicator. Draft state is cleared on successful submission.

**Heading (h1):** Thank you for reaching out to the Veteran and Family Wellbeing Agency

**Confirmation panel:** "Your feedback has been received." Include a reference number (`FB-XXXXXXXX`) and, if a contact method was provided, "We've sent a confirmation to [email / your phone / your postal address]" plus expected response timeframe: "We aim to respond within 28 days."

**If anonymous:** "Because you chose to stay anonymous, we won't contact you, but your feedback will be reviewed and acted on."

**Resource cards (three):**
1. "Find a service" — Search for services near you. Link.
2. "Wellbeing resources for you" — Browse wellbeing information for veterans and families. Link.
3. "Get urgent help now" — Access 24/7 crisis and urgent support. Link. (Visually distinct per design system alert/featured pattern.)

---

## Data model (submission payload)

```
{
  feedback_type: "compliment" | "suggestion" | "complaint",
  on_behalf: { is_on_behalf, client_first_name?, client_surname?, client_relationship?, consent_confirmed? },   // complaints only
  raised_elsewhere: { has_raised, raised_with?[], raised_with_other?, raised_date? },                          // complaints only
  feedback: { detail, outcome_sought?, ill_treatment, provider_details? },
  response: {
    wants_response,
    contact?: { first_name, surname, methods[], email?, phone?, postal_address?, dva_file_number? },
    response_recipient?,            // on-behalf complaints only
    recipient_contact?              // if response_recipient = client
  },
  declaration_confirmed: true,
  submitted_at, draft_started_at
}
```

Fields for unselected branches must be omitted (not sent as empty strings).

---

## Out of scope

- Authentication / MyService integration
- File uploads
- Back-office triage views
- Translations (build with i18n-ready string keys, English only for now)
