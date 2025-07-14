# fp-admin Documentation

This directory contains the documentation for fp-admin, built using MkDocs Material.

## Structure

```
docs/
├── index.md                    # Main documentation page
├── getting-started/           # Getting started guides
│   ├── installation.md
│   ├── quick-start.md
│   └── core-concepts.md
├── user-guide/               # User guides
│   ├── field-types.md
│   ├── widgets.md
│   ├── admin-models.md
│   ├── authentication.md
│   └── cli-commands.md
├── api/                      # API reference
│   ├── models.md
│   ├── views.md
│   └── apps.md
├── advanced/                 # Advanced topics
│   ├── error-handling.md
│   ├── update-endpoints.md
│   └── custom-fields.md
├── development/              # Development guides
│   ├── contributing.md
│   ├── testing.md
│   └── building.md
├── stylesheets/             # Custom CSS
│   └── extra.css
├── javascripts/             # Custom JavaScript
│   └── mathjax.js
└── requirements.txt         # Documentation dependencies
```

## Local Development

### Prerequisites

- Python 3.12+
- pip or uv

### Installation

```bash
# Install documentation dependencies
pip install -r docs/requirements.txt

# Or using uv
uv pip install -r docs/requirements.txt
```

### Running Locally

```bash
# Start the development server
mkdocs serve

# Build the documentation
mkdocs build

# Deploy to GitHub Pages (if you have access)
mkdocs gh-deploy
```

### Configuration

The documentation is configured in `mkdocs.yml` at the project root. Key features:

- **Material Theme**: Modern, responsive design
- **Search**: Full-text search across all pages
- **Navigation**: Automatic table of contents
- **Code Highlighting**: Syntax highlighting for code blocks
- **Admonitions**: Callouts for notes, warnings, etc.
- **Tabs**: Tabbed content sections
- **MathJax**: Mathematical expressions support
- **Git Integration**: Last updated dates and edit links

## Writing Documentation

### Markdown Extensions

The documentation uses several MkDocs Material extensions:

- **Admonitions**: `!!! note "Title"` for callouts
- **Code Annotations**: `{ .python }` for syntax highlighting
- **Tabs**: `=== "Tab 1"` for tabbed content
- **Footnotes**: `[^1]` for footnotes
- **Task Lists**: `- [ ]` for checkboxes
- **Emojis**: `:smile:` for emoji support

### Code Examples

```markdown
```python
from fp_admin.admin.fields import FieldView

# Example code
field = FieldView.text_field("name", "Name", required=True)
```
```

### Admonitions

```markdown
!!! note "Important Note"
    This is an important note.

!!! warning "Warning"
    This is a warning.

!!! tip "Tip"
    This is a helpful tip.
```

### Tabs

```markdown
=== "Python"
    ```python
    # Python code
    ```

=== "JavaScript"
    ```javascript
    // JavaScript code
    ```
```

## Deployment

### GitHub Pages

The documentation is automatically deployed to GitHub Pages via GitHub Actions:

1. Push changes to the `main` branch
2. GitHub Actions builds the documentation
3. Documentation is deployed to `https://esmairi.github.io/fp-admin/`

### Manual Deployment

```bash
# Build the site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## Contributing

### Adding New Pages

1. Create a new `.md` file in the appropriate directory
2. Add the page to the navigation in `mkdocs.yml`
3. Follow the existing documentation style
4. Test locally with `mkdocs serve`

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots when helpful
- Use admonitions for important notes
- Keep pages focused on a single topic
- Update the navigation when adding pages

### Testing

```bash
# Test the build
mkdocs build

# Test locally
mkdocs serve

# Check for broken links
mkdocs build
grep -r "404" site/
```

## Customization

### CSS Customization

Edit `docs/stylesheets/extra.css` to customize the appearance:

- Code block styling
- Table appearance
- Button styles
- Custom components

### JavaScript Customization

Edit `docs/javascripts/mathjax.js` for MathJax configuration.

### Theme Customization

Modify `mkdocs.yml` to customize:

- Color scheme
- Navigation
- Search behavior
- Social links
- Analytics

## Troubleshooting

### Common Issues

1. **Build Errors**: Check for syntax errors in markdown files
2. **Missing Dependencies**: Run `pip install -r docs/requirements.txt`
3. **Navigation Issues**: Verify page paths in `mkdocs.yml`
4. **Styling Problems**: Check CSS syntax in `extra.css`

### Getting Help

- Check the [MkDocs Material documentation](https://squidfunk.github.io/mkdocs-material/)
- Review existing documentation for examples
- Open an issue for documentation problems
