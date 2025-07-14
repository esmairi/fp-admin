# CLI Commands

This guide covers all available command-line interface (CLI) commands in fp-admin.

## Overview

fp-admin provides a comprehensive CLI for project management, database operations, and development tasks.

## Installation

The CLI is automatically installed with fp-admin:

```bash
# Install fp-admin (includes CLI)
pip install fp-admin

# Verify installation
fp-admin --version
```

## Basic Commands

### Help

```bash
# Show general help
fp-admin --help

# Show help for specific command
fp-admin startproject --help
fp-admin startapp --help
```

### Version

```bash
# Show fp-admin version
fp-admin --version
```

## Project Management

### Create New Project

```bash
# Create a new fp-admin project
fp-admin startproject myapp
```


### Create New App

```bash
# Create a new app
fp-admin startapp blog

# Create app with admin views
fp-admin startapp blog
```



## Database Commands

### Create Migrations

```bash
# Create initial migration
fp-admin make-migrations initial
```

### Apply Migrations

```bash
# Apply all pending migrations
fp-admin migrate

```

## User Management

### Create Superuser

```bash
# Create superuser interactively
fp-admin createsuperuser

# Create superuser with command line arguments
fp-admin createsuperuser --username=admin --email=admin@example.com --password=secret

```

**Options:**
- `--username`: Username for superuser
- `--email`: Email for superuser
- `--password`: Password for superuser

### Create User (TODO)

```bash
# Create regular user
fp-admin createuser

# Create user with specific data
fp-admin createuser --username=john --email=john@example.com --password=secret

# Create user without password prompt
fp-admin createuser --noinput --username=john --email=john@example.com --password=secret
```

**Options:**
- `--username`: Username for user
- `--email`: Email for user
- `--password`: Password for user
- `--noinput`: Non-interactive mode

### List Users (TODO)

```bash
# List all users
fp-admin list-users

# List users with details
fp-admin list-users --verbose

# List users in specific group
fp-admin list-users --group=admins
```

### Update User (TODO)

```bash
# Update user password
fp-admin updateuser --username=john --password=newpassword

# Update user email
fp-admin updateuser --username=john --email=newemail@example.com

# Update user status
fp-admin updateuser --username=john --is-active=false
```

### Delete User (TODO)

```bash
# Delete user
fp-admin deleteuser --username=john

# Delete user with confirmation
fp-admin deleteuser --username=john --confirm
```

## Group Management (TODO)

### Create Group

```bash
# Create group
fp-admin creategroup --name=editors --description="Content editors"

# Create group without description
fp-admin creategroup --name=viewers
```

### List Groups

```bash
# List all groups
fp-admin list-groups

# List groups with details
fp-admin list-groups --verbose
```

### Add User to Group

```bash
# Add user to group
fp-admin adduser --username=john --group=editors

# Add multiple users to group
fp-admin adduser --usernames=john,jane --group=editors
```

### Remove User from Group

```bash
# Remove user from group
fp-admin removeuser --username=john --group=editors

# Remove multiple users from group
fp-admin removeuser --usernames=john,jane --group=editors
```

## Permission Management (TODO)

### Create Permission

```bash
# Create permission
fp-admin createpermission --codename=add_post --name="Can add post" --description="Can create new posts"

# Create permission without description
fp-admin createpermission --codename=view_post --name="Can view post"
```

### List Permissions

```bash
# List all permissions
fp-admin list-permissions

# List permissions with details
fp-admin list-permissions --verbose
```

### Add Permission to Group

```bash
# Add permission to group
fp-admin addpermission --codename=add_post --group=editors

# Add multiple permissions to group
fp-admin addpermission --codename=add_post,change_post --group=editors
```

### Remove Permission from Group

```bash
# Remove permission from group
fp-admin removepermission --codename=add_post --group=editors

# Remove multiple permissions from group
fp-admin removepermission --codename=add_post,change_post --group=editors
```

## Development Commands

### Run Development Server

```bash
# Run development server
fp-admin runserver

# Run on specific port
fp-admin runserver --port=8001

# Run on specific host
fp-admin runserver --host=0.0.0.0

# Run with auto-reload
fp-admin runserver --reload
```




## Configuration Commands (TODO)

### Show Settings

```bash
# Show current settings
fp-admin show-settings


# Show settings in specific format
fp-admin show-settings --format=json
```


## Utility Commands (TODO)

### Shell

```bash
# Start interactive shell
fp-admin shell
```



### Apps Management (TODO)

```bash
# List installed plugins
fp-admin list-apps

# Install plugin
fp-admin install-app --name=app-name

# Uninstall plugin
fp-admin uninstall-app --name=app-name
```




## Command Examples

### Complete Workflow

```bash
# 1. Create new project
fp-admin startproject myblog

# 2. Navigate to project
cd myblog

# 3. Create app
fp-admin startapp blog

# 4. Create migrations
fp-admin make-migrations

# 5. Apply migrations
fp-admin migrate

# 6. Create superuser
fp-admin createsuperuser --username=admin --email=admin@example.com --password=secret

# 7. Run development server
fp-admin runserver
```


### User Management (TODO)

```bash
# 1. Create group
fp-admin creategroup --name=editors --description="Content editors"

# 2. Create permission
fp-admin createpermission --codename=add_post --name="Can add post"

# 3. Add permission to group
fp-admin addpermission --codename=add_post --group=editors

# 4. Create user
fp-admin createuser --username=john --email=john@example.com --password=secret

# 5. Add user to group
fp-admin adduser --username=john --group=editors
```

## Troubleshooting

### Common Issues

```bash
# Check if fp-admin is installed
fp-admin --version

```


## Best Practices

### 1. Use Version Control

```bash
# Initialize git repository
git init

# Add files
git add .

# Commit changes
git commit -m "Initial commit"
```

### 2. Use Virtual Environments

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install fp-admin
pip install fp-admin
```



## Next Steps

- **[Admin Models](admin-models.md)** - Configure admin interfaces
- **[Field Types](field-types.md)** - Learn about field types and widgets
- **[Authentication](authentication.md)** - Set up user management
- **[Widgets](widgets.md)** - Discover advanced widgets and configurations
