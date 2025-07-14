# Widgets

This guide covers all available widgets in fp-admin and how to configure them.

## Overview

Widgets are the UI components that render form fields in the admin interface. Each field type supports specific widgets that determine how the field appears and behaves.

## Basic Input Widgets

### Text Widget

Single-line text input for short text.

```python
from fp_admin.admin.fields import FieldView

# Basic text field
FieldView.text_field("name", "Name", required=True)

# With placeholder
FieldView.text_field("username", "Username", placeholder="Enter username")

# With max length
FieldView.text_field("title", "Title", max_length=100)
```

**Configuration Options:**
- `placeholder`: Placeholder text
- `max_length`: Maximum character length
- `min_length`: Minimum character length
- `pattern`: Regex pattern for validation

### Textarea Widget

Multi-line text input for longer content.

```python
# Basic textarea
FieldView.textarea_field("description", "Description")

# With rows
FieldView.textarea_field("content", "Content", rows=10)

# With placeholder
FieldView.textarea_field("notes", "Notes", placeholder="Enter notes here")
```

**Configuration Options:**
- `rows`: Number of visible rows
- `cols`: Number of visible columns
- `placeholder`: Placeholder text
- `max_length`: Maximum character length

### Password Widget

Password input with hidden characters.

```python
# Basic password field
FieldView.password_field("password", "Password")

# With confirmation
FieldView.password_field("password", "Password", confirm=True)
```

**Configuration Options:**
- `confirm`: Show password confirmation field
- `min_length`: Minimum password length
- `pattern`: Password strength pattern

## Number Input Widgets

### Input Widget

Basic numeric input.

```python
# Integer input
FieldView.number_field("age", "Age")

# Float input
FieldView.float_field("price", "Price")

# With min/max values
FieldView.number_field("rating", "Rating", min_value=1, max_value=5)
```

**Configuration Options:**
- `min_value`: Minimum allowed value
- `max_value`: Maximum allowed value
- `step`: Step increment for number input
- `mode`: Input mode ("decimal" for float)

### Slider Widget

Visual slider for numeric values.

```python
# Basic slider
FieldView.slider_field("rating", "Rating", min_value=0, max_value=10)

# With step
FieldView.slider_field("volume", "Volume", min_value=0, max_value=100, step=5)
```

**Configuration Options:**
- `min_value`: Minimum slider value
- `max_value`: Maximum slider value
- `step`: Step increment
- `show_value`: Show current value display

## Boolean Widgets

### Checkbox Widget

Standard checkbox for true/false values.

```python
# Basic checkbox
FieldView.checkbox_field("is_active", "Active")

# With default value
FieldView.checkbox_field("newsletter", "Newsletter", default=True)
```

**Configuration Options:**
- `default`: Default checked state
- `label_position`: Label position ("left", "right")

### Switch Widget

Toggle switch for boolean values.

```python
# Basic switch
FieldView.switch_field("is_published", "Published")

# With custom labels
FieldView.switch_field("status", "Status",
                      true_label="Enabled", false_label="Disabled")
```

**Configuration Options:**
- `true_label`: Label for true state
- `false_label`: Label for false state
- `default`: Default state

### Select Widget

Dropdown for boolean values.

```python
# Boolean select
FieldView.select_field("is_active", "Active",
                      choices=[(True, "Yes"), (False, "No")])
```

## Choice Widgets

### Dropdown Widget

Select dropdown for single choice.

```python
# Basic dropdown
FieldView.choice_field("category", "Category",
                      choices=[("tech", "Technology"), ("lifestyle", "Lifestyle")])

# With default
FieldView.choice_field("status", "Status",
                      choices=status_choices, default="draft")
```

**Configuration Options:**
- `choices`: List of (value, label) tuples
- `default`: Default selected value
- `placeholder`: Placeholder text
- `searchable`: Enable search functionality

### Radio Widget

Radio buttons for single choice.

```python
# Basic radio buttons
FieldView.radio_field("gender", "Gender",
                     choices=[("male", "Male"), ("female", "Female")])

# Horizontal layout
FieldView.radio_field("theme", "Theme",
                     choices=theme_choices, layout="horizontal")
```

**Configuration Options:**
- `choices`: List of (value, label) tuples
- `layout`: Layout direction ("vertical", "horizontal")
- `default`: Default selected value

## Multi-Choice Widgets

### MultiSelect Widget

Multi-select dropdown.

```python
# Basic multi-select
FieldView.multi_choice_field("tags", "Tags",
                            choices=tag_choices, max_selections=5)

# With min/max selections
FieldView.multi_choice_field("roles", "Roles",
                            choices=role_choices,
                            min_selections=1, max_selections=3)
```

