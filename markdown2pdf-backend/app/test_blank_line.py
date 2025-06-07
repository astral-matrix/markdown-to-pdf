#!/usr/bin/env python
"""
Test script to verify nested lists with blank lines are properly handled.
"""
import os
from app.services.markdown_service import markdown_service

def test_blank_line_in_lists():
    """Test that nested lists with blank lines are properly handled."""
    # Sample markdown with blank line between parent and nested items
    markdown_text = """## Works - No blank line

* **Correctness** -
  * histories stay sorted because inputs are strictly increasing;
  * `bisect_right` ensures we choose the greatest `timestamp_prev ≤ timestamp`.
* **Performance** - With ≤ 2 × 10⁵ total calls, worst-case `get` does log₂(10⁵) ≈ 17 steps, far under limits.
* **Memory** - Exactly one copy of each `(timestamp, value)` pair, so **O(total sets)**.

## Problematic - Blank line after parent item

* **Correctness** —

  * histories stay sorted because inputs are strictly increasing;
  * `bisect_right` ensures we choose the greatest `timestamp_prev ≤ timestamp`.
* **Performance** — With ≤ 2 × 10⁵ total calls, worst-case `get` does log₂(10⁵) ≈ 17 steps, far under limits.
* **Memory** — Exactly one copy of each `(timestamp, value)` pair, so **O(total sets)**.
"""

    # Convert to HTML
    html_result = markdown_service.convert_to_html(markdown_text)
    
    # Save the HTML to a file for inspection
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, "blank_line_test.html"), "w") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Blank Line Test</title>
    <style>
    /* List styling to support proper nesting */
    ul, ol {
        margin: 0.5em 0 0.5em 1em;
        padding-left: 1em;
    }
    ul li, ol li {
        margin-bottom: 0.25em;
    }
    li ul, li ol {
        margin-top: 0.25em;
    }
    .nested-list {
        margin-left: 1em !important;
    }
    /* Add increasing indentation based on nesting level */
    .nested-list[data-level="1"] {
        margin-left: 1em !important;
    }
    .nested-list[data-level="2"] {
        margin-left: 1.5em !important;
    }
    .nested-list[data-level="3"] {
        margin-left: 2em !important;
    }
    </style>
</head>
<body>
""" + html_result + """
</body>
</html>
""")
    
    print(f"HTML output saved to {os.path.join(output_dir, 'blank_line_test.html')}")
    
    # Check both list sections and print them for comparison
    print("\nWorks - No blank line:")
    works_start = html_result.find("<h2>Works - No blank line</h2>")
    if works_start >= 0:
        works_end = html_result.find("<h2>", works_start + 1)
        if works_end == -1:
            works_end = len(html_result)
        works_html = html_result[works_start:works_end]
        print(works_html)
    
    print("\nProblematic - Blank line after parent item:")
    problem_start = html_result.find("<h2>Problematic - Blank line after parent item</h2>")
    if problem_start >= 0:
        problem_html = html_result[problem_start:]
        print(problem_html)

if __name__ == "__main__":
    test_blank_line_in_lists() 