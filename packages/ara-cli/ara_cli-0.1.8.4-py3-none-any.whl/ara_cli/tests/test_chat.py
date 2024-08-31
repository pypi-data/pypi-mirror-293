import pytest
import tempfile
from ara_cli.chat import Chat


@pytest.fixture
def temp_chat_file():
    """Fixture to create a temporary chat file."""
    temp_file = tempfile.NamedTemporaryFile(delete=True, mode='w+', encoding='utf-8')
    yield temp_file
    temp_file.close()


@pytest.mark.parametrize("lines, expected", [
    (["This is a line.", "Another line here.", "Yet another line."], None),
    (["This is a line.", "# ara prompt:", "Another line here."], "# ara prompt:"),
    (["This is a line.", "# ara prompt:", "Another line here.", "# ara response:"], "# ara response:"),
    (["This is a line.", "  # ara prompt:  ", "Another line here.", "  # ara response:   "], "# ara response:"),
    (["# ara prompt:", "# ara response:"], "# ara response:"),
    (["# ara response:", "# ara prompt:", "# ara prompt:", "# ara response:"], "# ara response:"),
])
def test_get_last_role_marker(lines, expected):
    assert Chat.get_last_role_marker(lines=lines) == expected


@pytest.mark.parametrize("initial_content, expected_content", [
    (["This is a line.\n", "Another line here.\n", "Yet another line.\n"],
     ["This is a line.\n", "Another line here.\n", "Yet another line.\n", "\n", "# ara prompt:"]),

    (["This is a line.\n", "# ara prompt:\n", "Another line here.\n"],
     ["This is a line.\n", "# ara prompt:\n", "Another line here.\n"]),

    (["This is a line.\n", "# ara prompt:\n", "Another line here.\n", "# ara response:\n"],
     ["This is a line.\n", "# ara prompt:\n", "Another line here.\n", "# ara response:\n", "\n", "# ara prompt:"]),

    (["This is a line.\n", "  # ara prompt:  \n", "Another line here.\n", "  # ara response:   \n"],
     ["This is a line.\n", "  # ara prompt:  \n", "Another line here.\n", "  # ara response:   \n", "\n", "# ara prompt:"]),

    (["# ara prompt:\n", "# ara response:\n"],
     ["# ara prompt:\n", "# ara response:\n", "\n", "# ara prompt:"]),

    (["# ara response:\n", "# ara prompt:\n", "# ara prompt:\n", "# ara response:\n"],
     ["# ara response:\n", "# ara prompt:\n", "# ara prompt:\n", "# ara response:\n", "\n", "# ara prompt:"]),
])
def test_add_prompt_tag_if_needed(temp_chat_file, initial_content, expected_content):
    # Write the initial content to the temporary file
    temp_chat_file.writelines(initial_content)
    temp_chat_file.flush()

    # Call the function to test
    Chat(temp_chat_file.name, reset=False).add_prompt_tag_if_needed(temp_chat_file.name)

    # Read the file's content after the function call
    with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    assert lines == expected_content
