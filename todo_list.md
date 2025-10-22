# Simple Chores App - Technical Debt & Improvement Checklist

## Project Status Overview
**Current Score: 7/10**
**Test Coverage: 78%**
**Last Updated: 2025-10-13**

---

## 🔴 Immediate Priority (Do First)

Critical issues that should be addressed immediately before any deployment or further development.

- [x] **SECURITY: Remove hardcoded database password** - `tests/conftest.py:30` ✅ **COMPLETED 2025-10-13**
  - ~~Remove `'mysql+pymysql://root:LuCkY_2015!@localhost:3306/goodchoicesdb?autocommit=true'`~~
  - ~~Use environment variables or test config file~~
  - Related files: `tests/conftest.py`
  - **Fixed:** Now uses environment variables (USERNAME, PASSWORD, HOSTNAME, DBNAME, TEST_DBNAME)

- [x] **Fix deprecated datetime.utcnow()** - `flask_package/helpers.py:15` ✅ **COMPLETED 2025-10-13**
  - ~~Replace `datetime.utcnow()` with `datetime.now(datetime.UTC)`~~
  - ~~Will break in future Python versions~~
  - Related files: `flask_package/helpers.py`
  - **Fixed:** Changed to `datetime.now(UTC)` with proper imports

- [x] **Remove debug print statement** - `flask_package/routes.py:93` ✅ **COMPLETED 2025-10-13**
  - ~~Remove `print("current_user: ", current_user.username)`~~
  - ~~Use `app.logger.debug()` if needed~~
  - Related files: `flask_package/routes.py`
  - **Fixed:** Replaced with `app.logger.debug(f'Current user: {current_user.username}')`

- [x] **Fix duplicate HTML ID attributes** - `flask_package/templates/index.html:33,39` ✅ **COMPLETED 2025-10-13**
  - ~~Multiple `id="chore_num"` elements (violates HTML standards)~~
  - ~~Use only `name` attribute or make IDs unique with loop index~~
  - Related files: `flask_package/templates/index.html`
  - **Fixed:** Removed all duplicate ID attributes from loop, kept name attributes for form submission

- [x] **Create .env.example file** ✅ **COMPLETED 2025-10-13**
  - ~~Document required environment variables~~
  - ~~Include: `SECRET_KEY`, `USERNAME`, `PASSWORD`, `HOSTNAME`, `DBNAME`~~
  - ~~Add to root directory~~
  - **Fixed:** Created `.env.example` with all required variables and documentation

---

## 🟠 High Priority (Do Soon)

Important issues that affect maintainability, stability, and future development.

### Database & Models

- [x] **Fix SQLAlchemy legacy API** - `flask_package/models.py:11` ✅ **COMPLETED 2025-10-15**
  - ~~Replace `User.query.get(int(user_id))` with `db.session.get(User, int(user_id))`~~
  - ~~Update to SQLAlchemy 2.0 API~~
  - Related files: `flask_package/models.py`
  - **Fixed:** Changed to modern SQLAlchemy 2.0 API - all warnings eliminated from test output

- [ ] **Fix foreign key relationship** - `flask_package/models.py:38`
  - Change `username = db.Column(db.String(255))` to `user_id = db.Column(db.Integer, db.ForeignKey('user.id'))`
  - Add `user = db.relationship('User', backref='chores')`
  - Update all queries in `routes.py` to use `user_id`
  - Related files: `flask_package/models.py`, `flask_package/routes.py`

- [x] **Store feedback in database instead of global list** ✅ **COMPLETED 2025-10-22**
  - ~~Create `Feedback` model in `models.py`~~
  - ~~Remove global `feedback_list = []`~~
  - ~~Update `store_feedback()` to save to database~~
  - ~~Related files: `flask_package/helpers.py`, `flask_package/models.py`, `flask_package/routes.py`~~
  - **Fixed:** Created Feedback model with proper foreign key to User table, generated migration (b1a4f0cc1c5d), updated store_feedback() to use database, removed global list anti-pattern, tested and verified working

- [x] **Add database migrations with Alembic/Flask-Migrate** ✅ **COMPLETED 2025-10-21**
  - ~~Install `Flask-Migrate`~~
  - ~~Initialize migrations: `flask db init`~~
  - ~~Create initial migration: `flask db migrate -m "Initial migration"`~~
  - ~~Add migrations folder to git~~
  - ~~Update README with migration instructions~~
  - **Fixed:** Installed Flask-Migrate 4.1.0, initialized migrations folder, created baseline migration (b33ad6f90a12), successfully tested with `flask db upgrade`

### Error Handling

- [ ] **Add error handling around database operations** - `flask_package/routes.py`
  - Wrap db.session operations in try-except blocks
  - Handle `SQLAlchemyError`, `IntegrityError`, etc.
  - Add user-friendly error messages
  - Log errors appropriately
  - Related files: `flask_package/routes.py`

