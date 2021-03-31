# This a notebook for the Real Python blog "Effective Python Testing With Pytest".

"""
To install pytest with pip use
!pip install pytest
"""

"""
Most functional tests follow the Arrange-Act-Assert model:

1. Arrange, or set up, the conditions for the test
2. Act by calling some function or method
3. Assert that some end condition is true

Testing frameworks typically hook into your test’s assertions so that they can
provide information when an assertion fails. unittest, for example, provides
a number of helpful assertion utilities out of the box. However, even a small
set of tests requires a fair amount of boilerplate code.

Note! Boilerplate code or just boilerplate are sections of code that are
repeated in multiple places with little or no vatiation.

"""

def test_always_passes():
    assert True

def test_always_fails():
    assert False

"""
Results:
=================================================================== test session starts ===================================================================
platform win32 -- Python 3.8.0, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: D:\Courses\Skillfactory_Data_Science_Degree\module_3\Module_suppl_notebooks
collected 2 items

test_pytest_python.py .F                                                                                                                             [100%]

======================================================================== FAILURES =========================================================================
____________________________________________________________________ test_always_fails ____________________________________________________________________

    def test_always_fails():
>       assert False
E       assert False

test_pytest_python.py:29: AssertionError
================================================================= short test summary info =================================================================
FAILED test_pytest_python.py::test_always_fails - assert False
=============================================================== 1 failed, 1 passed in 0.19s ===============================================================

pytest presents the test results differently than unittest. The report shows:

1. The system state, including which versions of Python, pytest, and any plugins you have installed
2. The rootdir, or the directory to search under for configuration and tests
3. The number of tests the runner discovered

The output then indicates the status of each test using a syntax similar to unittest:

1. A dot (.) means that the test passed.
2. An F means that the test has failed.
3. An E means that the test raised an unexpected exception.
"""

"""
State and Dependency Management

--- A test double is an object that can stand in for a real object in a test,
similar to how a stunt double stands in for an actor in a movie. These are
sometimes all commonly referred to as “mocks”, but it's important to
distinguish between the different types of test doubles since they all have
different uses. The most common types of test doubles are stubs, mocks, and
fakes. ---

pytest takes a different approach. It leads you toward explicit dependency declarations that are still reusable thanks to the availability of fixtures. pytest fixtures are functions that create data or test doubles or initialize some system state for the test suite. Any test that wants to use a fixture must explicitly accept it as an argument, so dependencies are always stated up front.

"""

"""
Test Filtering

As your test suite grows, you may find that you want to run just a few tests on a feature and save the full suite for later. pytest provides a few ways of doing this:

1. Name-based filtering: You can limit pytest to running only those tests whose fully qualified names match a particular expression. You can do this with the -k parameter.
2. Directory scoping: By default, pytest will run only those tests that are in or under the current directory.
3. Test categorization: pytest can include or exclude tests from particular categories that you define. pytest enables you to create marks, or custom labels, for any test you like. You can do this with the -m parameter. A test may have multiple labels, and you can use them for granular control over which tests to run.
"""

"""
Fixtures

pytest fixtures are a way of providing data, test doubles, or state setup to your tests. Fixtures are functions that can return a wide range of values. Each test that depends on a fixture must explicitly accept that fixture as an argument.

"""

def format_data_for_display(people):
    corrected_people = []
    for person in people:
        corrected_people.append(
            f"{person['given_name']} {person['family_name']}: {person['title']}"
        )
    return corrected_people

def test_format_data_for_display():
    people = [
        {
            "given_name": "Alfonsa",
            "family_name": "Ruiz",
            "title": "Senior Software Engineer",
        },
        {
            "given_name": "Sayid",
            "family_name": "Khan",
            "title": "Project Manager",
        },
    ]

    assert format_data_for_display(people) == [
        "Alfonsa Ruiz: Senior Software Engineer",
        "Sayid Khan: Project Manager",
    ]

"""
Now suppose you need to write another function to transform the data into comma-separated values for use in Excel. The test would look awfully similar:
"""

def format_data_for_excel(people):
    corrected_people = []
    corrected_people.append('given,family,title\n')
    for person in people:
        corrected_people.append(
            f"{person['given_name']},{person['family_name']},{person['title']}\n"
        )
    return "".join(corrected_people)

def test_format_data_for_excel():
    people = [
        {
            "given_name": "Alfonsa",
            "family_name": "Ruiz",
            "title": "Senior Software Engineer",
        },
        {
            "given_name": "Sayid",
            "family_name": "Khan",
            "title": "Project Manager",
        },
    ]

    assert format_data_for_excel(people) == """given,family,title
Alfonsa,Ruiz,Senior Software Engineer
Sayid,Khan,Project Manager
"""

# Just create a fixture for the same underlying test data

import pytest

@pytest.fixture
def example_people_data():
    return [
        {
            "given_name": "Alfonsa",
            "family_name": "Ruiz",
            "title": "Senior Software Engineer",
        },
        {
            "given_name": "Sayid",
            "family_name": "Khan",
            "title": "Project Manager",
        },
    ]

# and to use it we need to add it as an argument to the test_pytest_python
# let's rewrite our tests
def test_format_data_for_display_fixture(example_people_data):
    assert format_data_for_display(example_people_data) == [
        "Alfonsa Ruiz: Senior Software Engineer",
        "Sayid Khan: Project Manager",
    ]

