<!--
============================================================================
SYNC IMPACT REPORT
============================================================================
Version Change: Initial → 1.0.0
Constitution Type: MINOR (new constitution establishment)

Modified Principles:
- NEW: I. Code Quality Standards
- NEW: II. Test-First Development (NON-NEGOTIABLE)
- NEW: III. User Experience Consistency
- NEW: IV. Performance Requirements

Added Sections:
- Core Principles (4 principles established)
- Quality Gates & Review Process
- Development Standards

Removed Sections:
- None (initial version)

Templates Requiring Updates:
✅ plan-template.md - Constitution Check section aligns with new principles
✅ spec-template.md - User scenarios and requirements align with UX/testing principles
✅ tasks-template.md - Task structure supports test-first and quality standards

Follow-up TODOs:
- None - All placeholders filled with concrete values

Rationale for Version 1.0.0:
This is the initial establishment of the Shop MingChang constitution,
defining foundational governance for code quality, testing discipline,
user experience consistency, and performance requirements.
============================================================================
-->

# Shop MingChang Constitution

## Core Principles

### I. Code Quality Standards

All code contributed to Shop MingChang MUST meet these non-negotiable quality criteria:

- **Readability First**: Code MUST be self-documenting with clear variable/function names. Complex logic requires inline comments explaining the "why", not the "what".
- **Single Responsibility**: Each function, class, or module MUST have one clear purpose. Functions exceeding 50 lines or classes exceeding 300 lines require architectural justification.
- **No Silent Failures**: All error conditions MUST be explicitly handled. Use typed exceptions/errors with descriptive messages. Logging MUST capture sufficient context for debugging.
- **Type Safety**: Use strict typing where the language supports it (TypeScript strict mode, Python type hints, etc.). All public APIs MUST have type annotations.
- **DRY Principle**: Code duplication across more than 2 locations MUST be refactored into reusable utilities. Document intentional duplication when abstraction would harm clarity.
- **Code Reviews**: All changes MUST pass peer review verifying adherence to these standards before merge.

**Rationale**: E-commerce platforms require maintainability at scale. Poor code quality compounds technical debt exponentially as features multiply, leading to cascading bugs and slow feature delivery.

### II. Test-First Development (NON-NEGOTIABLE)

Test-Driven Development is mandatory for all Shop MingChang features:

- **Red-Green-Refactor Cycle**: Tests MUST be written first, approved by stakeholders, and MUST fail before implementation begins. Only then may implementation commence to make tests pass.
- **Test Categories Required**:
  - **Contract Tests**: All API endpoints, data schemas, and inter-service communication MUST have contract tests.
  - **Integration Tests**: User journeys spanning multiple components MUST have integration tests.
  - **Unit Tests**: Business logic and data transformations MUST have unit tests with >80% coverage.
- **Test Quality**: Tests MUST be deterministic, fast (<100ms per unit test), and independent. Flaky tests block deployment.
- **Test Documentation**: Each test MUST clearly state: Given (precondition), When (action), Then (expected outcome).
- **No Implementation Without Tests**: Pull requests lacking corresponding tests will be automatically rejected.

**Rationale**: E-commerce systems handle financial transactions and customer data. Test-first development prevents regressions, enables safe refactoring, and serves as living documentation. The cost of production bugs (lost sales, customer trust, legal liability) far exceeds testing investment.

### III. User Experience Consistency

Shop MingChang MUST deliver a cohesive, predictable user experience:

- **Design System Compliance**: All UI components MUST use the established design system. Custom components require UX team approval.
- **Accessibility (WCAG 2.1 AA)**: MUST support keyboard navigation, screen readers, and meet color contrast requirements. Test with accessibility tools before deployment.
- **Responsive Design**: All interfaces MUST function on mobile (320px width), tablet (768px), and desktop (1920px) viewports without horizontal scrolling or layout breaks.
- **Interaction Patterns**: Consistent patterns for common actions (add to cart, checkout, navigation). Document deviations with UX rationale.
- **Loading & Feedback**: All user actions MUST provide immediate feedback (<100ms). Operations exceeding 1 second MUST show progress indicators.
- **Error Messages**: User-facing errors MUST be actionable (tell users what to do next) and never expose technical implementation details.
- **Internationalization (i18n)**: All user-facing text MUST use translation keys, not hardcoded strings. Support RTL languages if applicable.

