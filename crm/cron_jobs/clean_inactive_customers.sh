#!/bin/bash
set -euo pipefail

# حدد أماكن الملفات
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_FILE="/tmp/customer_cleanup_log.txt"

cd "$PROJECT_ROOT"

# شغّل كود بايثون من داخل manage.py shell
DELETED_COUNT=$(python3 manage.py shell <<'PY'
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, Order

cutoff = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(order__created_at__gte=cutoff).distinct()
count = inactive_customers.count()
inactive_customers.delete()
print(count)
PY
)

echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted ${DELETED_COUNT} inactive customers" >> "$LOG_FILE"
