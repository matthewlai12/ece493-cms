# Data Model

## Entities

### UserAccount
- Fields: id, email (unique), password_hash, name, role_id, status, created_at, updated_at
- Relationships: Role (many-to-one), Submissions (one-to-many), Reviews (one-to-many)
- Validation: email format, unique email, password strength
- State: active, disabled

### Role
- Fields: id, name (guest, author, referee, chair, admin, attendee)
- Relationships: UserAccount (one-to-many)

### Announcement
- Fields: id, title, body, published_at, is_public

### RegistrationPrice
- Fields: id, category, amount, currency, active_from, active_to

### Schedule
- Fields: id, status (draft, published), published_at
- Relationships: Sessions (one-to-many)

### Session
- Fields: id, schedule_id, title, room, start_time, end_time
- Relationships: Schedule (many-to-one), Submissions (many-to-many)

### Submission
- Fields: id, author_id, title, abstract, status (draft, submitted, accepted, rejected), created_at, updated_at
- Relationships: UserAccount (author), ManuscriptFile (one-to-one), Reviews (one-to-many)

### ManuscriptFile
- Fields: id, submission_id, filename, content_type, size_bytes, storage_key, uploaded_at
- Validation: allowed formats, size limits

### ReviewInvitation
- Fields: id, submission_id, referee_id, status (pending, accepted, rejected), sent_at, responded_at

### Review
- Fields: id, submission_id, referee_id, score, comments, submitted_at, status (draft, submitted)
- Validation: required fields on submit

### Decision
- Fields: id, submission_id, outcome (accept, reject), decided_by, decided_at, notes

### ConferenceRegistration
- Fields: id, attendee_id, status (initiated, paid, confirmed, cancelled), created_at

### Payment
- Fields: id, registration_id, amount, currency, status (pending, paid, declined), provider_ref, processed_at

### ConfirmationTicket
- Fields: id, registration_id, issued_at, delivery_channel, reference_code

## Relationships
- UserAccount -> Role (many-to-one)
- UserAccount -> Submission (one-to-many)
- Submission -> ManuscriptFile (one-to-one)
- Submission -> ReviewInvitation/Review/Decision (one-to-many/one-to-one)
- ReviewInvitation/Review -> UserAccount (referee)
- Schedule -> Session (one-to-many)
- Session <-> Submission (many-to-many)
- ConferenceRegistration -> Payment (one-to-one)
- ConferenceRegistration -> ConfirmationTicket (one-to-one)

## State Transitions
- Submission: draft -> submitted -> accepted/rejected
- ReviewInvitation: pending -> accepted/rejected
- Review: draft -> submitted
- Schedule: draft -> published
- ConferenceRegistration: initiated -> paid -> confirmed (or cancelled)
- Payment: pending -> paid/declined
