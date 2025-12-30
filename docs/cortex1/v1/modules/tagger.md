# Tagger Module

## Status: Implemented ✅

See `cortex1-core/docs/tagging-system.md` for full implementation details.

## Role
Add standardized tags to structured items to help downstream logic.

## Core Tags (Original Design)
- `@time`: Approximate effort (e.g., "5m", "15m", "30m", "60m")
- `@energy`: "Low", "Medium", or "High" cognitive/mental effort
- `@deadline`: A normalized date/time if one exists
- `@context`: Short label describing where/how the task is done
- `@owner`: Usually "Saq", but can support multiple identities in future

## Email-Specific Tags (Implemented)

**Classification:**
- `@category`: VIP, CRITICAL, Work, Personal, Shopping, Notification, Marketing, Spam
- `@vip`, `@critical`, `@shopping`, `@notification`, `@spam`, `@likely_spam`

**Urgency (3-Tier):**
- `@urgency_level`: critical, high, normal
- `@high_priority`, `@needs_verification`, `@potential_critical`

**Response Detection:**
- `@response_needed`: Email needs a reply
- `@no_response_needed`: No reply expected (notifications, receipts, spam)

**Spam Detection:**
- `@spam_score`: 0-15 (≥8 = spam, 5-7 = marketing, <5 = clean)

**Metadata:**
- `@from_domain`, `@thread`, `@source_adapter`
- `@forwarded`, `@forwarded_depth`
- `@priority`, `@sensitivity`, `@bulk`, `@list_unsubscribe`

## Design Notes
- Rule-based with keyword matching and heuristics
- ML categorizer available for hybrid classification
- Anti-spam heuristics downgrade fake urgency in marketing emails
- Domain-agnostic core with email-specific extensions