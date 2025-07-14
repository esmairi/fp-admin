# Field Types and Widgets Documentation

## Field Types and Widgets

| **Field Type**  | **Widgets**                       | **Note**                                                             |
|-----------------|-----------------------------------|----------------------------------------------------------------------|
| `string`        | `text`, `textarea`, `password`    | Short or long text, password input                                   |
| `number`        | `input`, `Slider`                 | Whole numbers, optional range with `Slider`                          |
| `float`         | `input`, `Slider`                 | Decimal input with `mode="decimal"`                                  |
| `time`          | `calendar` (`timeOnly`)           | Time-only input (hh\:mm)                                             |
| `datetime`      | `calendar` (`showTime`)           | Combined date and time input                                         |
| `boolean`       | `Checkbox`, `switch`, `select`    | True/false toggle                                                    |
| `choice`        | `dropdown`, `radio`, `select`     | Select one value from a predefined list (enum-like)                  |
| `multichoice`   | `multiSelect`, `chips`, `listBox` | Select multiple values from a list (many-to-many, tags, roles, etc.) |
| `foreignkey`    | `dropdown`, `autoComplete`        | Relation to another model (many-to-one)                              |
| `many_to_many`  | `autocomplete`, `dropdown`        | Relation to multiple items (many-to-many field)                      |
| `OneToOneField` | `autocomplete`, `dropdown`        | Unique foreign key, can be embedded or selected                      |
| `date`          | `calendar`                        | Date-only selection (`yy-mm-dd`)                                     |
| `file`          | `upload`                          | Upload one or more files                                             |
| `image`         | `image` + preview (custom)        | Image file with preview                                              |
| `json`          | `editor` (custom integration)     | Monaco or Ace for editable JSON                                      |
| `color`         | `colorPicker`                     | Color selection with HEX or RGB format                               |
| `primarykey`    | None                              | Primary key field (auto-increment, UUID, etc.) - always readonly/disabled |

## Widget Configuration

| **Option** | **Type** | **Description** | **Used By** |
|------------|----------|-----------------|-------------|
| `timeOnly` | boolean | Show only time picker | `time` fields |
| `showTime` | boolean | Show time in calendar | `datetime` fields |
| `mode` | string | Input mode (decimal) | `float` fields |
| `preview` | boolean | Show image preview | `image` fields |
| `editor_type` | string | Editor type (monaco/ace) | `json` fields |
| `min` | float | Minimum value | `number`/`float` fields |
| `max` | float | Maximum value | `number`/`float` fields |
| `step` | float | Step increment | `number`/`float` fields |

## Field Type Details

### `string`
- **Purpose**: Text input fields
- **Widgets**: `text`, `textarea`, `password`
- **Validation**: Length limits, pattern matching
- **Use Cases**: Names, descriptions, passwords, emails

### `number`
- **Purpose**: Integer input fields
- **Widgets**: `input`, `Slider`
- **Validation**: Min/max values, step increments
- **Use Cases**: Quantities, ratings, scores, counts

### `float`
- **Purpose**: Decimal number input
- **Widgets**: `input`, `Slider`
- **Configuration**: `mode="decimal"`
- **Use Cases**: Prices, measurements, percentages, weights

### `time`
- **Purpose**: Time-only input
- **Widgets**: `calendar` with `timeOnly=True`
- **Validation**: HH:MM format
- **Use Cases**: Start times, durations, schedules

### `datetime`
- **Purpose**: Combined date and time input
- **Widgets**: `calendar` with `showTime=True`
- **Validation**: ISO datetime format
- **Use Cases**: Created dates, event times, timestamps

### `boolean`
- **Purpose**: True/false toggle
- **Widgets**: `Checkbox`, `switch`, `select`
- **Validation**: Boolean values only
- **Use Cases**: Active flags, yes/no questions, toggles

### `choice`
- **Purpose**: Single selection from options
- **Widgets**: `dropdown`, `radio`, `select`
- **Validation**: Must be one of predefined choices
- **Use Cases**: Categories, status, single selection

### `multichoice`
- **Purpose**: Multiple selections from options
- **Widgets**: `multiSelect`, `chips`, `listBox`
- **Validation**: Min/max selections, valid choices
- **Use Cases**: Tags, roles, multiple selections

### `foreignkey`
- **Purpose**: Many-to-one relationships
- **Widgets**: `dropdown`, `autoComplete`
- **Configuration**: `model`, `id_field`, `title_field`
- **Use Cases**: Model relationships, foreign keys

### `many_to_many`
- **Purpose**: Many-to-many relationships
- **Widgets**: `autoComplete`, `dropdown`
- **Configuration**: `model`, `id_field`, `title_field`
- **Use Cases**: Multiple model relationships

