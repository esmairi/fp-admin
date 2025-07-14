# Custom Fields

This guide covers how to create custom field types, validators, and widgets in fp-admin for advanced use cases.

## Overview

fp-admin provides a flexible system for creating custom fields that extends beyond the built-in field types. You can create custom field types, validators, and widgets to handle specialized data requirements.

## Custom Field Types

### Creating Custom Field Types

To create a custom field type, you need to:

1. **Extend FieldFactory** with your custom method
2. **Define validation rules** for your field type
3. **Specify widget configuration** if needed

```python
from fp_admin.admin.fields import FieldFactory, FieldView, FieldValidation
from fp_admin.admin.fields.widgets import WidgetConfig

class CustomFieldFactory(FieldFactory):
    @classmethod
    def phone_field(cls, name: str, title: str, **kwargs):
        """Create a phone number field with custom validation."""
        # Define custom validation
        validation = FieldValidation(
            pattern=r"^\+?1?\d{9,15}$",
            required=kwargs.get("required", False)
        )

        # Create widget configuration
        widget_config = WidgetConfig(
            placeholder="+1 (555) 123-4567",
            mask="(999) 999-9999"
        )

        return FieldView(
            name=name,
            title=title,
            field_type="string",
            widget="phone",
            widget_config=widget_config,
            validators=validation,
            **kwargs
        )

    @classmethod
    def credit_card_field(cls, name: str, title: str, **kwargs):
        """Create a credit card field with Luhn algorithm validation."""
        validation = FieldValidation(
            pattern=r"^\d{4}-\d{4}-\d{4}-\d{4}$",
            required=kwargs.get("required", False)
        )

        widget_config = WidgetConfig(
            placeholder="1234-5678-9012-3456",
            mask="9999-9999-9999-9999"
        )

        return FieldView(
            name=name,
            title=title,
            field_type="string",
            widget="credit_card",
            widget_config=widget_config,
            validators=validation,
            **kwargs
        )
```

### Using Custom Field Types

```python
from fp_admin.admin.views import BaseViewBuilder
from fp_admin.admin.fields import FieldFactory
from .custom_fields import CustomFieldFactory

class ContactFormView(BaseViewBuilder):
    model = Contact
    view_type = "form"
    name = "ContactForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("name", "Name", required=True),
        CustomFieldFactory.phone_field("phone", "Phone Number", required=True),
        CustomFieldFactory.credit_card_field("credit_card", "Credit Card"),
        FieldFactory.email_field("email", "Email", required=True),
    ]
```

## Custom Validators

### Creating Custom Validators

Custom validators allow you to implement complex validation logic:

```python
from fp_admin.admin.fields.errors import FieldError
from fp_admin.admin.fields import FieldFactory

def validate_strong_password(value: str) -> FieldError:
    """Custom validator for strong password requirements."""
    if not value:
        return None

    errors = []

    if len(value) < 8:
        errors.append("PASSWORD MUST BE AT LEAST 8 CHARACTERS LONG")

    if not any(c.isupper() for c in value):
        errors.append("PASSWORD MUST CONTAIN AT LEAST ONE UPPERCASE LETTER")

    if not any(c.islower() for c in value):
        errors.append("PASSWORD MUST CONTAIN AT LEAST ONE LOWERCASE LETTER")

    if not any(c.isdigit() for c in value):
        errors.append("PASSWORD MUST CONTAIN AT LEAST ONE DIGIT")

    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in value):
        errors.append("PASSWORD MUST CONTAIN AT LEAST ONE SPECIAL CHARACTER")

    if errors:
        return FieldError(
            code="WEAK_PASSWORD",
            message="; ".join(errors)
        )

    return None

def validate_unique_email(value: str, model_class, current_id=None) -> FieldError:
    """Custom validator to ensure email uniqueness."""
    if not value:
        return None

    # Check if email already exists
    existing_user = model_class.objects.filter(email=value).first()
    if existing_user and existing_user.id != current_id:
        return FieldError(
            code="DUPLICATE_EMAIL",
            message="THIS EMAIL ADDRESS IS ALREADY REGISTERED"
        )

    return None
```

### Using Custom Validators