**Configuration Options:**
- `choices`: List of (value, label) tuples
- `min_selections`: Minimum required selections
- `max_selections`: Maximum allowed selections
- `searchable`: Enable search functionality

### Chips Widget

Chip-style multi-select.

```python
# Basic chips
FieldView.chips_field("skills", "Skills", choices=skill_choices)

# With color coding
FieldView.chips_field("categories", "Categories",
                     choices=category_choices, color_coded=True)
```

**Configuration Options:**
- `choices`: List of (value, label) tuples
- `color_coded`: Use different colors for chips
- `max_selections`: Maximum allowed selections

### ListBox Widget

List box for multi-selection.

```python
# Basic list box
FieldView.listbox_field("permissions", "Permissions",
                       choices=permission_choices)

# With size
FieldView.listbox_field("users", "Users",
                       choices=user_choices, size=10)
```

**Configuration Options:**
- `choices`: List of (value, label) tuples
- `size`: Number of visible options
- `multiple`: Allow multiple selections

## Date/Time Widgets

### Calendar Widget

Date and time picker.

```python
# Date only
FieldView.date_field("birth_date", "Birth Date")

# Date and time
FieldView.datetime_field("event_time", "Event Time")

# Time only
FieldView.time_field("start_time", "Start Time")
```

**Configuration Options:**
- `format`: Date/time format
- `min_date`: Minimum allowed date
- `max_date`: Maximum allowed date
- `show_time`: Show time picker
- `time_only`: Show only time picker

## File Upload Widgets

### Upload Widget

File upload input.

```python
# Basic file upload
FieldView.file_field("document", "Document")

# With file types
FieldView.file_field("image", "Image",
                    accept="image/*", max_size="5MB")

# Multiple files
FieldView.file_field("attachments", "Attachments", multiple=True)
```

**Configuration Options:**
- `accept`: Accepted file types
- `max_size`: Maximum file size
- `multiple`: Allow multiple files
- `upload_dir`: Upload directory

### Image Widget

Image upload with preview.

```python
# Basic image upload
FieldView.image_field("avatar", "Avatar")

# With dimensions
FieldView.image_field("banner", "Banner",
                     max_width=1200, max_height=400)

# With thumbnail
FieldView.image_field("photo", "Photo",
                     thumbnail_size=(150, 150))
```

**Configuration Options:**
- `max_width`: Maximum image width
- `max_height`: Maximum image height
- `thumbnail_size`: Thumbnail dimensions
- `preview`: Show image preview
- `accept`: Accepted image formats

## Relationship Widgets

### Foreign Key Widget

Dropdown for related model selection.

```python
# Basic foreign key
FieldView.foreign_key_field("category_id", "Category", model=Category)

# With custom display
FieldView.foreign_key_field("author_id", "Author",
                           model=User,
                           display_field="username")

# With search
FieldView.foreign_key_field("product_id", "Product",
                           model=Product,
                           searchable=True)
```

**Configuration Options:**
- `model`: Related model class
- `display_field`: Field to display in dropdown
- `searchable`: Enable search functionality
- `placeholder`: Placeholder text

### AutoComplete Widget

Searchable dropdown for relationships.

```python
# Basic autocomplete
FieldView.autocomplete_field("user_id", "User", model=User)

# With custom search
FieldView.autocomplete_field("product_id", "Product",
                            model=Product,
                            search_fields=["name", "description"])

# With minimum characters
FieldView.autocomplete_field("tag_id", "Tag",
                            model=Tag,
                            min_chars=2)
```

**Configuration Options:**
- `model`: Related model class
- `search_fields`: Fields to search in
- `min_chars`: Minimum characters to trigger search
- `display_field`: Field to display
- `placeholder`: Placeholder text

## Advanced Widgets

### JSON Editor Widget

JSON editor with syntax highlighting.

```python
# Basic JSON editor
FieldView.json_field("settings", "Settings")

# With default value
FieldView.json_field("config", "Configuration",
                    default={"theme": "dark", "language": "en"})

# With schema validation
FieldView.json_field("metadata", "Metadata",
                    schema=metadata_schema)
```

**Configuration Options:**
- `default`: Default JSON value
- `schema`: JSON schema for validation
- `editor_type`: Editor type ("monaco", "ace")
- `height`: Editor height

### Color Picker Widget

Color selection widget.

