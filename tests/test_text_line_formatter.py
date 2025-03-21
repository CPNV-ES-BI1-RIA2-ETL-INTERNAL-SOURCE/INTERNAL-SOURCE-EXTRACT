import pytest
from app.core.text_line_formatter import TextLineFormatter
from app.exceptions import EmptyTextError

class TestTextLineFormatter:
    @pytest.fixture
    def text_formatter(self):
        return TextLineFormatter()

    def test_format_valid_text(self, text_formatter):
        input_text = "Line1\nLine2\nLine3"
        result = text_formatter.format_text(input_text)
        assert result == ["Line1", "Line2", "Line3"]

    def test_format_empty_text(self, text_formatter):
        with pytest.raises(EmptyTextError) as exc_info:
            text_formatter.format_text("")
        assert "Empty text input" in str(exc_info.value)
        assert "text" in exc_info.value.details

    def test_format_none_text(self, text_formatter):
        with pytest.raises(EmptyTextError) as exc_info:
            text_formatter.format_text(None)
        assert "Empty text input" in str(exc_info.value)

    def test_format_only_whitespace_text(self, text_formatter):
        with pytest.raises(EmptyTextError) as exc_info:
            text_formatter.format_text("   \n\t\n   ")
        assert "No non-empty lines found in text" in str(exc_info.value)
        assert exc_info.value.details["line_count"] > 0

    def test_format_removes_empty_lines(self, text_formatter):
        input_text = "Line1\n\n\nLine2\n\nLine3"
        result = text_formatter.format_text(input_text)
        assert result == ["Line1", "Line2", "Line3"]

    def test_format_preserves_whitespace_in_lines(self, text_formatter):
        input_text = "Line1\nLine2\t\tTest\nLine3"
        result = text_formatter.format_text(input_text)
        assert result == ["Line1", "Line2\t\tTest", "Line3"]

    def test_format_handles_special_characters(self, text_formatter):
        input_text = "Line1 © ®\nLine2 € £\nLine3 → ←"
        result = text_formatter.format_text(input_text)
        assert len(result) == 3 