```python
class UserFormView(BaseViewBuilder):
    model = User
    view_type = "form"
    name = "UserForm"

    fields = [
        FieldFactory.primarykey_field("id", "ID"),
        FieldFactory.string_field("username", "Username", required=True),
        FieldFactory.email_field("email", "Email", required=True),
        FieldFactory.password_field(
            "password",
            "Password",
            required=True,
            custom_validator=validate_strong_password
        ),
    ]
```

### Complex Custom Validators

```python
def validate_business_hours(value: str) -> FieldError:
    """Validate business hours format (e.g., '9:00 AM - 5:00 PM')."""
    if not value:
        return None

    import re
    pattern = r"^([0-9]|1[0-2]):[0-5][0-9]\s(AM|PM)\s-\s([0-9]|1[0-2]):[0-5][0-9]\s(AM|PM)$"

    if not re.match(pattern, value):
        return FieldError(
            code="INVALID_HOURS_FORMAT",
            message="HOURS MUST BE IN FORMAT: 9:00 AM - 5:00 PM"
        )

    return None

def validate_zip_code(value: str) -> FieldError:
    """Validate US ZIP code format."""
    if not value:
        return None

    import re
    pattern = r"^\d{5}(-\d{4})?$"

    if not re.match(pattern, value):
        return FieldError(
            code="INVALID_ZIP_CODE",
            message="ZIP CODE MUST BE IN FORMAT: 12345 OR 12345-6789"
        )

    return None
```

## Custom Widgets

### Creating Custom Widgets

Custom widgets allow you to create specialized UI components:

```python
from fp_admin.admin.fields.widgets import WidgetConfig

class CustomWidgetConfig(WidgetConfig):
    """Custom widget configuration for specialized widgets."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.custom_property = kwargs.get("custom_property", None)

# Custom field with custom widget
def create_custom_widget_field(name: str, title: str, **kwargs):
    """Create a field with custom widget configuration."""
    widget_config = CustomWidgetConfig(
        custom_property="custom_value",
        placeholder=kwargs.get("placeholder", ""),
        mask=kwargs.get("mask", "")
    )

    return FieldView(
        name=name,
        title=title,
        field_type="string",
        widget="custom_widget",
        widget_config=widget_config,
        **kwargs
    )
```

### Advanced Widget Configuration

```python
class AdvancedWidgetConfig(WidgetConfig):
    """Advanced widget configuration with multiple options."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autocomplete = kwargs.get("autocomplete", False)
        self.search_url = kwargs.get("search_url", None)
        self.min_chars = kwargs.get("min_chars", 2)
        self.max_results = kwargs.get("max_results", 10)

def create_autocomplete_field(name: str, title: str, search_url: str, **kwargs):
    """Create an autocomplete field with custom search."""
    widget_config = AdvancedWidgetConfig(
        autocomplete=True,
        search_url=search_url,
        min_chars=2,
        max_results=10,
        placeholder="START TYPING TO SEARCH..."
    )

    return FieldView(
        name=name,
        title=title,
        field_type="string",
        widget="autocomplete",
        widget_config=widget_config,
        **kwargs
    )
```

## Field Type Extensions

### Extending Existing Field Types

You can extend existing field types with additional functionality:

```python
class ExtendedFieldFactory(FieldFactory):
    @classmethod
    def enhanced_email_field(cls, name: str, title: str, **kwargs):
        """Enhanced email field with additional validation."""
        # Get base email validation
        base_field = cls.email_field(name, title, **kwargs)

        # Add custom validation
        def validate_email_domain(value: str) -> FieldError:
            if not value:
                return None

            # Check for common disposable email domains
            disposable_domains = [
                "tempmail.com", "throwaway.com", "10minutemail.com"
            ]

            domain = value.split("@")[-1].lower()
            if domain in disposable_domains:
                return FieldError(
                    code="DISPOSABLE_EMAIL",
                    message="DISPOSABLE EMAIL ADDRESSES ARE NOT ALLOWED"
                )

            return None

        # Add custom validator
        base_field.custom_validator = validate_email_domain
        return base_field

    @classmethod
    def enhanced_password_field(cls, name: str, title: str, **kwargs):
        """Enhanced password field with strength meter."""
        base_field = cls.password_field(name, title, **kwargs)

        # Add strength meter widget configuration
        widget_config = WidgetConfig(
            show_strength_meter=True,
            min_strength=3,  # 1-5 scale
            strength_labels={
                1: "VERY WEAK",
                2: "WEAK",
                3: "MEDIUM",
                4: "STRONG",
                5: "VERY STRONG"
            }
        )

        base_field.widget_config = widget_config
        return base_field
```