### `OneToOneField`
- **Purpose**: One-to-one relationships
- **Widgets**: `autoComplete`, `dropdown`
- **Configuration**: `model`, `id_field`, `title_field`
- **Use Cases**: Unique model relationships

### `date`
- **Purpose**: Date-only selection
- **Widgets**: `calendar`
- **Validation**: YYYY-MM-DD format
- **Use Cases**: Birth dates, event dates, deadlines

### `file`
- **Purpose**: File upload
- **Widgets**: `upload`
- **Validation**: File type, size limits
- **Use Cases**: Documents, attachments, files

### `image`
- **Purpose**: Image upload with preview
- **Widgets**: `image`
- **Configuration**: `preview=True`
- **Use Cases**: Avatars, photos, images

### `json`
- **Purpose**: Structured JSON data
- **Widgets**: `editor`
- **Configuration**: `editor_type` (monaco/ace)
- **Use Cases**: Configuration, metadata, complex data

### `color`
- **Purpose**: Color selection
- **Widgets**: `colorPicker`
- **Validation**: HEX or RGB format
- **Use Cases**: Theme colors, branding, visual settings

### `primarykey`
- **Purpose**: Primary key field
- **Widgets**: None (no widget)
- **Validation**: Unique identifier validation
- **Use Cases**: Auto-increment IDs, UUIDs, custom primary keys
- **Behavior**: Always readonly and disabled

## Widget Behavior

### Calendar Widget
- **timeOnly**: Shows only time picker (HH:MM)
- **showTime**: Shows both date and time picker
- **Default**: Shows only date picker

### Slider Widget
- **min/max**: Defines range
- **step**: Defines increment
- **mode**: "decimal" for float values

### MultiSelect Widget
- **min_selections**: Minimum required selections
- **max_selections**: Maximum allowed selections

### AutoComplete Widget
- **search**: Enables search functionality
- **model**: Related model for suggestions

## Relationship Fields

### `foreignkey`
- **Purpose**: Many-to-one relationships
- **Widgets**: `dropdown`, `autoComplete`
- **Configuration**: `model`, `id_field`, `title_field`
- **Example**: User belongs to one Department

### `many_to_many`
- **Purpose**: Many-to-many relationships
- **Widgets**: `autoComplete`, `dropdown`
- **Configuration**: `model`, `id_field`, `title_field`
- **Example**: User has many Roles, Role has many Users

### `OneToOneField`
- **Purpose**: One-to-one relationships
- **Widgets**: `autoComplete`, `dropdown`
- **Configuration**: `model`, `id_field`, `title_field`
- **Example**: User has one Profile, Profile belongs to one User

## Field Validation

| **Field Type** | **Validation Rules** |
|----------------|---------------------|
| `string` | Length, pattern (email) |
| `number` | Min/max values, step |
| `float` | Min/max values, decimal precision |
| `time` | HH:MM format |
| `datetime` | ISO datetime format |
| `email` | Email pattern validation |
| `multichoice` | Min/max selections |
| `file` | File type, size limits |
| `image` | Image format, size limits |

## Usage Examples

### Basic Field Creation
```python
from fp_admin.admin.fields import FieldView

# String field
name_field = FieldView.string_field("name", "Name")

# Number field with slider
rating_field = FieldView.slider_field("rating", "Rating")

# Time field with configuration
time_field = FieldView.time_field("start_time", "Start Time")

# Boolean field with switch
active_field = FieldView.switch_field("active", "Active")

# Choice field with dropdown
category_field = FieldView.select_field("category", "Category")

# Multichoice field with chips
tags_field = FieldView.chips_field("tags", "Tags")
```

### Widget Configuration
```python
from fp_admin.admin.fields import FieldView, WidgetConfig

# Float field with decimal mode
price_field = FieldView.float_field(
    "price",
    "Price",
    widget_config=WidgetConfig(mode="decimal", min=0.0, max=1000.0)
)

# Image field with preview
avatar_field = FieldView.image_field(
    "avatar",
    "Avatar",
    widget_config=WidgetConfig(preview=True)
)

# JSON field with Monaco editor
config_field = FieldView.json_field(
    "config",
    "Configuration",
    widget_config=WidgetConfig(editor_type="monaco")
)

# Number field with slider and range
score_field = FieldView.slider_field(
    "score",
    "Score",
    widget_config=WidgetConfig(min=0, max=100, step=5)
)
```

### Relationship Fields
```python
from fp_admin.admin.fields import RelationshipField

# Foreign key relationship
user_field = RelationshipField.foreignkey_field(
    "user_id",
    "User",
    model="User"
)

# Many-to-many relationship
roles_field = RelationshipField.many_to_many_field(
    "roles",
    "Roles",
    model="Role"
)

# Autocomplete relationship
department_field = RelationshipField.autocomplete_field(
    "department",
    "Department",
    model="Department"
)
```

### Choice Fields with Options
```
