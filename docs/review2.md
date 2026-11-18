# Review 2 — First Working Slice

## 1. Project Overview

**Project:** AI Prompt Lab — Student Prompt Experimentation Tool

**Tagline:** Experiment with prompts. Compare results. Learn what works.

AI Prompt Lab is a web application that allows students to record AI prompts, save the responses they receive, and evaluate those responses based on relevance, clarity, and completeness.

The goal of the first working slice is to provide a functional account workflow and one useful core interaction: evaluating and saving an AI prompt experiment.

### Technology Stack

- **Language:** Python 3.12
- **Backend:** Flask
- **Database:** SQLite
- **Database Management:** Flask-SQLAlchemy
- **Authentication:** Flask-Login
- **Password Security:** Werkzeug password hashing
- **Frontend:** HTML, CSS, Bootstrap 5
- **Testing:** pytest

## 2. User Stories

The following user stories describe the main needs of the application's intended users.

1. **Account Creation:** As a new student, I want to create an account so I can save my experiments.

2. **Sign-In:** As a registered student, I want to sign in so I can access my experiments securely.

3. **Evaluate Responses:** As a student, I want to enter a prompt and its AI response so I can evaluate the quality of the results.

4. **Save Experiments:** As a student, I want to save my experiments with ratings and notes so I can revisit what I learned.

5. **Sign-Out:** As a student, I want to sign out so my account isn't left accessible on a shared computer.

## 3. Audience and Presentation Approach

### Target Audience

The primary audience is students who use AI tools for academic work, experimentation, and learning.

The application is designed to help students reflect on the quality of AI-generated responses and understand how different prompts can influence results.

### Presentation Approaches Considered

**Option A: Academic Workspace**

- Clean and organized layout.
- Clear navigation and readable typography.
- Structured forms and evaluation components.
- Focus on usability and productivity.

**Option B: Creative AI Lab**

- Dark backgrounds and expressive colors.
- Purple and violet accents.
- More experimental, technology-focused atmosphere.

### Selected Approach: Hybrid Design

The selected design combines the structured layout of Option A with the color palette and atmosphere of Option B.

The interface will use a clean academic workspace layout with deep navy and purple backgrounds, violet highlights, lavender details, and teal accents.

This approach balances usability with a creative visual identity appropriate for an AI experimentation tool.

### Proposed Color Palette

- Deep navy: `#17152D`
- Dark purple: `#292044`
- Violet: `#7656D6`
- Lavender: `#A78BFA`
- Teal: `#38C6B0`

## 4. Implemented Functionality

The first working slice includes:

- Account registration with username, email, and password.
- Sign-in and sign-out functionality.
- Password hashing for account security.
- Protected experiment pages that require authentication.
- An experiment form for entering a title, prompt, and AI response.
- Three evaluation criteria: relevance, clarity, and completeness.
- Automatic calculation of an overall evaluation score.
- Saving experiments in an SQLite database and associating them with the signed-in user.

## 5. Application Architecture

The application uses a three-layer architecture.

### Frontend

- HTML templates provide the application's pages.
- Bootstrap provides responsive layouts and styling.
- Forms collect account information and experiment data.
- Flash messages communicate validation results and successful actions.

### Backend

- Python and Flask handle application logic and routing.
- Flask-Login manages authentication and protected pages.
- Werkzeug provides password hashing and verification.
- The evaluation module handles scoring calculations.

### Database

- SQLite stores user accounts and experiments.
- SQLAlchemy manages database models and queries.
- Each experiment is associated with the user who created it.

### Application Structure

The application separates responsibilities into modules:

- `app/__init__.py`: Application setup and configuration.
- `app/auth.py`: Registration, sign-in, and sign-out.
- `app/experiments.py`: Experiment creation and validation.
- `app/evaluation.py`: Evaluation scoring strategies.
- `app/models.py`: User and experiment database models.
- `app/templates/`: HTML pages.
- `tests/`: Automated application tests.

## 6. Design Pattern Experiment

### Approaches Compared

**Approach A: Simple Function**

The first approach calculates the average of the three evaluation scores directly.

Advantages:

- Simple to implement.
- Easy to understand.
- Appropriate when only one scoring method is needed.

Disadvantages:

- Becomes less flexible if additional scoring methods are introduced.
- Scoring logic can become harder to manage as requirements grow.

**Approach B: Strategy Pattern**

The second approach separates scoring methods into individual strategies that share a common interface.

Two strategies were implemented:

- `EqualWeightStrategy`: Gives relevance, clarity, and completeness equal importance.
- `RelevanceFocusedStrategy`: Gives relevance 50% importance and clarity and completeness 25% each.

Advantages:

- Scoring methods are separated from the main experiment workflow.
- New scoring methods can be added without rewriting the experiment route.
- Each strategy can be tested independently.

### Results

Using example scores of relevance = 5, clarity = 4, and completeness = 3:

| Approach | Overall Score |
|---|---:|
| Simple Function | 4.00 |
| Equal Weight Strategy | 4.00 |
| Relevance-Focused Strategy | 4.25 |

### Decision

The Equal Weight Strategy was selected as the application's default scoring method.

This preserves the original behavior while allowing alternative scoring methods to be introduced later.

The Strategy Pattern provides a useful extension point, although it introduces more code and complexity than the simple function. For this first slice, the equal-weight method remains the most straightforward default.

## 7. Testing and Verification

The application was tested using pytest.

**Automated test result: 13 passed.**

The tests cover:

- Successful account registration.
- Duplicate email rejection.
- Successful sign-in.
- Incorrect password rejection.
- Successful sign-out.
- Blocking signed-out users from protected pages.
- Saving an experiment.
- Associating an experiment with the correct user.
- Rejecting invalid evaluation scores.
- Rejecting missing required fields.
- Testing both scoring approaches and their results.

### Manual Verification

The application was also tested manually through the browser.

A test account was created and used to sign in. An experiment was submitted successfully, and the resulting database record was inspected directly in SQLite.

The saved record contained:

- **Title:** Testing an AI Travel Prompt
- **Relevance:** 5
- **Clarity:** 4
- **Completeness:** 3
- **Overall rating:** 4.0
- **Associated user:** student01

The sign-out workflow was also tested manually. After signing out, attempting to access the protected experiment page redirected the user to the sign-in page.

## 8. AI Assistance Reflection

AI assistance was used to help plan the application structure, explain Flask concepts, develop the authentication and experiment workflows, implement the scoring strategies, and create automated tests.

The code was implemented incrementally, with each major change followed by testing.

The application was tested using pytest and manually through the browser. The saved experiment was also inspected in SQLite to verify that the information was actually persisted.

**What I learned:**

AI assistance can speed up development, but generated code still needs to be understood, reviewed, and tested. Breaking the implementation into smaller steps made it easier to identify and correct problems.

**What I would do differently next time:**

Plan database changes and test database configuration more carefully before modifying existing models. I would also establish the testing workflow earlier to avoid accidentally affecting the development database.

## 9. Review 2 Status and Next Steps

### Completed

- Account registration and authentication.
- Core prompt experiment workflow.
- Evaluation using three criteria.
- Saving experiments in SQLite.
- Sign-out and protected-page access checks.
- Strategy Pattern implementation and comparison.
- Automated tests with 13 passing tests.
- Manual browser and database verification.
- Initial project documentation.

### Remaining

- Verify the latest changes are committed and pushed to GitHub.
- Add the relevant repository, issue, change, and check links to the project update.
- Complete the required Review 2 submission update.

**Next step:** Finalize the Review 2 update and verify the repository evidence before submission.
