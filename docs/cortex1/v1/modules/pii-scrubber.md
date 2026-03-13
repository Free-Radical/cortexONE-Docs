# PII Scrubber Module

**PRIVACY-FIRST**: PII scrubbing is MANDATORY before any cloud model call.

## Role

Protect privacy by ensuring that any text sent to cloud LLMs does not contain raw personally identifiable information (PII).

## Key Behavior

Scans text for:
- Names, emails, phone numbers, physical addresses
- Organization names, domain names, usernames, IDs
- Account numbers, SSNs, credit cards, and other identifiers

Replaces with configurable placeholder format:
- `<EMAIL_1>`, `<PHONE_1>` (deterministic mode)
- `<EMAIL_x9kf>`, `<PHONE_7pz3>` (non-deterministic mode)

## Scrubbing Modes

### Non-Deterministic Mode (Maximum Privacy)

- Same PII results in different placeholder IDs across calls
- Mapping exists only in memory, destroyed after call
- Makes correlation attacks much harder

**Use for**: Production with maximum privacy requirements

### Deterministic Mode (Default Implementation)

- Same PII produces consistent placeholders within a session
- Mapping can be logged for audit trail

**Use for**: Development, testing, audit requirements

### Design Decision

The implementation defaults to **deterministic mode** because:
1. Reproducible testing is essential for QA
2. Audit trail supports compliance requirements
3. PII never leaves local system regardless of token format
4. Non-deterministic mode available via config flag

This is a documented tradeoff, not a deviation from spec.

## Interaction with Local vs Cloud

**Local models**:
- Can use raw content (user option)
- Scrubbing optional but recommended

**Cloud models**:
- MUST always use PII-scrubbed text
- Model Gateway enforces `scrubbed=True` flag
- Scrubbing happens before any network call

## Recommended Libraries

- **scrubadub** (light): Basic PII detection, name detection with spacy
- **Presidio** (enterprise): Microsoft's comprehensive PII detection

## ZeroVeil SDK Integration

ZeroVeil SDK provides packaged PII scrubbing for use with ZeroVeil Gateway:
- **ZeroVeil SDK** (BSL, no fee): Presidio-based scrubbing, basic relay client.
- **ZeroVeil SDK Pro** (BSL + paid license): Presidio + regex + scrubadub, deterministic + non-deterministic modes, reversible token mapping, scrub audit logging.

The SDK scrubs client-side; the Gateway baseline PII gate catches anything the SDK misses.

See `zeroveil-gateway-pro/docs/editions.md` for the full product matrix.

## Baseline PII Gate (Gateway-Pro — Hard Security Invariant)

ZeroVeil Gateway Pro runs a baseline PII scan unconditionally on every request before forwarding to any model. This is a hard security invariant — it cannot be disabled by policy config.

### What the Baseline Scans

The baseline gate uses fast regex to detect the most dangerous PII categories:
- Social Security Numbers (SSNs)
- Credit card numbers
- Email addresses
- Phone numbers

### Relationship to Policy Config

The `pii_gate.enabled` policy flag controls **extended** PII detection (PHI patterns, custom regex patterns, configurable entity types). It does NOT control the baseline scan. The baseline runs regardless of `pii_gate.enabled`:

| `pii_gate.enabled` | Baseline scan (SSN, CC, email, phone) | Extended scan (PHI, custom patterns) |
|--------------------|---------------------------------------|---------------------------------------|
| `true`             | Always runs                           | Runs                                  |
| `false`            | Always runs                           | Skipped                               |

### Two-Layer Protection

1. **SDK layer** (client-side): SDK scrubs with `auto_scrub=True` by default. Catches names, emails, phones, addresses, account numbers, and other identifiers using Presidio + scrubadub.
2. **Gateway baseline layer** (server-side): Catches anything that slipped through the SDK, using fast regex on the four highest-risk categories.

This two-layer model ensures that even a misconfigured or outdated SDK version cannot cause raw SSNs or credit card numbers to reach a cloud model.

## Output

Returns:
- `scrubbed_text`: Text with PII replaced by tokens
- `scrub_metadata`: Structure with count and (optionally) mapping
- `scrub_mode`: "deterministic" or "nondeterministic"

## Configuration

```bash
# Scrubbing mode
CORTEX_PII_MODE=deterministic      # Default - stable tokens
CORTEX_PII_MODE=nondeterministic   # Maximum privacy - random tokens

# Enable scrubadub library
CORTEX_PII_USE_SCRUBADUB=1
```
