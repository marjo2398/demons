1. Modify `functions.php` to use the logic provided in the task description. The code for `set_language` currently depends on `$_SESSION`, whereas the task snippet clearly describes a new version that relies on `$_COOKIE` and `setcookie`.
2. Add a test suite for `set_language`. Create a file like `tests/test_set_language.php` that includes `functions.php` and executes various test scenarios for `set_language`. It will cover:
   - Happy paths: Valid language from GET, valid language from COOKIE, valid default language.
   - Error/edge cases: Unsupported language falls back to default, empty GET/COOKIE falls back to default.
3. The test suite needs to be executed via PHP CLI directly (e.g. `php tests/test_set_language.php`) and mock DB dependency since testing `set_language` does not require database and it would fail without a configured local DB.
4. Complete pre-commit step to make sure proper testing, verifications, reviews and reflections are done.
5. Submit the change with branch name `testing-improvement-set-language`.
