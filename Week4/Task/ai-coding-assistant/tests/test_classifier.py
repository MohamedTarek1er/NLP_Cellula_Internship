from app.Intent_Classifier.classifier import Intent, classify_intent

def test_explain_existing_code():
    result = classify_intent(
        "Explain what this Python function does."
    )
    assert result == Intent.EXPLAIN

def test_generate_new_code():
    
    result = classify_intent(
        "Write a Python function that sorts a list."
    )
    assert result == Intent.GENERATE

def test_explain_programming_error():
    
    result = classify_intent(
        "Why does this loop produce an IndexError?"
    )
    assert result == Intent.EXPLAIN

def test_generate_machine_learning_model():
    result = classify_intent(
        "Create a CNN model for image classification."
    )
    assert result == Intent.GENERATE

def test_empty_query():
    import pytest

    with pytest.raises(ValueError):
        classify_intent("   ")