## Validation Chains

### Creating Validation Chains

You can chain multiple validators together:

```python
def create_validation_chain(*validators):
    """Create a chain of validators."""
    def chained_validator(value: str) -> FieldError:
        for validator in validators:
            error = validator(value)
            if error:
                return error
        return None

    return chained_validator

# Usage example
def validate_phone_format(value: str) -> FieldError:
    """Validate phone number format."""
    import re
    pattern = r"^\+?1?\d{9,15}$"
    if not re.match(pattern, value):
        return FieldError(
            code="INVALID_PHONE_FORMAT",
            message="PHONE NUMBER MUST BE IN VALID FORMAT"
        )
    return None

def validate_phone_country(value: str) -> FieldError:
    """Validate phone number country code."""
    if value and not value.startswith("+1"):
        return FieldError(
            code="INVALID_COUNTRY_CODE",
            message="PHONE NUMBER MUST START WITH +1"
        )
    return None

# Create chained validator
phone_validator = create_validation_chain(
    validate_phone_format,
    validate_phone_country
)

# Use in field
FieldFactory.string_field(
    "phone",
    "Phone Number",
    custom_validator=phone_validator
)
```

## Conditional Validation

### Implementing Conditional Validation

```python
def create_conditional_validator(condition_func, validator_func):
    """Create a validator that only runs under certain conditions."""
    def conditional_validator(value: str, form_data: dict = None) -> FieldError:
        if condition_func(form_data):
            return validator_func(value)
        return None

    return conditional_validator

# Example: Validate business hours only if business is open
def is_business_open(form_data: dict) -> bool:
    """Check if business is marked as open."""
    return form_data.get("is_open", False)

def validate_business_hours_conditional(value: str, form_data: dict = None) -> FieldError:
    """Validate business hours only if business is open."""
    if not is_business_open(form_data):
        return None

    return validate_business_hours(value)

# Usage
business_hours_validator = create_conditional_validator(
    is_business_open,
    validate_business_hours_conditional
)
```

## Custom Field Types with Business Logic

### Complex Custom Fields

```python
class BusinessFieldFactory(FieldFactory):
    @classmethod
    def tax_id_field(cls, name: str, title: str, **kwargs):
        """Create a tax ID field with validation."""
        def validate_tax_id(value: str) -> FieldError:
            if not value:
                return None

            # Remove common separators
            clean_value = value.replace("-", "").replace(" ", "")

            # Check length (SSN: 9 digits, EIN: 9 digits)
            if len(clean_value) != 9:
                return FieldError(
                    code="INVALID_TAX_ID_LENGTH",
                    message="TAX ID MUST BE 9 DIGITS"
                )

            # Check if all digits
            if not clean_value.isdigit():
                return FieldError(
                    code="INVALID_TAX_ID_FORMAT",
                    message="TAX ID MUST CONTAIN ONLY DIGITS"
                )

            return None

        widget_config = WidgetConfig(
            placeholder="123-45-6789",
            mask="999-99-9999"
        )

        return FieldView(
            name=name,
            title=title,
            field_type="string",
            widget="tax_id",
            widget_config=widget_config,
            custom_validator=validate_tax_id,
            **kwargs
        )

    @classmethod
    def credit_score_field(cls, name: str, title: str, **kwargs):
        """Create a credit score field with range validation."""
        def validate_credit_score(value: int) -> FieldError:
            if value is None:
                return None

            if not isinstance(value, int):
                return FieldError(
                    code="INVALID_CREDIT_SCORE_TYPE",
                    message="CREDIT SCORE MUST BE A NUMBER"
                )

            if value < 300 or value > 850:
                return FieldError(
                    code="INVALID_CREDIT_SCORE_RANGE",
                    message="CREDIT SCORE MUST BE BETWEEN 300 AND 850"
                )

            return None

        widget_config = WidgetConfig(
            min_value=300,
            max_value=850,
            step=1
        )

        return FieldView(
            name=name,
            title=title,
            field_type="number",
            widget="slider",
            widget_config=widget_config,
            custom_validator=validate_credit_score,
            **kwargs
        )
```