def test_format_data_for_excel_fixture(example_people_data):
    assert format_data_for_excel(example_people_data) == """given,family,title
Alfonsa,Ruiz,Senior Software Engineer
Sayid,Khan,Project Manager
"""

"""
Fixtures at Scale

As you extract more fixtures from your tests, you might see that some fixtures could benefit from further extraction. Fixtures are modular, so they can depend on other fixtures. You may find that fixtures in two separate test modules share a common dependency. What can you do in this case?

You can move fixtures from test modules into more general fixture-related modules. That way, you can import them back into any test modules that need them. This is a good approach when you find yourself using a fixture repeatedly throughout your project.

pytest looks for conftest.py modules throughout the directory structure. Each conftest.py provides configuration for the file tree pytest finds it in. You can use any fixtures that are defined in a particular conftest.py throughout the file’s parent directory and in any subdirectories. This is a great place to put your most widely used fixtures.

"""

"""
Marks: Categorizing Tests

Marking tests is useful for categorizing tests by subsystem or dependencies. If some of your tests require access to a database, for example, then you could create a @pytest.mark.database_access mark for them.

When the time comes to run your tests, you can still run them all by default with the pytest command. If you’d like to run only those tests that require database access, then you can use pytest -m database_access. To run all tests except those that require database access, you can use pytest -m "not database_access".

Here are some of the builtin markers:

1. usefixtures - use fixtures on a test function or class
2. filterwarnings - filter certain warnings of a test function
3. skip - always skip a test function
4. skipif - skip a test function if a certain condition is met
5. xfail - produce an “expected failure” outcome if a certain condition is met
6. parametrize - perform multiple calls to the same test function.

"""

"""
Parametrization: Combining Tests

You saw earlier in this tutorial how pytest fixtures can be used to reduce code duplication by extracting common dependencies. Fixtures aren’t quite as useful when you have several tests with slightly different inputs and expected outputs. In these cases, you can parametrize a single test definition, and pytest will create variants of the test for you with the parameters you specify.

Imagine you’ve written a function to tell if a string is a palindrome. An initial set of tests could look like this:
"""

def is_palindrome(string):
    import re
    if len(string) == 0:
        return True
    preprocessed_string = string.replace(' ', '').lower()
    preprocessed_string_reg = re.search(r"\w+", preprocessed_string).group(0)
    if preprocessed_string_reg == preprocessed_string_reg[::-1]:
        return True
    else:
        return False

def test_is_palindrome_empty_string():
    assert is_palindrome("")

def test_is_palindrome_single_character():
    assert is_palindrome("a")

def test_is_palindrome_mixed_casing():
    assert is_palindrome("Bob")

def test_is_palindrome_with_spaces():
    assert is_palindrome("Never odd or even")

def test_is_palindrome_with_punctuation():
    assert is_palindrome("Do geese see God?")

def test_is_palindrome_not_palindrome():
    assert not is_palindrome("abc")

def test_is_palindrome_not_quite():
    assert not is_palindrome("abab")

"""
All of these tests except the last two have the same shape:

def test_is_palindrome_<in some situation>():
    assert is_palindrome("<some string>")

Therefore, we can use @pytest.mark.parametrize() to fill in this shape with different values, reducing your test code significantly:
"""

@pytest.mark.parametrize(
    "palindrome",
    [
        "",
        "a",
        "Bob",
        "Never odd or even",
        "Do geese see God?",
    ]
)
def test_is_palindrome(palindrome):
    assert is_palindrome(palindrome)

@pytest.mark.parametrize(
    "not_palindrome",
    [
        "abc",
        "abab"
    ]
)
def test_is_not_palindrome(not_palindrome):
    assert not is_palindrome(not_palindrome)

"""
The first argument to parametrize() is a comma-delimited string of parameter names that goes into the function as an argument. The second argument is a list of either tuples or single values that represent the parameter value(s). You could take your parametrization a step further to combine all your tests into one:
"""

@pytest.mark.parametrize(
    "string, expected_result",
    [
        ("", True),
        ("a", True),
        ("Bob", True),
        ("Never odd or even", True),
        ("Do geese see God?", True),
        ("abc", False),
        ("abab", False),
    ]
)
def test_is_palindrome(string, expected_result):
    assert is_palindrome(string) == expected_result

"""
Durations Reports and Useful pytest Plugins

We read earlier about using marks to filter out slow tests when you run your suite. If you want to improve the speed of your tests, then it’s useful to know which tests might offer the biggest improvements. pytest can automatically record test durations for you and report the top offenders.

Use the --durations option to the pytest command to include a duration report in your test results. --durations expects an integer value n and will report the slowest n number of tests. The output will follow your test results:

pytest --durations=3 -vv



pytest-randomly

pytest-randomly does something seemingly simple but with valuable effect: It forces your tests to run in a random order. pytest always collects all the tests it can find before running them, so pytest-randomly shuffles that list of tests just before execution.

This is a great way to uncover tests that depend on running in a specific order, which means they have a stateful dependency on some other test. If you built your test suite from scratch in pytest, then this isn’t very likely. It’s more likely to happen in test suites that you migrate to pytest.

The plugin will print a seed value in the configuration description. You can use that value to run the tests in the same order as you try to fix the issue.



pytest-cov

If you measure how well your tests cover your implementation code, you likely use the coverage package. pytest-cov integrates coverage, so you can run pytest --cov to see the test coverage report.


"""
