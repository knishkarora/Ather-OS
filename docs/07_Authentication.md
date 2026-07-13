# Authentication

[[README|Knowledge Base Home]] > Authentication

Authentication is not implemented and is not currently applicable to the running codebase.

## Current State

The audited repository contains:

- No user model.
- No login route.
- No session handling.
- No JWT handling.
- No password hashing.
- No OAuth integration.
- No API key middleware.
- No environment variables for secrets.
- No frontend authentication UI.

Searches for common authentication and environment terms did not find implementation references in project source.

## Relationship to APIs

Because [[04_APIs|APIs]] are not implemented, there is no request authentication flow. When APIs are added, authentication decisions should be documented here before protected routes are introduced.

## Relationship to Database

The current [[03_Database|Database]] work is limited to workflow events. There are no user tables, sessions, refresh tokens, API keys, or ownership relationships.

## Future Questions

- Is Ather OS single-user local software during Phase 0?
- Should local mode skip authentication entirely?
- If remote mode is added, should access use user accounts, API keys, or a private deployment model?
- Should workflow ownership be modeled before remote execution?

These are open product decisions, not current implementation facts.

## Related

- [[04_APIs|APIs]]
- [[03_Database|Database]]
- [[09_Roadmap|Roadmap]]
- [[13_Decisions|Decisions]]
