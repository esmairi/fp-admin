# Blog App Example

A complete blog application built with fp-admin, demonstrating how to create a full-featured content management system with user management, posts, categories, tags, and comments.

## 🚀 Features

- **User Management**: Register and manage users with different roles (admin, author, reader)
- **Content Management**: Create, edit, and publish blog posts
- **Category System**: Organize posts into categories
- **Tagging System**: Add tags to posts for better organization
- **Comment System**: Allow readers to comment on posts with moderation
- **Admin Interface**: Beautiful admin interface for all content management
- **Blog Settings**: Configure blog-wide settings and preferences

## 📁 Project Structure

```
blog_app/
├── app.py                 # Main application file
├── settings.py           # Application settings
├── apps/
│   └── blog/
│       ├── __init__.py
│       ├── models.py     # Database models
│       ├── admin.py      # Admin interface configuration
│       ├── views.py      # Custom view configurations
│       ├── apps.py       # App configuration
│       └── routers.py    # API routes
└── scripts/
    └── sample_data.py    # Sample data creation script
```

## 🛠️ Models

### User Model (from fp_admin.apps.auth.models)
- **Fields**: username, email, password, is_active, is_superuser
- **Features**: Authentication, authorization, user management
- **Note**: Uses the shared User model from the auth app

### Category Model
- **Fields**: name, slug, description, color, is_active
- **Features**: Post organization, visual categorization

### Tag Model
- **Fields**: name, slug, description
- **Features**: Post tagging, flexible categorization

### Post Model
- **Fields**: title, slug, content, excerpt, featured_image, status, is_featured, allow_comments, view_count, published_at
- **Features**: Rich content management, publishing workflow, SEO optimization, **file upload support**

### Comment Model
- **Fields**: content, is_approved, is_spam, ip_address, user_agent
- **Features**: Comment moderation, spam detection, threaded comments

### BlogSettings Model
- **Fields**: site_name, site_description, posts_per_page, allow_registration, moderate_comments
- **Features**: Blog configuration, user registration control

## 🚀 Getting Started

### 1. Setup the Project

```bash
# Navigate to the blog app directory
cd examples/blog_app

# Install dependencies (if not already installed)
pip install fp-admin sqlmodel fastapi uvicorn
```

### 2. Initialize the Database

```bash
# Create initial migration
fp-admin make-migrations --name initial

# Apply migrations
fp-admin migrate
```

### 3. Create Sample Data

```bash
# Run the sample data script
python scripts/sample_data.py
```

### 4. Start the Application

```bash
# Run the development server
python app.py
```

### 5. Access the Admin Interface

- **URL**: http://localhost:8000/admin
- **Default Admin**: admin@example.com / admin123

## 📊 Sample Data

The sample data script creates:

- **4 Users**: Admin, 2 authors, 1 reader
- **3 Categories**: Technology, Lifestyle, Programming
- **5 Tags**: Python, FastAPI, Web Development, Tutorial, Tips
- **3 Posts**: Sample blog posts with content
- **3 Comments**: Sample comments on posts
- **1 Settings Record**: Blog configuration

## 🎨 Admin Interface Features

### User Management (via Auth App)
- User authentication and authorization
- User registration and management
- Role assignment (superuser, regular user)
- User activity tracking

### Content Management
- Rich text editor for post content
- Post status management (draft, published, archived)
- Featured post designation
- SEO-friendly slugs
- Excerpt generation
- **File Upload Support**: Featured image uploads with validation and thumbnails

### Category & Tag Management
- Visual category organization with colors
- Tag creation and management
- Category and tag statistics

### Comment Moderation
- Comment approval workflow
- Spam detection
- IP address and user agent tracking
- Threaded comment support

### Blog Settings
- Site configuration
- User registration control
- Comment moderation settings
- Posts per page configuration

## 🔧 Customization

### Adding New Models

1. **Create the model** in `apps/blog/models.py`
2. **Configure admin** in `apps/blog/admin.py`
3. **Add custom views** in `apps/blog/views.py`
4. **Register in app config** in `apps/blog/apps.py`

### Example: Adding a Newsletter Model

```python
# In models.py
class Newsletter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)
    subscribed_at: datetime = Field(default_factory=datetime.utcnow)

# In admin.py
class NewsletterAdmin(AdminModel):
    model = Newsletter
    label = "Newsletters"
    list_fields = ["email", "is_active", "subscribed_at"]
    search_fields = ["email"]

# In apps.py - add to admin_models list
admin_models = [
    # ... existing models
    NewsletterAdmin,
]
```

### File Upload Support

The blog app includes comprehensive file upload support:

- **Featured Images**: Upload images for blog posts
- **File Validation**: Extension and size validation
- **Thumbnail Generation**: Automatic thumbnail creation
- **Secure Storage**: Unique filenames and organized directory structure
- **Supported Formats**: JPG, JPEG, PNG, GIF, WebP
- **Size Limits**: 5MB maximum file size

### Custom Field Types

The admin interface supports various field types:

- `text` - Regular text input
- `textarea` - Multi-line text area
- `email` - Email input with validation
- `url` - URL input with validation
- `number` - Numeric input
- `checkbox` - Boolean checkbox
- `select` - Dropdown selection
- `date` - Date picker
- `datetime` - Date and time picker
- `color` - Color picker
- `password` - Password input
- `file` - File upload input

## 🧪 Testing

### Manual Testing

1. **User Management**:
   - Create new users with different roles
   - Test user profile editing
   - Verify role-based permissions

2. **Content Management**:
   - Create posts with different statuses
   - Test category and tag assignment
   - Verify post publishing workflow

3. **Comment System**:
   - Add comments to posts
   - Test comment moderation
   - Verify spam detection

### API Testing

The application provides RESTful APIs for all models:

- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/posts/` - List posts
- `POST /api/v1/posts/` - Create post
- And more...

## 📝 Best Practices

### Model Design
- Use descriptive field names
- Add proper field descriptions
- Implement proper relationships
- Use appropriate field types

### Admin Configuration
- Configure meaningful list fields
- Add helpful search and filter options
- Use appropriate field types for forms
- Provide clear help text

### Data Management
- Use migrations for schema changes
- Create sample data for testing
- Implement proper validation
- Handle relationships correctly

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection**:
   - Ensure database URL is correct in settings
   - Check if migrations are applied

2. **Admin Interface**:
   - Verify models are registered in admin
   - Check field configurations

3. **Sample Data**:
   - Ensure all dependencies are installed
   - Check database permissions

### Getting Help

- Check the fp-admin documentation
- Review the model and admin configurations
- Test with the sample data first
- Use the admin interface to explore the data

## 🎯 Next Steps

This blog app demonstrates the core features of fp-admin. You can extend it by:

- Adding authentication and authorization
- Implementing file uploads for images
- Adding search functionality
- Creating custom admin widgets
- Building a public-facing blog interface
- Adding analytics and reporting
- Implementing email notifications

## 📄 License

This example is part of the fp-admin project and follows the same license terms.
