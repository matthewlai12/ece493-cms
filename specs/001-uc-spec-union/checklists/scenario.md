# Scenario Checklist: UC-Driven Specification & Unified UAT

**Purpose**: Validate user scenarios, acceptance criteria, and UAT alignment before implementation planning
**Created**: 2026-02-10
**Feature**: specs/001-uc-spec-union/spec.md

## User Story Coverage

- [ ] CHK001 All 29 user stories are present and uniquely named (UC-01 through UC-29)
- [ ] CHK002 Each user story includes a priority (P1/P2/P3)
- [ ] CHK003 Each user story is independently testable and states an independent test
- [ ] CHK004 Primary actor is clear for each user story
- [ ] CHK005 Story ordering reflects priority and end-to-end user journeys

## Acceptance Scenarios Quality

- [ ] CHK006 Every user story includes at least one main success scenario
- [ ] CHK007 Every user story includes at least one failure/edge scenario
- [ ] CHK008 Scenarios use clear Given/When/Then format
- [ ] CHK009 Scenarios are testable without implementation details
- [ ] CHK010 Scenarios avoid ambiguous terms (e.g., "fast", "secure") without measurable criteria
- [ ] CHK011 Scenario outcomes match the Success/Failed End Conditions in the related UC

## Edge Case Coverage

- [ ] CHK012 Validation failures are covered for registration, login, submission, and review flows
- [ ] CHK013 File upload errors (format/size/availability) are covered
- [ ] CHK014 Database/storage unavailability is covered for read and write paths
- [ ] CHK015 Scheduling conflicts and constraint violations are covered
- [ ] CHK016 Payment failures and provider downtime are covered
- [ ] CHK017 Notification delivery failures are covered

## UAT Alignment

- [ ] CHK018 All TC-XX acceptance tests are listed as UAT sources
- [ ] CHK019 UAT index location is defined and referenced
- [ ] CHK020 Each P1 user story has at least one matching UAT test scenario
- [ ] CHK021 UAT tests include both primary and alternate flows

## Traceability & Consistency

- [ ] CHK022 Use case coverage map links every UC to exactly one user story
- [ ] CHK023 Functional requirements map to user stories and scenarios
- [ ] CHK024 Security/privacy considerations are reflected in scenarios where relevant
- [ ] CHK025 Success criteria are supported by at least one scenario or metric

## Notes

- Check items off as completed: `[x]`
- Add comments or findings inline
