# tests/data/test_cases.py
TEST_CASES = {
    "simple_queries": [
        ("What is 2+2?", "4"),
        ("Hello", "Hello! How can I help you?"),
        ("Goodbye", "Goodbye! Have a great day!")
    ],
    "complex_queries": [
        (
            "Analyze the sentiment of: This product is amazing!",
            "positive"
        ),
        (
            "Summarize: Long text here...",
            "Summary of the text"
        )
    ],
    "edge_cases": [
        ("", "I didn't receive any input."),
        ("🤖" * 100, "I see you've sent many robot emojis."),
        (None, "Invalid input received.")
    ]
}