- [ ] **Add graceful degradation for database failures**
  - Handle connection timeouts
  - Show maintenance page if database unavailable
  - Consider implementing circuit breaker pattern

### Security

- [ ] **Fix hardcoded user in feedback function** - `flask_package/helpers.py:14`
  - Replace `user='chipcorey'` with `current_user.username`
  - Related files: `flask_package/helpers.py`

- [ ] **Fix hardcoded test credentials** - `tests/conftest.py:22`
  - Remove dependency on specific user `ralph.corey.1@gmail.com`
  - Create test users dynamically in fixtures
  - Use test database instead of production
  - Related files: `tests/conftest.py`

### Testing

- [ ] **Complete skipped tests** - `tests/` directory
  - `test_forms.py::test_registration_form` - marked as "incomplete"
  - `test_models.py::test_register_user` - needs better mocking
  - `test_models.py::test_chore` - needs better mocking
  - `test_routes.py::test_new_chore` - needs better mocking
  - `test_routes.py::test_reset` - marked as "incomplete"
  - Related files: `tests/test_forms.py`, `tests/test_models.py`, `tests/test_routes.py`

- [ ] **Create separate test database configuration**
  - Use SQLite in-memory for tests or separate test MySQL database
  - Update `conftest.py` to use test config
  - Ensure tests don't touch production data
  - Related files: `tests/conftest.py`

---

## 🟡 Medium Priority (Plan For)

Improvements that enhance code quality, maintainability, and user experience.

### Code Architecture

- [ ] **Implement RESTful API design** - `flask_package/routes.py:87-135`
  - Split monolithic `index()` route into separate endpoints:
    - `POST /api/chores` - create chore
    - `DELETE /api/chores/<id>` - delete chore
    - `PATCH /api/chores/<id>` - update/complete chore
    - `POST /api/chores/reset` - reset all chores
    - `GET /api/chores` - list chores (already exists as part of index)
  - Related files: `flask_package/routes.py`

- [ ] **Create configuration management system** - `flask_package/__init__.py:17-30`
  - Create `config.py` with Config classes (Development, Production, Testing)
  - Separate dev/test/prod configurations
  - Fix DEBUG vs logger level inconsistency
  - Use `app.config.from_object()`
  - Related files: `flask_package/__init__.py`, new file `config.py`

- [ ] **Fix naming convention inconsistencies**
  - Rename `rmove_chore` to `remove_chore` throughout
  - Standardize all variable/function names to snake_case
  - Related files: `flask_package/routes.py`, `flask_package/templates/index.html`

- [ ] **Create constants file for magic strings/numbers** - New file
  - Create `flask_package/constants.py`
  - Move emoji Unicode values to constants:
    - `EMOJI_PENDING = "\U0001F636"`
    - `EMOJI_HAPPY_LIST = [...]`
  - Move affirmations list to constants
  - Reference constants throughout code
  - Related files: New file `flask_package/constants.py`, `flask_package/helpers.py`, `flask_package/routes.py`

### Code Quality

- [ ] **Add type hints to all functions**
  - Add type hints to `helpers.py` functions
  - Add type hints to `routes.py` functions
  - Add type hints to `forms.py` classes
  - Add type hints to `models.py` classes
  - Related files: All `.py` files in `flask_package/`

- [ ] **Standardize docstring style**
  - Choose format (Google, NumPy, or Sphinx style)
  - Add docstrings to all functions
  - Add docstrings to all classes
  - Include parameter descriptions and return types
  - Related files: All `.py` files

- [ ] **Improve database query efficiency** - `flask_package/routes.py:125-126`
  - Simplify query: `Chore.query.filter_by(username=current_user.username).order_by(Chore.chore_id).all()`
  - Consider eager loading if relationships added
  - Add query performance monitoring
  - Related files: `flask_package/routes.py`

### Features & Functionality

- [ ] **Complete HTMX implementation**
  - Make chore creation use HTMX (currently traditional POST)
  - Make chore completion use HTMX for instant feedback
  - Make chore deletion use HTMX
  - Uncomment and fix register partial in base.html
  - Add HTMX to reset functionality
  - Related files: `flask_package/templates/index.html`, `flask_package/templates/base.html`, `flask_package/routes.py`

- [ ] **Add input validation for chore creation** - `flask_package/routes.py:95-100`
  - Add length validation (min/max)
  - Sanitize input to prevent XSS
  - Add WTForm for chore creation
  - Add client-side validation
  - Related files: `flask_package/routes.py`, `flask_package/forms.py`

