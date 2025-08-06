#!/bin/bash

#!/bin/bash

LOGFILE="/tmp/odoo_mail_handler.log"
echo "$(date) - Invoked with sender: $SENDER, recipient: $RECIPIENT" >> "$LOGFILE"


# Enhanced mail handler for Odoo integration
MAIL_DIR="/opt/odoo/mail"
MAIL_FILE="$MAIL_DIR/incoming_mail.mbox"
LOG_FILE="/var/log/odoo-mail-handler.log"

# Create directory if it doesn't exist
mkdir -p "$MAIL_DIR"

# Log the delivery attempt
echo "$(date): Mail delivery attempt" >> "$LOG_FILE"

# Read the entire email from stdin
EMAIL_CONTENT=$(cat)

# Append to mbox format with proper separator
echo "" >> "$MAIL_FILE"
echo "From postfix $(date)" >> "$MAIL_FILE"
echo "$EMAIL_CONTENT" >> "$MAIL_FILE"
echo "" >> "$MAIL_FILE"

# Set proper permissions
chown odoo:odoo "$MAIL_FILE" 2>/dev/null || true
chmod 664 "$MAIL_FILE"
chown odoo:odoo "$LOG_FILE" 2>/dev/null || true
chmod 664 "$LOG_FILE"

# Log success
echo "$(date): Mail delivered successfully to $MAIL_FILE" >> "$LOG_FILE"

exit 0