```python
# Basic color picker
FieldView.color_field("theme_color", "Theme Color")

# With default color
FieldView.color_field("primary_color", "Primary Color",
                     default="#007bff")

# With format
FieldView.color_field("accent_color", "Accent Color",
                     format="rgb")
```

**Configuration Options:**
- `default`: Default color value
- `format`: Color format ("hex", "rgb", "hsl")
- `palette`: Custom color palette
- `alpha`: Enable alpha channel

### Rich Text Widget

Rich text editor.

```python
# Basic rich text
FieldView.richtext_field("content", "Content")

# With toolbar
FieldView.richtext_field("description", "Description",
                        toolbar=["bold", "italic", "link"])

# With height
FieldView.richtext_field("body", "Body", height=300)
```

**Configuration Options:**
- `toolbar`: Available toolbar buttons
- `height`: Editor height
- `plugins`: Additional plugins
- `placeholder`: Placeholder text

### Markdown Widget

Markdown editor.

```python
# Basic markdown
FieldView.markdown_field("content", "Content")

# With preview
FieldView.markdown_field("description", "Description",
                        preview=True)

# With height
FieldView.markdown_field("body", "Body", height=400)
```

**Configuration Options:**
- `preview`: Show live preview
- `height`: Editor height
- `toolbar`: Available toolbar buttons
- `placeholder`: Placeholder text

## Custom Widgets

### Creating Custom Widgets

You can create custom widgets by extending the base widget classes:

```python
from fp_admin.admin.fields import FieldView

class CustomWidget(FieldView):
    def __init__(self, name: str, label: str, **kwargs):
        super().__init__(
            name=name,
            label=label,
            field_type="string",
            widget="custom",
            **kwargs
        )

    def get_widget_config(self):
        return {
            "type": "custom",
            "component": "CustomComponent",
            "props": self.get_props()
        }
```

### Widget Configuration

Each widget can be configured with specific options:

```python
# Widget with custom configuration
FieldView(
    name="custom_field",
    label="Custom Field",
    field_type="string",
    widget="custom",
    widget_config={
        "custom_option": "value",
        "another_option": True
    }
)
```

## Widget Best Practices

### 1. Choose Appropriate Widgets

- Use **text** for short, single-line input
- Use **textarea** for longer, multi-line content
- Use **dropdown** for single selection from many options
- Use **radio** for single selection from few options
- Use **multiSelect** for multiple selections
- Use **switch** for boolean toggles
- Use **slider** for numeric ranges

### 2. Provide Good Defaults

```python
# Good: Provide sensible defaults
FieldView.switch_field("is_active", "Active", default=True)
FieldView.choice_field("status", "Status",
                      choices=status_choices, default="draft")
```

### 3. Use Validation

```python
# Good: Add validation
FieldView.text_field("email", "Email",
                    pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
FieldView.number_field("age", "Age",
                      min_value=0, max_value=120)
```

### 4. Consider User Experience

```python
# Good: Add helpful placeholders and labels
FieldView.text_field("username", "Username",
                    placeholder="Enter your username")
FieldView.textarea_field("description", "Description",
                        placeholder="Describe your item...")
```

## Widget Examples

### Complete Form Example

```python
class ProductView(AdminView):
    model = Product
    label = "Products"

    def get_form_fields(self):
        return [
            # Basic information
            FieldView.text_field("name", "Product Name", required=True),
            FieldView.textarea_field("description", "Description"),

            # Pricing
            FieldView.float_field("price", "Price", min_value=0),
            FieldView.choice_field("currency", "Currency",
                                 choices=[("USD", "USD"), ("EUR", "EUR")]),

            # Status
            FieldView.switch_field("is_active", "Active", default=True),
            FieldView.choice_field("status", "Status",
                                 choices=status_choices, default="draft"),

            # Categories
            FieldView.foreign_key_field("category_id", "Category", model=Category),
            FieldView.multi_choice_field("tags", "Tags",
                                       choices=tag_choices, max_selections=5),

            # Media
            FieldView.image_field("image", "Product Image"),
            FieldView.file_field("manual", "User Manual",
                               accept=".pdf,.doc,.docx"),

            # Metadata
            FieldView.json_field("metadata", "Additional Data"),
            FieldView.color_field("brand_color", "Brand Color"),

            # Dates
            FieldView.date_field("release_date", "Release Date"),
            FieldView.datetime_field("last_updated", "Last Updated"),
        ]
```

## Next Steps

- **[Field Types](field-types.md)** - Learn about field types and their capabilities
- **[Admin Models](admin-models.md)** - Configure advanced admin features
- **[Custom Fields](../advanced/custom-fields.md)** - Create custom field types and widgets
