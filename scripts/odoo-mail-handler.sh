#!/bin/bash

# --- Configurable paths ---
TMP_LOG="/tmp/odoo_mail_handler.log"
DELIVERY_LOG="/var/log/odoo-mail-handler.log"
MAIL_DIR="/opt/odoo/mail"
MAIL_FILE="$MAIL_DIR/incoming_mail.mbox"

# --- Ensure mail directory exists ---
mkdir -p "$MAIL_DIR"

# --- Read full email from stdin once ---
EMAIL_CONTENT=$(cat)

# --- Timestamp for logging ---
NOW="$(date)"

# --- Debug log (raw message + invocation) ---
{
  echo "[$NOW] --- Handler invoked ---"
  echo "[$NOW] Raw message follows:"
  echo "$EMAIL_CONTENT"
  echo "[$NOW] --- End of message ---"
} >> "$TMP_LOG"

# --- Extract headers for traceability ---
FROM_HEADER=$(echo "$EMAIL_CONTENT" | grep -i '^From:' | head -n1)
TO_HEADER=$(echo "$EMAIL_CONTENT" | grep -i '^To:' | head -n1)
SUBJECT_HEADER=$(echo "$EMAIL_CONTENT" | grep -i '^Subject:' | head -n1)
MSG_MD5=$(echo "$EMAIL_CONTENT" | md5sum | awk '{print $1}')

# --- Delivery log ---
{
  echo "$NOW: Handler invoked"
  echo "$NOW: From header: $FROM_HEADER"
  echo "$NOW: To header: $TO_HEADER"
  echo "$NOW: Subject: $SUBJECT_HEADER"
  echo "$NOW: Message MD5: $MSG_MD5"
  echo "$NOW: Mail delivery attempt"
} >> "$DELIVERY_LOG"

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
echo "$NOW: Mail delivered successfully to $MAIL_FILE" >> "$DELIVERY_LOG"

# --- Optional: echo to stderr for Postfix visibility ---
echo "$NOW: Handler completed successfully" >&2

exit 0
