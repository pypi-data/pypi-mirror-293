from textwrap import dedent
import pytest

def test_import() -> None:
    import amazon_sagemaker_hyperpod  # type: ignore # noqa: F401
