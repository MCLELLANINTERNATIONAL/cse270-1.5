import pytest
import json
from build_sentences import (
    get_seven_letter_word,
    parse_json_from_file,
    choose_sentence_structure,
    get_pronoun,
    get_article,
    get_word,
    fix_agreement,
    build_sentence,
    structures
)

def test_get_seven_letter_word(mocker):
    # Test valid input: should return uppercase version
    mocker.patch("builtins.input", return_value="example")
    result = get_seven_letter_word()
    assert result == "EXAMPLE"

    # Test invalid input: fewer than 7 letters should raise ValueError
    mocker.patch("builtins.input", return_value="short")
    with pytest.raises(ValueError):
        get_seven_letter_word()


def test_parse_json_from_file(tmp_path):
    # Create a temporary JSON file with known test data
    test_data = {
        "adjectives": ["big"],
        "nouns": ["cat"],
        "verbs": ["runs"],
        "adverbs": ["quickly"],
        "prepositions": ["over"]
    }

    file_path = tmp_path / "test_words.json"
    with open(file_path, "w") as file:
        json.dump(test_data, file)

    # Parse the JSON file and verify the result
    result = parse_json_from_file(file_path)
    assert result == test_data


def test_choose_sentence_structure(mocker):
    # Mock random.choice so the outcome is predictable
    mock_choice = mocker.patch("random.choice", return_value=structures[0])

    result = choose_sentence_structure()

    assert result == structures[0]
    mock_choice.assert_called_once_with(structures)


def test_get_pronoun(mocker):
    # Mock random.choice to return a known pronoun
    mock_choice = mocker.patch("random.choice", return_value="he")

    result = get_pronoun()

    assert result == "he"
    mock_choice.assert_called_once()


def test_get_article(mocker):
    # Mock random.choice to return a known article
    mock_choice = mocker.patch("random.choice", return_value="a")

    result = get_article()

    assert result == "a"
    mock_choice.assert_called_once()


def test_get_word():
    # Create a small list where each letter maps to an index
    speech_part = ["apple", "banana", "cat", "dog"]

    # A -> index 0
    assert get_word("A", speech_part) == "apple"


def test_fix_agreement():
    # Rule 1: "he" or "she" adds "s" to the verb two words ahead
    sentence1 = ["he", "quickly", "run"]
    fix_agreement(sentence1)
    assert sentence1 == ["he", "quickly", "runs"]

    sentence2 = ["she", "slowly", "walk"]
    fix_agreement(sentence2)
    assert sentence2 == ["she", "slowly", "walks"]

    # Rule 2: change "a" to "an" if noun two words ahead starts with vowel
    sentence3 = ["a", "big", "apple"]
    fix_agreement(sentence3)
    assert sentence3 == ["an", "big", "apple"]

    # Rule 3: if "the" is first word, add "s" to verb four words ahead
    sentence4 = ["the", "big", "dog", "quickly", "jump"]
    fix_agreement(sentence4)
    assert sentence4 == ["the", "big", "dog", "quickly", "jumps"]


def test_build_sentence(mocker):
    # Structure that exercises every branch in build_sentence
    structure = ["PRO", "ADV", "VERB", "ART", "ADJ", "NOUN", "PREP", "ART", "ADJ", "NOUN"]

    # Seed word supplies letters for ADJ, NOUN, ADV, VERB, PREP
    seed_word = "ABCDEFG"

    # Data lists are arranged so A=0, B=1, C=2, etc.
    data = {
        "adjectives": ["eager", "brave", "calm", "daring", "elegant", "fancy", "gentle"],
        "nouns": ["apple", "bear", "cat", "dog", "eagle", "frog", "goat"],
        "adverbs": ["abruptly", "boldly", "calmly", "daily", "eagerly", "firmly", "gently"],
        "verbs": ["accept", "build", "climb", "dance", "explore", "follow", "gather"],
        "prepositions": ["above", "below", "circa", "during", "except", "from", "given"],
    }

    # Make article and pronoun predictable
    mocker.patch("build_sentences.get_article", return_value="a")
    mocker.patch("build_sentences.get_pronoun", return_value="he")

    result = build_sentence(seed_word, structure, data)

    assert result == "He abruptly builds a calm dog except a fancy goat"