---

description: "Task list template for feature implementation"

---

# Tasks: UC-Driven Specification & Unified UAT

**Input**: Design documents from `/specs/001-uc-spec-union/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/ and tests/
- [X] T002 Initialize Python project and dependency manifest in pyproject.toml
- [X] T003 Configure linting and formatting in pyproject.toml
- [X] T004 Create base FastAPI app scaffold in src/api/app.py
- [X] T005 Create web UI scaffold in src/web/app.py
- [X] T006 Add environment configuration loader in src/config/settings.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Setup database connection and base ORM models in src/models/base.py
- [X] T008 Create Alembic migration setup in alembic.ini and migrations/
- [X] T009 [P] Implement role-based access control middleware in src/api/middleware/rbac.py
- [X] T010 [P] Implement authentication service in src/services/auth_service.py
- [X] T011 [P] Implement audit logging utilities in src/services/audit_log.py
- [X] T012 [P] Implement file storage client in src/services/storage_client.py
- [X] T013 [P] Implement notification service (email) in src/services/notification_service.py
- [X] T014 [P] Implement payment provider client in src/services/payment_client.py
- [X] T015 [P] Implement scheduling engine base in src/services/scheduling_engine.py
- [X] T016 Create shared API routing in src/api/routes.py
- [X] T017 Create shared web routing in src/web/routes.py
- [X] T018 Define UAT index placeholder in specs/001-uc-spec-union/uat/uat-index.md

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - UC-01 View Public Announcements (Priority: P3)

**Goal**: UC-01 View Public Announcements

**Independent Test**: Public announcements are successfully retrieved and displayed to the guest

### Implementation for User Story 1

- [X] T019 [P] [US1] Create or update Announcement model in src/models/announcement.py
- [X] T020 [P] [US1] Implement announcements service in src/services/announcements_service.py
- [X] T021 [US1] Implement API handler in src/api/announcements.py
- [X] T022 [US1] Wire API route in src/api/routes.py
- [X] T023 [US1] Implement web handler/page in src/web/announcements.py
- [X] T024 [US1] Wire web route in src/web/routes.py

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - UC-02 View Conference Registration Prices (Priority: P3)

**Goal**: UC-02 View Conference Registration Prices

**Independent Test**: The conference registration price list is successfully displayed to the guest

### Implementation for User Story 2

- [X] T025 [P] [US2] Create or update RegistrationPrice model in src/models/registrationprice.py
- [X] T026 [P] [US2] Implement registration_prices service in src/services/registration_prices_service.py
- [X] T027 [US2] Implement API handler in src/api/registration_prices.py
- [X] T028 [US2] Wire API route in src/api/routes.py
- [X] T029 [US2] Implement web handler/page in src/web/registration_prices.py
- [X] T030 [US2] Wire web route in src/web/routes.py

**Checkpoint**: User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - UC-03 View Conference Schedule (Priority: P3)

**Goal**: UC-03 View Conference Schedule

**Independent Test**: The published conference schedule is successfully displayed to the guest

### Implementation for User Story 3

- [X] T031 [P] [US3] Create or update Schedule model in src/models/schedule.py
- [X] T032 [P] [US3] Implement schedule_view service in src/services/schedule_view_service.py
- [X] T033 [US3] Implement API handler in src/api/schedule_view.py
- [X] T034 [US3] Wire API route in src/api/routes.py
- [X] T035 [US3] Implement web handler/page in src/web/schedule_view.py
- [X] T036 [US3] Wire web route in src/web/routes.py

**Checkpoint**: User Story 3 should be fully functional and testable independently

---

## Phase 6: User Story 4 - UC-04 Register User Account (Priority: P1)

**Goal**: UC-04 Register User Account

**Independent Test**: A new user account is successfully created and stored in the CMS database, and the user is redirected to the login page

### Tests for User Story 4 (REQUIRED for P1) ⚠️

- [X] T037 [P] [US4] Create contract test in tests/contract/test_user_registration.py
- [X] T038 [P] [US4] Create integration test in tests/integration/test_user_registration.py

### Implementation for User Story 4

- [X] T039 [P] [US4] Create or update UserAccount model in src/models/useraccount.py
- [X] T040 [P] [US4] Implement user_registration service in src/services/user_registration_service.py
- [X] T041 [US4] Implement API handler in src/api/user_registration.py
- [X] T042 [US4] Wire API route in src/api/routes.py
- [X] T043 [US4] Implement web handler/page in src/web/user_registration.py
- [X] T044 [US4] Wire web route in src/web/routes.py

**Checkpoint**: User Story 4 should be fully functional and testable independently

---

## Phase 7: User Story 5 - UC-05 Validate Registration Information (Priority: P2)

**Goal**: UC-05 Validate Registration Information

**Independent Test**: The user’s registration information is validated successfully, allowing the account creation process to continue

### Implementation for User Story 5

- [X] T045 [P] [US5] Create or update UserAccount model in src/models/useraccount.py
- [X] T046 [P] [US5] Implement registration_validation service in src/services/registration_validation_service.py
- [X] T047 [US5] Implement API handler in src/api/registration_validation.py
- [X] T048 [US5] Wire API route in src/api/routes.py
- [X] T049 [US5] Implement web handler/page in src/web/registration_validation.py
- [X] T050 [US5] Wire web route in src/web/routes.py

**Checkpoint**: User Story 5 should be fully functional and testable independently

---

## Phase 8: User Story 6 - UC-06 Log In to System (Priority: P1)

**Goal**: UC-06 Log In to System

**Independent Test**: The user is successfully authenticated and redirected to their personalized dashboard

### Tests for User Story 6 (REQUIRED for P1) ⚠️

- [X] T051 [P] [US6] Create contract test in tests/contract/test_auth_login.py
- [X] T052 [P] [US6] Create integration test in tests/integration/test_auth_login.py

### Implementation for User Story 6

- [X] T053 [P] [US6] Create or update UserAccount model in src/models/useraccount.py
- [X] T054 [P] [US6] Implement auth_login service in src/services/auth_login_service.py
- [X] T055 [US6] Implement API handler in src/api/auth_login.py
- [X] T056 [US6] Wire API route in src/api/routes.py
- [X] T057 [US6] Implement web handler/page in src/web/auth_login.py
- [X] T058 [US6] Wire web route in src/web/routes.py
- [X] T059 [US6] Add audit logging for auth_login actions in src/services/audit_log.py

**Checkpoint**: User Story 6 should be fully functional and testable independently

---

## Phase 9: User Story 7 - UC-07 Change Password (Priority: P2)

**Goal**: UC-07 Change Password

**Independent Test**: The user’s password is successfully updated in the CMS database, and the new password is required for future logins

### Implementation for User Story 7

- [X] T060 [P] [US7] Create or update UserAccount model in src/models/useraccount.py
- [X] T061 [P] [US7] Implement auth_password service in src/services/auth_password_service.py
- [X] T062 [US7] Implement API handler in src/api/auth_password.py
- [X] T063 [US7] Wire API route in src/api/routes.py
- [X] T064 [US7] Implement web handler/page in src/web/auth_password.py
- [X] T065 [US7] Wire web route in src/web/routes.py

**Checkpoint**: User Story 7 should be fully functional and testable independently

---

## Phase 10: User Story 8 - UC-08 Submit Paper Manuscript (Priority: P1)

**Goal**: UC-08 Submit Paper Manuscript

**Independent Test**: The paper manuscript and all required submission information are successfully stored and marked as submitted for review

### Tests for User Story 8 (REQUIRED for P1) ⚠️

- [X] T066 [P] [US8] Create contract test in tests/contract/test_submission_create.py
- [X] T067 [P] [US8] Create integration test in tests/integration/test_submission_create.py

### Implementation for User Story 8

- [X] T068 [P] [US8] Create or update Submission model in src/models/submission.py
- [X] T069 [P] [US8] Implement submission_create service in src/services/submission_create_service.py
- [X] T070 [US8] Implement API handler in src/api/submission_create.py
- [X] T071 [US8] Wire API route in src/api/routes.py
- [X] T072 [US8] Implement web handler/page in src/web/submission_create.py
- [X] T073 [US8] Wire web route in src/web/routes.py
- [X] T074 [US8] Add audit logging for submission_create actions in src/services/audit_log.py

**Checkpoint**: User Story 8 should be fully functional and testable independently

---

## Phase 11: User Story 9 - UC-09 Upload Manuscript File (Priority: P1)

**Goal**: UC-09 Upload Manuscript File

**Independent Test**: The manuscript file is successfully validated, stored, and associated with the author’s paper submission

### Tests for User Story 9 (REQUIRED for P1) ⚠️

- [X] T075 [P] [US9] Create contract test in tests/contract/test_manuscript_upload.py
- [X] T076 [P] [US9] Create integration test in tests/integration/test_manuscript_upload.py

### Implementation for User Story 9

- [X] T077 [P] [US9] Create or update ManuscriptFile model in src/models/manuscriptfile.py
- [X] T078 [P] [US9] Implement manuscript_upload service in src/services/manuscript_upload_service.py
- [X] T079 [US9] Implement API handler in src/api/manuscript_upload.py
- [X] T080 [US9] Wire API route in src/api/routes.py
- [X] T081 [US9] Implement web handler/page in src/web/manuscript_upload.py
- [X] T082 [US9] Wire web route in src/web/routes.py
- [X] T083 [US9] Add audit logging for manuscript_upload actions in src/services/audit_log.py

**Checkpoint**: User Story 9 should be fully functional and testable independently

---

## Phase 12: User Story 10 - UC-10 Save Submission Progress (Priority: P1)

**Goal**: UC-10 Save Submission Progress

**Independent Test**: The current state of the paper submission is successfully stored and can be retrieved later by the author

### Tests for User Story 10 (REQUIRED for P1) ⚠️

- [X] T084 [P] [US10] Create contract test in tests/contract/test_submission_save.py
- [X] T085 [P] [US10] Create integration test in tests/integration/test_submission_save.py

### Implementation for User Story 10

- [X] T086 [P] [US10] Create or update Submission model in src/models/submission.py
- [X] T087 [P] [US10] Implement submission_save service in src/services/submission_save_service.py
- [X] T088 [US10] Implement API handler in src/api/submission_save.py
- [X] T089 [US10] Wire API route in src/api/routes.py
- [X] T090 [US10] Implement web handler/page in src/web/submission_save.py
- [X] T091 [US10] Wire web route in src/web/routes.py
- [X] T092 [US10] Add audit logging for submission_save actions in src/services/audit_log.py

**Checkpoint**: User Story 10 should be fully functional and testable independently

---

## Phase 13: User Story 11 - UC-11 Receive Paper Decision (Priority: P2)

**Goal**: UC-11 Receive Paper Decision

**Independent Test**: The author successfully receives and can view the final decision (accept or reject) for their paper

### Implementation for User Story 11

- [X] T093 [P] [US11] Create or update Decision model in src/models/decision.py
- [X] T094 [P] [US11] Implement decision_notify service in src/services/decision_notify_service.py
- [X] T095 [US11] Implement API handler in src/api/decision_notify.py
- [X] T096 [US11] Wire API route in src/api/routes.py
- [X] T097 [US11] Implement web handler/page in src/web/decision_notify.py
- [X] T098 [US11] Wire web route in src/web/routes.py

**Checkpoint**: User Story 11 should be fully functional and testable independently

---

## Phase 14: User Story 12 - UC-12 Receive Presentation Schedule (Priority: P2)

**Goal**: UC-12 Receive Presentation Schedule

**Independent Test**: The author successfully receives and can view the presentation schedule details for their accepted paper

### Implementation for User Story 12

- [X] T099 [P] [US12] Create or update Schedule model in src/models/schedule.py
- [X] T100 [P] [US12] Implement schedule_notify service in src/services/schedule_notify_service.py
- [X] T101 [US12] Implement API handler in src/api/schedule_notify.py
- [X] T102 [US12] Wire API route in src/api/routes.py
- [X] T103 [US12] Implement web handler/page in src/web/schedule_notify.py
- [X] T104 [US12] Wire web route in src/web/routes.py

**Checkpoint**: User Story 12 should be fully functional and testable independently

---

## Phase 15: User Story 13 - UC-13 Receive Review Invitation (Priority: P2)

**Goal**: UC-13 Receive Review Invitation

**Independent Test**: The referee successfully receives a review invitation and can view the paper details and respond to the invitation

### Implementation for User Story 13

- [X] T105 [P] [US13] Create or update ReviewInvitation model in src/models/reviewinvitation.py
- [X] T106 [P] [US13] Implement review_invite_notify service in src/services/review_invite_notify_service.py
- [X] T107 [US13] Implement API handler in src/api/review_invite_notify.py
- [X] T108 [US13] Wire API route in src/api/routes.py
- [X] T109 [US13] Implement web handler/page in src/web/review_invite_notify.py
- [X] T110 [US13] Wire web route in src/web/routes.py

**Checkpoint**: User Story 13 should be fully functional and testable independently

---

## Phase 16: User Story 14 - UC-14 Accept or Reject Review Invitation (Priority: P2)

**Goal**: UC-14 Accept or Reject Review Invitation

**Independent Test**: The referee’s response (accept or reject) is successfully recorded, and the system updates the review assignment status accordingly

### Implementation for User Story 14

- [X] T111 [P] [US14] Create or update ReviewInvitation model in src/models/reviewinvitation.py
- [X] T112 [P] [US14] Implement review_invite_response service in src/services/review_invite_response_service.py
- [X] T113 [US14] Implement API handler in src/api/review_invite_response.py
- [X] T114 [US14] Wire API route in src/api/routes.py
- [X] T115 [US14] Implement web handler/page in src/web/review_invite_response.py
- [X] T116 [US14] Wire web route in src/web/routes.py

**Checkpoint**: User Story 14 should be fully functional and testable independently

---

## Phase 17: User Story 15 - UC-15 Access Assigned Papers (Priority: P2)

**Goal**: UC-15 Access Assigned Papers

**Independent Test**: The referee successfully views the list of assigned papers and can access the manuscript files for review

### Implementation for User Story 15

- [X] T117 [P] [US15] Create or update Submission model in src/models/submission.py
- [X] T118 [P] [US15] Implement assigned_papers service in src/services/assigned_papers_service.py
- [X] T119 [US15] Implement API handler in src/api/assigned_papers.py
- [X] T120 [US15] Wire API route in src/api/routes.py
- [X] T121 [US15] Implement web handler/page in src/web/assigned_papers.py
- [X] T122 [US15] Wire web route in src/web/routes.py

**Checkpoint**: User Story 15 should be fully functional and testable independently

---

## Phase 18: User Story 16 - UC-16 Submit Paper Review (Priority: P1)

**Goal**: UC-16 Submit Paper Review

**Independent Test**: The completed review form is successfully stored in the CMS and made available to the editor

### Tests for User Story 16 (REQUIRED for P1) ⚠️

- [X] T123 [P] [US16] Create contract test in tests/contract/test_review_submit.py
- [X] T124 [P] [US16] Create integration test in tests/integration/test_review_submit.py

### Implementation for User Story 16

- [X] T125 [P] [US16] Create or update Review model in src/models/review.py
- [X] T126 [P] [US16] Implement review_submit service in src/services/review_submit_service.py
- [X] T127 [US16] Implement API handler in src/api/review_submit.py
- [X] T128 [US16] Wire API route in src/api/routes.py
- [X] T129 [US16] Implement web handler/page in src/web/review_submit.py
- [X] T130 [US16] Wire web route in src/web/routes.py
- [X] T131 [US16] Add audit logging for review_submit actions in src/services/audit_log.py

**Checkpoint**: User Story 16 should be fully functional and testable independently

---

## Phase 19: User Story 17 - UC-17 Enforce Referee Workload Limit (Priority: P2)

**Goal**: UC-17 Enforce Referee Workload Limit

**Independent Test**: The referee is assigned no more than five papers, and any attempt to exceed this limit is prevented by the system

### Implementation for User Story 17

- [X] T132 [P] [US17] Create or update ReviewInvitation model in src/models/reviewinvitation.py
- [X] T133 [P] [US17] Implement referee_workload service in src/services/referee_workload_service.py
- [X] T134 [US17] Implement API handler in src/api/referee_workload.py
- [X] T135 [US17] Wire API route in src/api/routes.py
- [X] T136 [US17] Implement web handler/page in src/web/referee_workload.py
- [X] T137 [US17] Wire web route in src/web/routes.py

**Checkpoint**: User Story 17 should be fully functional and testable independently

---

## Phase 20: User Story 18 - UC-18 Assign Referees to Submitted Papers (Priority: P1)

**Goal**: UC-18 Assign Referees to Submitted Papers

**Independent Test**: Referees are successfully assigned to submitted papers and notified

### Tests for User Story 18 (REQUIRED for P1) ⚠️

- [X] T138 [P] [US18] Create contract test in tests/contract/test_referee_assign.py
- [X] T139 [P] [US18] Create integration test in tests/integration/test_referee_assign.py

### Implementation for User Story 18

- [X] T140 [P] [US18] Create or update ReviewInvitation model in src/models/reviewinvitation.py
- [X] T141 [P] [US18] Implement referee_assign service in src/services/referee_assign_service.py
- [X] T142 [US18] Implement API handler in src/api/referee_assign.py
- [X] T143 [US18] Wire API route in src/api/routes.py
- [X] T144 [US18] Implement web handler/page in src/web/referee_assign.py
- [X] T145 [US18] Wire web route in src/web/routes.py
- [X] T146 [US18] Add audit logging for referee_assign actions in src/services/audit_log.py

**Checkpoint**: User Story 18 should be fully functional and testable independently

---

## Phase 21: User Story 19 - UC-19 Ensure Three Referees per Paper (Priority: P2)

**Goal**: UC-19 Ensure Three Referees per Paper

**Independent Test**: Each paper has exactly three referees assigned before review proceeds

### Implementation for User Story 19

- [X] T147 [P] [US19] Create or update ReviewInvitation model in src/models/reviewinvitation.py
- [X] T148 [P] [US19] Implement three_referees service in src/services/three_referees_service.py
- [X] T149 [US19] Implement API handler in src/api/three_referees.py
- [X] T150 [US19] Wire API route in src/api/routes.py
- [X] T151 [US19] Implement web handler/page in src/web/three_referees.py
- [X] T152 [US19] Wire web route in src/web/routes.py

**Checkpoint**: User Story 19 should be fully functional and testable independently

---

## Phase 22: User Story 20 - UC-20 Receive Completed Review Forms (Priority: P2)

**Goal**: UC-20 Receive Completed Review Forms

**Independent Test**: The editor can access completed review forms for evaluation

### Implementation for User Story 20

- [X] T153 [P] [US20] Create or update Review model in src/models/review.py
- [X] T154 [P] [US20] Implement review_access service in src/services/review_access_service.py
- [X] T155 [US20] Implement API handler in src/api/review_access.py
- [X] T156 [US20] Wire API route in src/api/routes.py
- [X] T157 [US20] Implement web handler/page in src/web/review_access.py
- [X] T158 [US20] Wire web route in src/web/routes.py

**Checkpoint**: User Story 20 should be fully functional and testable independently

---

## Phase 23: User Story 21 - UC-21 Make Final Paper Decision (Priority: P1)

**Goal**: UC-21 Make Final Paper Decision

**Independent Test**: The decision for each paper is recorded and communicated to the author

### Tests for User Story 21 (REQUIRED for P1) ⚠️

- [X] T159 [P] [US21] Create contract test in tests/contract/test_decision_record.py
- [X] T160 [P] [US21] Create integration test in tests/integration/test_decision_record.py

### Implementation for User Story 21

- [X] T161 [P] [US21] Create or update Decision model in src/models/decision.py
- [X] T162 [P] [US21] Implement decision_record service in src/services/decision_record_service.py
- [X] T163 [US21] Implement API handler in src/api/decision_record.py
- [X] T164 [US21] Wire API route in src/api/routes.py
- [X] T165 [US21] Implement web handler/page in src/web/decision_record.py
- [X] T166 [US21] Wire web route in src/web/routes.py
- [X] T167 [US21] Add audit logging for decision_record actions in src/services/audit_log.py

**Checkpoint**: User Story 21 should be fully functional and testable independently

---

## Phase 24: User Story 22 - UC-22 Edit Conference Schedule (Priority: P2)

**Goal**: UC-22 Edit Conference Schedule

**Independent Test**: The conference schedule is successfully updated and stored, with conflicts resolved and constraints satisfied

### Implementation for User Story 22

- [X] T168 [P] [US22] Create or update Schedule model in src/models/schedule.py
- [X] T169 [P] [US22] Implement schedule_edit service in src/services/schedule_edit_service.py
- [X] T170 [US22] Implement API handler in src/api/schedule_edit.py
- [X] T171 [US22] Wire API route in src/api/routes.py
- [X] T172 [US22] Implement web handler/page in src/web/schedule_edit.py
- [X] T173 [US22] Wire web route in src/web/routes.py
- [X] T174 [US22] Add audit logging for schedule_edit actions in src/services/audit_log.py

**Checkpoint**: User Story 22 should be fully functional and testable independently

---

## Phase 25: User Story 23 - UC-23 Generate Conference Schedule (Priority: P2)

**Goal**: UC-23 Generate Conference Schedule

**Independent Test**: A valid conference schedule is generated, stored, and made available for review and further editing

### Implementation for User Story 23

- [X] T175 [P] [US23] Create or update Schedule model in src/models/schedule.py
- [X] T176 [P] [US23] Implement schedule_generate service in src/services/schedule_generate_service.py
- [X] T177 [US23] Implement API handler in src/api/schedule_generate.py
- [X] T178 [US23] Wire API route in src/api/routes.py
- [X] T179 [US23] Implement web handler/page in src/web/schedule_generate.py
- [X] T180 [US23] Wire web route in src/web/routes.py
- [X] T181 [US23] Add audit logging for schedule_generate actions in src/services/audit_log.py

**Checkpoint**: User Story 23 should be fully functional and testable independently

---

## Phase 26: User Story 24 - UC-24 Modify Generated Conference Schedule (Priority: P2)

**Goal**: UC-24 Modify Generated Conference Schedule

**Independent Test**: The conference schedule is successfully modified, validated, and stored, reflecting real-world constraints

### Implementation for User Story 24

- [X] T182 [P] [US24] Create or update Schedule model in src/models/schedule.py
- [X] T183 [P] [US24] Implement schedule_modify service in src/services/schedule_modify_service.py
- [X] T184 [US24] Implement API handler in src/api/schedule_modify.py
- [X] T185 [US24] Wire API route in src/api/routes.py
- [X] T186 [US24] Implement web handler/page in src/web/schedule_modify.py
- [X] T187 [US24] Wire web route in src/web/routes.py
- [X] T188 [US24] Add audit logging for schedule_modify actions in src/services/audit_log.py

**Checkpoint**: User Story 24 should be fully functional and testable independently

---

## Phase 27: User Story 25 - UC-25 Publish Final Conference Schedule (Priority: P2)

**Goal**: UC-25 Publish Final Conference Schedule

**Independent Test**: The final conference schedule is published and accessible, and authors and attendees are notified

### Implementation for User Story 25

- [X] T189 [P] [US25] Create or update Schedule model in src/models/schedule.py
- [X] T190 [P] [US25] Implement schedule_publish service in src/services/schedule_publish_service.py
- [X] T191 [US25] Implement API handler in src/api/schedule_publish.py
- [X] T192 [US25] Wire API route in src/api/routes.py
- [X] T193 [US25] Implement web handler/page in src/web/schedule_publish.py
- [X] T194 [US25] Wire web route in src/web/routes.py
- [X] T195 [US25] Add audit logging for schedule_publish actions in src/services/audit_log.py

**Checkpoint**: User Story 25 should be fully functional and testable independently

---

## Phase 28: User Story 26 - UC-26 Register for Conference (Priority: P1)

**Goal**: UC-26 Register for Conference

**Independent Test**: The attendee is successfully registered for the conference and proceeds to payment or confirmation

### Tests for User Story 26 (REQUIRED for P1) ⚠️

- [X] T196 [P] [US26] Create contract test in tests/contract/test_conference_register.py
- [X] T197 [P] [US26] Create integration test in tests/integration/test_conference_register.py

### Implementation for User Story 26

- [X] T198 [P] [US26] Create or update ConferenceRegistration model in src/models/conferenceregistration.py
- [X] T199 [P] [US26] Implement conference_register service in src/services/conference_register_service.py
- [X] T200 [US26] Implement API handler in src/api/conference_register.py
- [X] T201 [US26] Wire API route in src/api/routes.py
- [X] T202 [US26] Implement web handler/page in src/web/conference_register.py
- [X] T203 [US26] Wire web route in src/web/routes.py
- [X] T204 [US26] Add audit logging for conference_register actions in src/services/audit_log.py

**Checkpoint**: User Story 26 should be fully functional and testable independently

---

## Phase 29: User Story 27 - UC-27 Pay Conference Registration Fee (Priority: P1)

**Goal**: UC-27 Pay Conference Registration Fee

**Independent Test**: The registration fee is successfully paid, and the attendee’s participation is confirmed

### Tests for User Story 27 (REQUIRED for P1) ⚠️

- [X] T205 [P] [US27] Create contract test in tests/contract/test_registration_payment.py
- [X] T206 [P] [US27] Create integration test in tests/integration/test_registration_payment.py

### Implementation for User Story 27

- [X] T207 [P] [US27] Create or update Payment model in src/models/payment.py
- [X] T208 [P] [US27] Implement registration_payment service in src/services/registration_payment_service.py
- [X] T209 [US27] Implement API handler in src/api/registration_payment.py
- [X] T210 [US27] Wire API route in src/api/routes.py
- [X] T211 [US27] Implement web handler/page in src/web/registration_payment.py
- [X] T212 [US27] Wire web route in src/web/routes.py
- [X] T213 [US27] Add audit logging for registration_payment actions in src/services/audit_log.py

**Checkpoint**: User Story 27 should be fully functional and testable independently

---

## Phase 30: User Story 28 - UC-28 Receive Payment Confirmation Ticket (Priority: P2)

**Goal**: UC-28 Receive Payment Confirmation Ticket

**Independent Test**: The attendee receives a payment confirmation ticket that can be viewed or saved as proof of registration

### Implementation for User Story 28

- [X] T214 [P] [US28] Create or update ConfirmationTicket model in src/models/confirmationticket.py
- [X] T215 [P] [US28] Implement payment_confirmation service in src/services/payment_confirmation_service.py
- [X] T216 [US28] Implement API handler in src/api/payment_confirmation.py
- [X] T217 [US28] Wire API route in src/api/routes.py
- [X] T218 [US28] Implement web handler/page in src/web/payment_confirmation.py
- [X] T219 [US28] Wire web route in src/web/routes.py

**Checkpoint**: User Story 28 should be fully functional and testable independently

---

## Phase 31: User Story 29 - UC-29 View Conference Schedule (Priority: P3)

**Goal**: UC-29 View Conference Schedule

**Independent Test**: The attendee successfully views the published conference schedule

### Implementation for User Story 29

- [X] T220 [P] [US29] Create or update Schedule model in src/models/schedule.py
- [X] T221 [P] [US29] Implement schedule_view_attendee service in src/services/schedule_view_attendee_service.py
- [X] T222 [US29] Implement API handler in src/api/schedule_view_attendee.py
- [X] T223 [US29] Wire API route in src/api/routes.py
- [X] T224 [US29] Implement web handler/page in src/web/schedule_view_attendee.py
- [X] T225 [US29] Wire web route in src/web/routes.py

**Checkpoint**: User Story 29 should be fully functional and testable independently

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T226 Documentation updates in docs/ and specs/001-uc-spec-union/quickstart.md
- [X] T227 Code cleanup and refactoring in src/
- [X] T228 Performance optimization across all stories in src/services/
- [X] T229 Security hardening review in src/services/auth_service.py
- [X] T230 Finalize UAT index content in specs/001-uc-spec-union/uat/uat-index.md
- [X] T231 Run quickstart validation steps in specs/001-uc-spec-union/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **P1 Stories**: US4, US6, US8, US9, US10, US16, US18, US21, US26, US27
- **P2 Stories**: US5, US7, US11, US12, US13, US14, US15, US17, US19, US20, US22, US23, US24, US25, US28
- **P3 Stories**: US1, US2, US3, US29
- P2 stories depend on P1 foundations where applicable (auth, submissions, reviews, payments)
- P3 stories can be delivered after foundational setup, independent of P1 business workflows

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories can run in parallel per story
- Within each story, model and service tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
Task: "Create or update Announcement model in src/models/announcement.py"
Task: "Implement announcements service in src/services/announcements_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add P1 user stories in priority order → Test independently
4. Add P2 user stories → Test independently
5. Add P3 user stories → Test independently