- [ ] **Add pagination for chores list** - `flask_package/routes.py:125-126`
  - Implement pagination with Flask-SQLAlchemy's `paginate()`
  - Add page size configuration (default 20-50)
  - Update template to show pagination controls
  - Related files: `flask_package/routes.py`, `flask_package/templates/index.html`

- [ ] **Improve emoji/status storage method** - `flask_package/models.py:36`
  - Consider using enum for status (pending/completed)
  - Store emoji preference separately
  - Add `status` field and `completed_emoji` field
  - Migrate existing data
  - Related files: `flask_package/models.py`, `flask_package/routes.py`

### Security

- [ ] **Implement rate limiting**
  - Install `Flask-Limiter`
  - Add rate limiting to login route (5 attempts per minute)
  - Add rate limiting to registration (3 per hour per IP)
  - Add rate limiting to feedback submission
  - Related files: `flask_package/__init__.py`, `flask_package/routes.py`

- [ ] **Add HTTPS enforcement and secure cookies**
  - Configure HTTPS redirect in production
  - Set `SESSION_COOKIE_SECURE = True`
  - Set `SESSION_COOKIE_HTTPONLY = True`
  - Set `SESSION_COOKIE_SAMESITE = 'Lax'`
  - Related files: `flask_package/__init__.py`, `config.py`

- [ ] **Configure session timeout**
  - Set `PERMANENT_SESSION_LIFETIME`
  - Implement session refresh on activity
  - Add "remember me" functionality properly
  - Related files: `flask_package/__init__.py`

### User Experience

- [ ] **Add confirmation dialogs for destructive actions**
  - Add JavaScript confirm for "Remove Chore"
  - Add confirm for "Reset All Chores"
  - Consider using Bootstrap modals for better UX
  - Related files: `flask_package/templates/index.html`

- [ ] **Improve flash message styling** - `flask_package/templates/base.html:54-64`
  - Add category support (success, error, warning, info)
  - Use Bootstrap alert classes
  - Update all `flash()` calls to include category
  - Add auto-dismiss for messages
  - Related files: `flask_package/templates/base.html`, all files with `flash()` calls

- [ ] **Improve accessibility**
  - Add ARIA labels to all form inputs
  - Change button text from "+" to "Mark Complete" (with aria-label)
  - Change button text from "x" to "Remove" (with aria-label)
  - Add alt text context to logo image
  - Test with screen reader
  - Related files: `flask_package/templates/index.html`, `flask_package/templates/base.html`

---

## 🟢 Nice to Have (Future Enhancements)

Lower priority improvements that would enhance the project but aren't critical.

### Documentation

- [ ] **Create comprehensive API documentation**
  - Document all routes and endpoints
  - Include request/response examples
  - Add authentication requirements
  - Consider using Swagger/OpenAPI

- [ ] **Add database schema documentation**
  - Create ER diagram
  - Document all tables and relationships
  - Include field descriptions and constraints
  - Add to docs folder

- [ ] **Create deployment guide**
  - Document PythonAnywhere deployment steps
  - Include environment setup instructions
  - Add database migration steps
  - Document environment variables

- [ ] **Add contribution guidelines**
  - Create `CONTRIBUTING.md`
  - Include code style guide
  - Document testing requirements
  - Add PR template

- [ ] **Update README.md**
  - Fix app name inconsistency (Good Choices vs Simple Chores)
  - Update feature list
  - Add screenshots
  - Include setup instructions
  - Add badges for build status, coverage

### Performance

- [ ] **Implement caching strategy**
  - Install `Flask-Caching`
  - Cache static assets with versioning
  - Consider caching user chores list
  - Add cache invalidation on updates
  - Related files: `flask_package/__init__.py`

- [ ] **Configure database connection pooling** - `flask_package/__init__.py:28`
  - Set `SQLALCHEMY_POOL_SIZE`
  - Configure `SQLALCHEMY_MAX_OVERFLOW`
  - Monitor pool usage
  - Related files: `flask_package/__init__.py`

- [ ] **Add static asset optimization**
  - Minify CSS/JS files
  - Implement asset bundling
  - Add compression middleware
  - Consider CDN for Bootstrap/jQuery

### Testing

- [ ] **Add integration tests for user flows**
  - Test complete registration → login → create chore → complete → logout flow
  - Test edge cases and error scenarios
  - Add tests for concurrent users
  - Related files: New file `tests/test_integration.py`

- [ ] **Increase test coverage to 90%+**
  - Add tests for error handling paths
  - Test validation edge cases
  - Test authentication edge cases
  - Related files: All files in `tests/`

- [ ] **Add end-to-end tests**
  - Use Selenium or Playwright
  - Test complete user workflows in browser
  - Test responsive design
  - Test accessibility

### Features from README

