import markdown
from pygments.styles import get_style_by_name
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension


class MarkdownService:
    def __init__(self):
        self.markdown_extensions = [
            TableExtension(),
            CodeHiliteExtension(css_class='code-highlight', pygments_style='github-dark')
        ]
    
    def convert_to_html(self, markdown_text: str) -> str:
        """Convert markdown text to HTML"""
        html = markdown.markdown(markdown_text, extensions=self.markdown_extensions)
        
        # Add some basic styling for the HTML output
        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Inter', sans-serif; line-height: 1.4; }}
                table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
                th, td {{ border: 1px solid #ddd; padding: 0.5em; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                pre {{ background-color: #f6f8fa; padding: 1em; overflow: auto; }}
                code {{ font-family: 'Source Code Pro', monospace; }}
                blockquote {{ border-left: 4px solid #ddd; margin-left: 0; padding-left: 1em; color: #666; }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """


# Create a singleton instance
markdown_service = MarkdownService() 