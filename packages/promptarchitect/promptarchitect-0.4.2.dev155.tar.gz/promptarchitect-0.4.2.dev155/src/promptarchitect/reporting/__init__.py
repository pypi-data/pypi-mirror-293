def create_test_reporter(session_config) -> None:
    """
    Create a test reporter based on the report format.

    Parameters
    ----------
    report_format : str
        The format of the report.
    report_path : PathLike
        The path to the report.

    Returns
    -------
    TestReporter
        The test reporter.
    """

    # We move the imports into this method to break a circular dependency problem in one of our scripts.
    # This is a common pattern in Python where you import modules inside functions to avoid circular dependencies.
    from promptarchitect.reporting.html import HtmlTestReporter
    from promptarchitect.reporting.json import JsonTestReporter

    if session_config.report_format == "html":
        return HtmlTestReporter(
            report_path=session_config.report_path,
            theme=session_config.report_theme,
            template_path=session_config.template_path,
        )
    elif session_config.report_format == "json":
        return JsonTestReporter(session_config.report_path)
    else:
        raise ValueError(f"Unsupported report format: {session_config.report_format}")
