#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status 
    #it prevents the container from continuing if migrations or database connections fail.

# Function to wait for MySQL to be ready
wait_for_db() {
    echo "Waiting for database..."
    until python -c "import pymysql; pymysql.connect(host='$DB_HOST', user='$MYSQL_USER', password='$MYSQL_PASSWORD')"; do
        echo "Waiting for database..."
        sleep 2
    done
    echo "Database is ready!"
}

# Set environment variables for DB host if not set
DB_HOST=${DB_HOST:-db}

# Wait for MySQL
wait_for_db

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if environment variables exist
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py shell <<-END
	from django.contrib.auth import get_user_model
	User = get_user_model()
	if not User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').exists():
	    User.objects.create_superuser(
	        email='$DJANGO_SUPERUSER_EMAIL',
	        first_name='$DJANGO_SUPERUSER_FIRST_NAME',
	        last_name='$DJANGO_SUPERUSER_LAST_NAME',
	        password='$DJANGO_SUPERUSER_PASSWORD'
	    )
END
fi


# Start Django server
echo "Starting Django server..."
exec "$@"
