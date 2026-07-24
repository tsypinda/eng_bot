# Roadmap for GB Eng_bot

> A Telegram bot for interactive English learning via gamified word practice.  
> Core MVP focus: API-driven card enrichment (translation + audio) and simple memorization games.  
>
> Status: MVP in progress.  
> Key risk: Over-engineering toward the long-term vision (e.g., textbook analysis).  
> Rule: All “textbook parsing” functionality is deferred to the backlog.

## Core MVP (Next 3 Weeks)

These tasks deliver the core value proposition: users can create lessons, get automatic translations/audio, and practice with simple games.

| Task | Description | Tech / APIs | Deadline | Status |
| :--- | :--- | :--- | :--- | :--- |
| [ ] Auto translation & audio | On word addition, the bot fetches translation and audio via API. | Yandex Translate + TTS/Forvo-like API | Week 1 | Plan |
| [ ] Manual translation override | Users can correct inaccurate auto-translations. | DB update logic + command handler | Week 1 | Plan |
| [ ] Context fill-in-the-blank game | Bot shows a sentence with the target word omitted; user fills it in. | Example sentence source + answer validation | Week 2 | Plan |
| [ ] Multiple-choice translation game | Bot shows a word and 4 translation options (1 correct). | Option generation logic + answer check | Week 2 | Plan |
| [ ] Step-by-step input flow | Replace complex command syntax with a state-machine guided flow (word → confirm → add to lesson). | FSM (Finite State Machine) implementation | Week 3 | Plan |

### MVP Completion Criteria

The MVP is considered ready when a user can complete the following end-to-end flow without errors or workarounds:

1. Create a new lesson.
2. Add 5 words (with auto-translation and audio fetched via API).
3. Play both games (context fill-in and multiple-choice) with these words.
4. Correct one auto-generated translation manually.
5. The bot retains all data across restarts and does not crash during the flow.

---

## Nice to Have (Post-MVP)

Features that improve usability but are not required for the initial release.

- [ ] Error history: show words where the user frequently makes mistakes.
- [ ] Time-limited challenges: add a timer to game rounds for increased engagement.
- [ ] Progress persistence: ensure robust data retention between sessions (if not already fully implemented).

---

## Backlog of Long-Term Ideas (Not for MVP)

High-level ambitions that must not influence the current MVP scope.

- [Idea] Textbook parsing: upload a textbook and generate a structured learning path per unit (long-term vision).
- [Idea] Level-based personalization (A1, B2, etc.) with adaptive content delivery.
- [Idea] Mobile app version or web dashboard for statistics.