## Testing Custom Fields

### Unit Tests for Custom Fields

```python
import pytest
from fp_admin.admin.fields.errors import FieldError

def test_phone_field_validation():
    """Test phone field validation."""
    from .custom_fields import CustomFieldFactory

    field = CustomFieldFactory.phone_field("phone", "Phone Number")

    # Test valid phone numbers
    valid_numbers = [
        "+1234567890",
        "1234567890",
        "+1-234-567-8900"
    ]

    for number in valid_numbers:
        errors = field.validate_value(number)
        assert len(errors) == 0, f"VALID PHONE NUMBER FAILED: {number}"

    # Test invalid phone numbers
    invalid_numbers = [
        "123",
        "abc",
        "123-456-789"
    ]

    for number in invalid_numbers:
        errors = field.validate_value(number)
        assert len(errors) > 0, f"INVALID PHONE NUMBER PASSED: {number}"

def test_custom_validator():
    """Test custom validator function."""
    from .validators import validate_strong_password

    # Test strong password
    strong_password = "SecurePass123!"
    error = validate_strong_password(strong_password)
    assert error is None

    # Test weak password
    weak_password = "weak"
    error = validate_strong_password(weak_password)
    assert error is not None
    assert "WEAK" in error.message
```

## Best Practices

### 1. Keep Validators Focused

```python
# Good: Single responsibility
def validate_email_format(value: str) -> FieldError:
    """Validate email format only."""
    import re
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, value):
        return FieldError(code="INVALID_EMAIL", message="INVALID EMAIL FORMAT")
    return None

# Good: Separate domain validation
def validate_email_domain(value: str) -> FieldError:
    """Validate email domain only."""
    # Domain-specific validation logic
    pass
```

### 2. Use Descriptive Error Messages

```python
# Good: Clear, descriptive error messages
def validate_zip_code(value: str) -> FieldError:
    if not value:
        return None

    import re
    pattern = r"^\d{5}(-\d{4})?$"

    if not re.match(pattern, value):
        return FieldError(
            code="INVALID_ZIP_CODE",
            message="ZIP CODE MUST BE IN FORMAT: 12345 OR 12345-6789"
        )

    return None
```

### 3. Handle Edge Cases

```python
def validate_phone_number(value: str) -> FieldError:
    """Validate phone number with edge case handling."""
    if not value:
        return None

    # Handle None values
    if value is None:
        return FieldError(code="REQUIRED", message="PHONE NUMBER IS REQUIRED")

    # Handle empty strings
    if value.strip() == "":
        return FieldError(code="REQUIRED", message="PHONE NUMBER IS REQUIRED")

    # Handle non-string values
    if not isinstance(value, str):
        return FieldError(code="TYPE_ERROR", message="PHONE NUMBER MUST BE TEXT")

    # Continue with validation...
    return None
```

### 4. Document Custom Fields

```python
class CustomFieldFactory(FieldFactory):
    """Custom field factory with specialized field types."""

    @classmethod
    def phone_field(cls, name: str, title: str, **kwargs):
        """
        Create a phone number field with validation.

        Args:
            name: Field name
            title: Field display title
            **kwargs: Additional field options

        Returns:
            FieldView: Configured phone field

        Example:
            phone_field = CustomFieldFactory.phone_field(
                "phone", "Phone Number", required=True
            )
        """
        # Implementation...
```

## Performance Considerations

### 1. Cache Validation Results

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def validate_zip_code_cached(value: str) -> FieldError:
    """Cached zip code validation for performance."""
    return validate_zip_code(value)
```

### 2. Optimize Complex Validations

```python
def validate_credit_card_optimized(value: str) -> FieldError:
    """Optimized credit card validation."""
    if not value:
        return None

    # Quick format check first
    if not value.replace("-", "").isdigit():
        return FieldError(code="INVALID_FORMAT", message="INVALID CREDIT CARD FORMAT")

    # More expensive Luhn algorithm check only if format is valid
    return validate_luhn_algorithm(value)
```

## Next Steps

- **[Field Types](../user-guide/field-types.md)** - Learn about built-in field types
- **[Widgets](../user-guide/widgets.md)** - Discover available widgets
- **[Admin Models](../user-guide/admin-models.md)** - Configure admin interfaces
- **[Error Handling](error-handling.md)** - Handle validation errors properly
