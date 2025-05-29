#!/bin/bash

# This script gathers Django project information for debugging.
# Run it from the /home/project/xrwvm-fullstack_developer_capstone/server directory.

OUTPUT_FILE="django_debug_info.txt"
PROJECT_ROOT="/home/project/xrwvm-fullstack_developer_capstone/server"

echo "Gathering Django debug information..."

{
  echo "=== SCRIPT START TIME: $(date) ==="
  echo ""

  echo "=== SERVER DIRECTORY STRUCTURE (djangoproj and djangoapp only) ==="
  echo "--- ${PROJECT_ROOT}/djangoproj ---"
  ls -R "${PROJECT_ROOT}/djangoproj"
  echo ""
  echo "--- ${PROJECT_ROOT}/djangoapp ---"
  ls -R "${PROJECT_ROOT}/djangoapp"
  echo ""

  echo "=== ${PROJECT_ROOT}/Dockerfile ==="
  cat "${PROJECT_ROOT}/Dockerfile"
  echo ""
  echo "=== END OF Dockerfile ==="
  echo ""

  echo "=== ${PROJECT_ROOT}/entrypoint.sh ==="
  cat "${PROJECT_ROOT}/entrypoint.sh"
  echo ""
  echo "=== END OF entrypoint.sh ==="
  echo ""

  echo "=== ${PROJECT_ROOT}/requirements.txt ==="
  cat "${PROJECT_ROOT}/requirements.txt"
  echo ""
  echo "=== END OF requirements.txt ==="
  echo ""

  echo "=== ${PROJECT_ROOT}/djangoproj/settings.py ==="
  cat "${PROJECT_ROOT}/djangoproj/settings.py"
  echo ""
  echo "=== END OF djangoproj/settings.py ==="
  echo ""

  echo "=== ${PROJECT_ROOT}/djangoproj/urls.py ==="
  cat "${PROJECT_ROOT}/djangoproj/urls.py"
  echo ""
  echo "=== END OF djangoproj/urls.py ==="
  echo ""

  echo "=== ${PROJECT_ROOT}/djangoproj/wsgi.py ==="
  cat "${PROJECT_ROOT}/djangoproj/wsgi.py"
  echo ""
  echo "=== END OF djangoproj/wsgi.py ==="
  echo ""

  echo "=== ${PROJECT_ROOT}/djangoapp/views.py ==="
  cat "${PROJECT_ROOT}/djangoapp/views.py"
  echo ""
  echo "=== END OF djangoapp/views.py ==="
  echo ""

  echo "=== ${PROJECT_ROOT}/djangoapp/urls.py ==="
  cat "${PROJECT_ROOT}/djangoapp/urls.py"
  echo ""
  echo "=== END OF djangoapp/urls.py ==="
  echo ""

  echo "=== ${PROJECT_ROOT}/djangoapp/models.py ==="
  cat "${PROJECT_ROOT}/djangoapp/models.py"
  echo ""
  echo "=== END OF djangoapp/models.py ==="
  echo ""
  
  echo "=== ${PROJECT_ROOT}/djangoapp/admin.py ==="
  cat "${PROJECT_ROOT}/djangoapp/admin.py"
  echo ""
  echo "=== END OF djangoapp/admin.py ==="
  echo ""

  echo "=== ${PROJECT_ROOT}/djangoapp/apps.py ==="
  cat "${PROJECT_ROOT}/djangoapp/apps.py"
  echo ""
  echo "=== END OF djangoapp/apps.py ==="
  echo ""

  echo "=== ${PROJECT_ROOT}/manage.py ==="
  cat "${PROJECT_ROOT}/manage.py"
  echo ""
  echo "=== END OF manage.py ==="
  echo ""

  echo "=== SCRIPT END TIME: $(date) ==="
} > "${OUTPUT_FILE}"

echo ""
echo "All info dumped to ${OUTPUT_FILE} in the current directory (${PWD})."
echo "Please run 'cat ${OUTPUT_FILE}', then copy and paste ALL of its content here."