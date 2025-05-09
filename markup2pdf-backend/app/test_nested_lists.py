#!/usr/bin/env python
"""
Simple test script to verify nested list rendering in markdown-to-pdf conversion.
"""
import os
from app.services.markdown_service import markdown_service

def test_nested_lists():
    """Test that nested lists are properly handled in the conversion."""
    # Sample markdown with nested lists using 2-space indentation
    markdown_text = """# Nested List Test

* Level 1 Item A
  * Level 2 Item A.1
    * Level 3 Item A.1.1
    * Level 3 Item A.1.2
  * Level 2 Item A.2
* Level 1 Item B
  * Level 2 Item B.1
    * Level 3 Item B.1.1
      * Level 4 Item B.1.1.1
        * Level 5 Item B.1.1.1.1

1. Ordered List Item 1
   1. Nested Ordered Item 1.1
      1. Nested Ordered Item 1.1.1
   2. Nested Ordered Item 1.2
2. Ordered List Item 2
   * Mixed List Item 2.1
     * Mixed List Item 2.1.1

# Problem Requirements List Test

* **Correctness** -
  * histories stay sorted because inputs are strictly increasing;
  * `bisect_right` ensures we choose the greatest `timestamp_prev ≤ timestamp`.
* **Performance** - With ≤ 2 × 10⁵ total calls, worst-case `get` does log₂(10⁵) ≈ 17 steps, far under limits.
* **Memory** - Exactly one copy of each `(timestamp, value)` pair, so **O(total sets)**.
"""

    # Convert to HTML
    html_result = markdown_service.convert_to_html(markdown_text)
    
    # Save the HTML to a file for inspection
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, "nested_lists_test.html"), "w") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Nested List Test</title>
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
    .nested-list[data-level="4"] {
        margin-left: 2.5em !important;
    }
    .nested-list[data-level="5"] {
        margin-left: 3em !important;
    }
    </style>
</head>
<body>
""" + html_result + """
</body>
</html>
""")
    
    print(f"HTML output saved to {os.path.join(output_dir, 'nested_lists_test.html')}")
    
    # Print a portion of the processed HTML to verify nested lists are properly formatted
    print("\nHTML Output Preview:")
    preview_lines = html_result.split('\n')[:20]
    for line in preview_lines:
        print(line)
    
    # Check specifically for the Problem Requirements list
    print("\nProblem Requirements List Preview:")
    requirements_start = html_result.find("<h1>Problem Requirements List Test</h1>")
    if requirements_start >= 0:
        requirements_html = html_result[requirements_start:requirements_start+1000]  # Get a reasonable chunk
        for line in requirements_html.split('\n')[:30]:  # Show first 30 lines
            print(line)

if __name__ == "__main__":
    test_nested_lists() 