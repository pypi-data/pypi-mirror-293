from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, computed_field

from promptarchitect.specification import (
    EngineeredPromptSpecification,
    TestSpecificationTypes,
)
from promptarchitect.validation.core import TestCaseOutcome, TestCaseStatus


class TestSpecificationReport(BaseModel):
    test_id: str
    specification: TestSpecificationTypes
    outcomes: List[TestCaseOutcome]

    @computed_field
    @property
    def description(self) -> str:
        return self.specification.description


class PromptFileTestReport(BaseModel):
    """
    Defines the format for a test report for a single file.

    Attributes
    ----------
    file_path : str
        The path to the file
    specification : EngineeredPromptSpecification
        The specification for the file
    passed_tests : int
        The number of tests that passed
    failed_tests : int
        The number of tests that failed
    total_duration : float
        The total duration of the tests
    total_cost : float
        The total cost of the prompts executed in the tests
    """

    date_created: datetime
    specification: EngineeredPromptSpecification
    tests: List[TestSpecificationReport]

    @computed_field
    @property
    def tests_passed(self) -> int:
        return len(
            [
                outcome
                for test in self.tests
                for outcome in test.outcomes
                if outcome.status == TestCaseStatus.PASSED
            ]
        )

    @computed_field
    @property
    def tests_failed(self) -> int:
        return len(
            [
                outcome
                for test in self.tests
                for outcome in test.outcomes
                if outcome.status == TestCaseStatus.FAILED
                or outcome.status == TestCaseStatus.ERROR
            ]
        )

    @computed_field
    @property
    def percentage_passed(self) -> float:
        if self.test_count == 0:
            return 0.0

        return self.tests_passed / self.test_count

    @computed_field
    @property
    def test_count(self) -> int:
        return sum([len(test.outcomes) for test in self.tests])

    @computed_field
    @property
    def total_duration(self) -> float:
        return sum(
            [outcome.duration for test in self.tests for outcome in test.outcomes]
        )

    @computed_field
    @property
    def total_costs(self) -> float:
        return sum(
            outcome.costs.costs for test in self.tests for outcome in test.outcomes
        )


class TestRunMessage(BaseModel):
    level: Literal["warning", "error"]
    message: str


class TestSessionReport(BaseModel):
    files: List[PromptFileTestReport]
    messages: List[TestRunMessage] = []

    @computed_field
    @property
    def tests_failed(self) -> int:
        return sum([file.tests_failed for file in self.files])

    @computed_field
    @property
    def tests_passed(self) -> int:
        return sum([file.tests_passed for file in self.files])

    @computed_field
    @property
    def total_duration(self) -> float:
        return sum([file.total_duration for file in self.files])

    @computed_field
    @property
    def total_costs(self) -> float:
        return sum([file.total_costs for file in self.files])

    @computed_field
    @property
    def files_without_tests(self) -> List[EngineeredPromptSpecification]:
        return [
            file.specification
            for file in self.files
            if not file.specification.has_tests
        ]

    @computed_field
    @property
    def files_with_tests(self) -> List[PromptFileTestReport]:
        return [file for file in self.files if file.specification.has_tests]

    @computed_field
    @property
    def percentage_with_tests(self) -> float:
        if len(self.files) == 0:
            return 0.0

        return len(self.files_with_tests) / len(self.files)


class TestReporter(ABC):
    """Base class for building a test reporter."""

    report_path: str

    def __init__(self, report_path: str):
        """
        Initialize the test reporter.

        Parameters
        ----------
        report_path : str
            The path to the report
        """
        self.report_path = report_path

    @abstractmethod
    def generate_report(
        self,
        prompts: List[EngineeredPromptSpecification],
        test_outcomes: List[TestCaseOutcome],
    ) -> None:
        """
        Generate a test report from the test outcomes in a session.

        Parameters
        ----------
        template_location : str
            The path to the template file
        report_location : str
            The path to the report file
        prompts : List[EngineeredPromptSpecification]
            The prompts that were tested
        test_outcomes : List[TestCaseOutcome]
            The outcomes of the test cases
        """
        raise NotImplementedError()

    @staticmethod
    def _collect_results(
        prompt_specs: List[EngineeredPromptSpecification],
        test_outcomes: List[TestCaseOutcome],
    ) -> TestSessionReport:
        """
        Collect the test results and combine them into a reportable structure.

        Parameters
        ----------
        prompt_specs : List[EngineeredPromptSpecification]
            The specifications for the prompts
        test_outcomes : List[TestCaseOutcome]
            The outcomes of the tests

        Returns
        -------
        TestSessionReport
            The report of the test session
        """
        test_files = []

        for prompt_spec in prompt_specs:
            related_tests = list(
                [
                    test_outcome
                    for test_outcome in test_outcomes
                    if test_outcome.prompt_file == prompt_spec.filename
                ]
            )

            tests = []

            for test_spec_key in prompt_spec.metadata.tests.keys():
                test_spec = prompt_spec.metadata.tests[test_spec_key]

                test = TestSpecificationReport(
                    test_id=test_spec_key,
                    specification=test_spec,
                    outcomes=[
                        test_outcome
                        for test_outcome in related_tests
                        if test_outcome.test_id == test_spec_key
                    ],
                )

                tests.append(test)

            test_files.append(
                PromptFileTestReport(
                    date_created=datetime.now(),
                    specification=prompt_spec,
                    tests=tests,
                )
            )

        return TestSessionReport(
            files=test_files,
        )
