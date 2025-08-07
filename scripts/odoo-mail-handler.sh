#!/bin/bash

# --- Configurable paths ---
LOG_DIR="/var/log/odoo"
DELIVERY_LOG="$LOG_DIR/odoo-mail-handler.log"
MAIL_DIR="/opt/odoo/mail"
MAIL_FILE="$MAIL_DIR/incoming_mail.mbox"

# --- Ensure directories exist ---
mkdir -p "$MAIL_DIR" "$LOG_DIR"

# --- Redirect stdout and stderr to log ---
exec >> "$DELIVERY_LOG" 2>&1

# --- Enable debug tracing ---
set -x

# --- Timestamp and context ---
NOW="$(date)"
echo "[$NOW] --- Handler invoked ---"
echo "Running as: $(whoami)"
echo "PWD: $(pwd)"
echo "Script: $0"

# --- Read full email from stdin ---
EMAIL_CONTENT=$(cat)

# --- Log raw message ---
echo "[$NOW] Raw message follows:"
echo "$EMAIL_CONTENT"
echo "[$NOW] --- End of message ---"

# --- Extract headers for traceability ---
FROM_HEADER=$(echo "$EMAIL_CONTENT" | grep -i '^From:' | head -n1)
TO_HEADER=$(echo "$EMAIL_CONTENT" | grep -i '^To:' | head -n1)
SUBJECT_HEADER=$(echo "$EMAIL_CONTENT" | grep -i '^Subject:' | head -n1)
MSG_MD5=$(echo "$EMAIL_CONTENT" | md5sum | awk '{print $1}')

# --- Delivery log summary ---
echo "$NOW: From header: $FROM_HEADER"
echo "$NOW: To header: $TO_HEADER"
echo "$NOW: Subject: $SUBJECT_HEADER"
echo "$NOW: Message MD5: $MSG_MD5"
echo "$NOW: Mail delivery attempt"

# --- Append to mbox format ---
{
  echo ""
  echo "From postfix $NOW"
  echo "$EMAIL_CONTENT"
  echo ""
} >> "$MAIL_FILE"

# --- Set permissions (non-fatal) ---
chown odoo:odoo "$MAIL_FILE" "$DELIVERY_LOG" 2>/dev/null || true
chmod 664 "$MAIL_FILE" "$DELIVERY_LOG"

# --- Final success log ---
echo "$NOW: Mail delivered successfully to $MAIL_FILE"

# --- Optional: echo to stderr for Postfix visibility ---
echo "$NOW: Handler completed successfully" >&2

exit 0
