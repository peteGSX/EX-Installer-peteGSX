# EX-Installer

## What This Is

A graphical firmware installation tool for Arduino devices that downloads, extracts, configures, and flashes firmware with a user-friendly interface.

## Core Value

Make Arduino firmware installation simple, reliable, and accessible to all users regardless of technical background.

## Requirements

### Validated

- [ ] ✓ Arduino device detection (existing codebase)
- [ ] ✓ GitHub release downloading (existing codebase)
- [ ] ✓ Serial communication (existing codebase)

### Active

- [ ] **TEST-01**: Unit test infrastructure (pytest with 80%+ coverage)
- [ ] **TEST-02**: Integration tests for CLI workflow
- [ ] **TEST-03**: End-to-end tests for complete user journey
- [ ] **TEST-04**: Performance testing for all operations
- [ ] **TEST-05**: Security testing for input validation
- [ ] **TEST-06**: Accessibility testing for WCAG compliance
- [ ] **TEST-07**: CI/CD pipeline with automated testing
- [ ] **TEST-08**: Platform-specific testing (Windows, macOS, Linux)
- [ ] **TEST-09**: Virtual environment usage enforced in all phases (see ENVIRONMENT.md)

### Out of Scope

- (None yet - will be defined during testing phase)

## Context

**Current Testing State:**
- Zero automated test coverage
- No test infrastructure
- No CI/CD integration
- All testing to be implemented incrementally

**Testing Philosophy:**
- Build test coverage incrementally
- Prioritize critical paths
- Balance all test types (unit, integration, E2E, performance, security)
- Add tests alongside code development
- **Enforce virtual environment usage in all phases and future work**

**Testing Phases:**
- Phase 1 (Week 1): Foundation - pytest infrastructure, 20+ unit tests, CI/CD
- Phase 2 (Weeks 2-3): Integration - cross-module tests, E2E tests, platform testing
- Phase 3 (Weeks 4+): Advanced - performance, security, accessibility, regression

**Balanced Distribution:**
- Unit Tests: 30%
- Integration Tests: 30%
- E2E Tests: 25%
- Performance Tests: 10%
- Security Tests: 5%

**Hard Requirements:**
- Virtual environment must be used for all Python work
- Virtual environment must be activated before running tests
- CI/CD must activate virtual environment before running tests
- All dependencies must be installed from requirements files
- Python 3.13 only
- Tests must pass with virtual environment activated

## Constraints

- **Timeline**: Testing phased over 4+ weeks
- **Effort**: ~190 hours total for complete test suite
- **Quality**: 80%+ coverage on critical modules required
- **CI/CD**: GitHub Actions for automated testing
- **Virtual Environment**: All Python work must use virtual environment (venv/)
- **Python Version**: Python 3.13 only
- **Dependencies**: Must be installed from requirements files
- **Testing Standards**: All phases must follow testing standards including virtual environment requirements

## Testing Standards

**Hard Requirements:**

1. **Virtual Environment Usage**: All Python work must use activated virtual environment
   - Must use `python -m venv venv` to create virtual environment
   - Must activate virtual environment before running any Python commands
   - CI/CD must activate virtual environment before running tests
   - Git must ignore venv/, .venv/, env/, and similar directories

2. **Virtual Environment Creation**: Virtual environment must be created during Phase 1
   - Must use Python 3.13 to match project requirements
   - Must be created in project root as `venv/`
   - Must be committed to git (excluded from .gitignore)

3. **Dependency Installation**: All dependencies must be installed from requirements files
   - Base dependencies: `requirements.txt`
   - Python 3.13 specific: `requirements-python313.txt`
   - Test dependencies: pytest, pytest-cov, pytest-mock, pytest-benchmark

4. **Testing Requirements**: All phases must follow testing standards
   - Virtual environment must be activated before running tests
   - CI/CD must activate virtual environment before running tests
   - Tests must pass with virtual environment activated
   - No phase can be considered complete without virtual environment usage
   - All future development must use virtual environment

5. **Documentation Requirements**: All testing must be properly documented
   - `.planning/codebase/ENVIRONMENT.md` must be created and maintained
   - `requirements.txt` and `requirements-python313.txt` must be kept up to date
   - All test files must be documented
   - CI/CD configuration must document testing procedures

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|----------|
| pytest as test framework | Python standard, good coverage tools | pytest configured |
| Phased testing approach | Manage complexity, deliver incrementally | 3-phase roadmap created |
| Balanced test distribution | Comprehensive coverage, all aspects | Unit/Integration/E2E/Performance/Security |
| GitHub Actions for CI | Platform-native, easy setup | Workflow created |
| Virtual environment | Ensure reproducible, isolated Python environment | venv/ created and enforced |
| Python 3.13 | Matches project requirements | requirements-python313.txt |
| Virtual environment usage | Enforced in all phases and future work | ENVIRONMENT.md created |

---
*Last updated: 2026-05-24 after TESTING.md revision and ROADMAP.md creation*
