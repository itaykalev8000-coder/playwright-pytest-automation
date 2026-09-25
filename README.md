# Playwright + pytest Test Automation

UI and API test automation in Python, built with Playwright and pytest.

- UI tests run against [SauceDemo](https://www.saucedemo.com), a demo e-commerce site: login, product sorting, cart and checkout.
- API tests run against the public [Automation Exercise API](https://automationexercise.com/api_list): products, search and user accounts.

## Tech stack

Python, Playwright, pytest, Allure, GitHub Actions

## Project structure

```
pages/          Page Object Model classes for the SauceDemo screens
api_client/     Small client for the Automation Exercise API
tests/ui/       Browser tests
tests/api/      API tests
utils/          Test data and helpers
```

## Running locally

```bash
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                  # all tests
pytest -m smoke         # smoke only
pytest tests/api        # API only
pytest --headed         # see the browser while tests run
```

### Allure report

Results are saved to `allure-results`. To open the report you need the [Allure CLI](https://allurereport.org):

```bash
allure serve allure-results
```

UI tests that fail attach a screenshot to the report.

## CI

Every push to `main` and every pull request runs all the tests on GitHub Actions. The Allure results are uploaded as an artifact, and when something fails the Playwright traces are uploaded too (open them with `playwright show-trace`).

## Notes

- The Automation Exercise API returns HTTP 200 even for errors, and the real status code is in the JSON body (`responseCode`). The tests assert on the body, and the client fails right away if the HTTP status itself is not 200.
- `problem_user` on SauceDemo has a sorting bug on purpose, so that test is marked `xfail` rather than skipped.
- The account tests create their own user with a random email and delete it at the end, so they don't depend on existing data.

## Next steps

- Tests for the brands API
- Publish the Allure report to GitHub Pages
- Run the UI tests on Firefox and WebKit as well