- [ ] **Add profile page** (from Future Features in README)
  - Create profile route and template
  - Allow users to update email, password
  - Add profile image upload
  - Show account statistics (chores completed, etc.)

- [ ] **Add stopwatch and timer page** (from Future Features in README)
  - Create new route `/tools`
  - Implement stopwatch with JavaScript
  - Implement countdown timer
  - Make it work offline with service worker

- [ ] **Make mobile-first responsive** (from Future Features in README)
  - Redesign CSS with mobile-first approach
  - Test on various device sizes
  - Improve touch targets
  - Optimize for mobile performance

- [ ] **Add parent/child profiles** (from Future Features in README)
  - Create `Profile` or `Family` model
  - Allow parent account to add children
  - Separate child login (simple PIN?)
  - Parent dashboard to view all children's chores

- [ ] **Integrate Claude API for affirmations** (from Future Features in README)
  - Sign up for Anthropic API key
  - Create affirmation generation function
  - Cache generated affirmations
  - Add fallback to current random list
  - Related files: `flask_package/helpers.py`

- [ ] **Add scoring/rewards system** (from Future Features in README)
  - Add `points` field to `Chore` model
  - Track points earned per user
  - Create rewards catalog
  - Add leaderboard
  - Allow parent to set rewards

### Code Quality

- [ ] **Add pre-commit hooks**
  - Install `pre-commit`
  - Add hooks for pylint, black, isort
  - Add hook to prevent committing secrets
  - Add to `.pre-commit-config.yaml`

- [ ] **Set up CI/CD pipeline**
  - Create GitHub Actions workflow
  - Run tests on every PR
  - Check code coverage
  - Run linting
  - Auto-deploy to PythonAnywhere on merge to main

- [ ] **Add code formatting with Black**
  - Install and configure Black
  - Format all existing code
  - Add to pre-commit hooks

---

## 📊 Progress Tracking

### Summary by Category

| Category | Total | Completed | In Progress | Remaining |
|----------|-------|-----------|-------------|-----------|
| 🔴 Immediate | 5 | 5 | 0 | 0 |
| 🟠 High Priority | 13 | 3 | 0 | 10 |
| 🟡 Medium Priority | 18 | 0 | 0 | 18 |
| 🟢 Nice to Have | 23 | 0 | 0 | 23 |
| **TOTAL** | **59** | **8** | **0** | **51** |

### Completion Tracking

- **Overall Progress**: 13.6% (8/59 items completed)
- **Immediate Priority**: 100% (5/5 completed) ✅ **SPRINT 1 COMPLETE!**
- **High Priority**: 23.1% (3/13 completed) - Sprint 2 in progress!
- **Medium Priority**: 0% (0/18 completed)
- **Nice to Have**: 0% (0/23 completed)

---

## 🎯 Recommended Sprint Plan

### Sprint 1: Critical Fixes (Week 1)
Focus on all 🔴 Immediate Priority items + security items from 🟠 High Priority
- Remove hardcoded secrets
- Fix deprecated APIs
- Clean up debug code
- Fix HTML issues
- Create .env.example

### Sprint 2: Database & Models (Week 2-3)
Focus on database-related 🟠 High Priority items
- Fix foreign key relationships
- Add migrations
- Store feedback in DB
- Update all queries

### Sprint 3: Testing & Error Handling (Week 4)
Focus on testing and stability
- Complete skipped tests
- Add error handling
- Create test database config
- Increase coverage

### Sprint 4: Code Quality & Architecture (Week 5-6)
Focus on 🟡 Medium Priority code improvements
- Refactor to RESTful design
- Add type hints
- Create configuration management
- Add constants file

### Sprint 5: User Experience (Week 7)
Focus on UX improvements
- Complete HTMX implementation
- Add confirmation dialogs
- Improve accessibility
- Better error messages

### Sprint 6: Security & Performance (Week 8)
Focus on remaining 🟡 Medium Priority security items
- Rate limiting
- HTTPS enforcement
- Session security
- Basic caching

### Future Sprints: Nice to Have
Work through 🟢 Nice to Have items based on priority and user feedback

---

## 📝 Notes

- Update progress percentages as items are completed
- Mark items as complete with `[x]` in the checkbox
- Add notes and dates when items are completed
- Review and reprioritize quarterly
- Link related pull requests or commits next to completed items

---

## 🔗 Related Documents

- [README.md](README.md) - Project overview and features
- [simple_chores_idea.md](simple_chores_idea.md) - Product strategy and ideas framework
- [requirements.txt](requirements.txt) - Python dependencies
- Test files in [tests/](tests/) directory
- Application code in [flask_package/](flask_package/) directory

---

**Last Review Date**: 2025-10-22
**Next Review Date**: 2026-01-22 (Quarterly)
**Reviewer**: Code Review Analysis / Sprint 2 Update