**Rationale**: Inconsistent UX increases cognitive load, reduces conversion rates, and drives customer abandonment. A unified experience builds trust and reduces support costs.

### IV. Performance Requirements

Shop MingChang MUST maintain these performance benchmarks:

- **Page Load Times**:
  - Initial page load (First Contentful Paint): <1.5 seconds on 3G connection
  - Time to Interactive: <3 seconds
  - Largest Contentful Paint: <2.5 seconds
- **API Response Times**:
  - Read operations (product listings, details): p95 <200ms
  - Write operations (add to cart, checkout): p95 <500ms
  - Search queries: p95 <300ms
- **Resource Budgets**:
  - JavaScript bundle: <300KB (gzipped) for initial load
  - Critical CSS: <50KB (inlined)
  - Images: Lazy-loaded, WebP format with fallbacks, max 200KB per image
- **Scalability**: System MUST handle 10x current traffic without degradation (load test before major launches).
- **Database Queries**: N+1 queries are prohibited. All queries MUST be indexed, with execution plans reviewed for operations >50ms.
- **Caching Strategy**: MUST implement multi-layer caching (CDN, application, database) with documented TTLs and invalidation strategies.
- **Performance Monitoring**: MUST instrument all critical paths with metrics (response times, error rates, resource usage). Alerts trigger at thresholds.

**Rationale**: Every 100ms of latency costs ~1% in sales. Performance directly impacts conversion rates, SEO rankings, and operational costs. Proactive performance budgets prevent degradation.

## Quality Gates & Review Process

All feature implementations MUST pass these gates before deployment:

### Pre-Implementation Gate
- Constitution compliance check completed (see plan-template.md Constitution Check section)
- Test scenarios written and stakeholder-approved
- Performance impact assessed (benchmarks for affected paths)

### Pre-Merge Gate
- All tests passing (unit, integration, contract)
- Code review approved by at least one peer
- No linting/formatting violations
- Type safety verified (no `any` types in TypeScript, etc.)
- Accessibility audit passed for UI changes
- Performance budgets not exceeded

### Pre-Deployment Gate
- Integration tests passing in staging environment
- Load testing completed for high-traffic features
- Monitoring/alerting configured for new functionality
- Rollback plan documented
- Security scan passed (dependency vulnerabilities, injection risks)

**Violation Handling**: Gates may be bypassed only for critical production incidents (P0 severity) with CTO approval and mandatory follow-up remediation within 48 hours.

## Development Standards

### Documentation Requirements
- All public APIs MUST have usage examples and parameter descriptions
- Architectural decisions MUST be documented in `specs/` directory
- README MUST be updated when adding new services or major features

### Dependency Management
- Security patches MUST be applied within 7 days of disclosure
- Major version upgrades require risk assessment and testing plan
- New dependencies require team review (license, maintenance status, bundle size impact)

### Branching & Deployment
- Feature branches MUST follow naming: `###-feature-name` (from spec.md)
- Commits MUST reference task IDs from tasks.md
- Main branch is protected: requires passing CI/CD and approvals
- Deploy during low-traffic windows; monitor for 1 hour post-deployment

### Observability
- All services MUST emit structured logs (JSON format)
- Critical user journeys MUST have distributed tracing
- Business metrics tracked: conversion rate, cart abandonment, checkout completion
- Technical metrics tracked: error rates, latency percentiles, resource utilization

## Governance

**Authority**: This constitution supersedes all conflicting practices, coding conventions, or individual preferences. When principles conflict with delivery timelines, the principle takes precedence—adjust scope, not quality.

**Amendment Process**:
1. Proposed amendments MUST document rationale and impact analysis
2. Require approval from technical leadership and affected stakeholders
3. Version bump follows semantic versioning:
   - **MAJOR**: Principle removal or backward-incompatible redefinition
   - **MINOR**: New principle added or material expansion
   - **PATCH**: Clarifications, wording fixes, non-semantic refinements
4. Amendments MUST include migration plan for existing code
5. All team members MUST be notified of constitution changes within 24 hours

**Compliance Verification**:
- All pull requests MUST include constitution compliance checklist
- Quarterly audits of codebase against constitution principles
- Principle violations raised in code review MUST be addressed before merge
- Persistent pattern of violations triggers architecture review

**Continuous Improvement**: Constitution principles are living standards. Feedback from retrospectives, production incidents, and team observations inform evolution.

**Version**: 1.0.0 | **Ratified**: 2025-11-12 | **Last Amended**: 2025-11-12
