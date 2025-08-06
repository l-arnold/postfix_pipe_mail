#!/usr/bin/env python3
import os
import sys

import datetime

with open("/tmp/odoo_mail_pipe.log", "a") as log:
    log.write(f"{datetime.datetime.now()} - Triggered for recipient: {sys.argv[1] if len(sys.argv) > 1 else 'unknown'}\n")



def main():
    mbox_path = '/opt/odoo/mail/incoming_mail.mbox'
    
    try:
        # Check if file exists
        if not os.path.exists(mbox_path):
            print(f"ERROR: Mbox file does not exist: {mbox_path}", file=sys.stderr)
            sys.exit(1)
            
        # Check if file is readable
        if not os.access(mbox_path, os.R_OK):
            print(f"ERROR: Cannot read mbox file: {mbox_path}", file=sys.stderr)
            sys.exit(1)
            
        # Check file size
        if os.path.getsize(mbox_path) == 0:
            # No mail to process - this is normal
            sys.exit(0)
            
        # Read the file
        with open(mbox_path, 'r') as f:
            content = f.read()
            
        # Check if we can write to the file (to clear it)
        if not os.access(mbox_path, os.W_OK):
            print(f"ERROR: Cannot write to mbox file: {mbox_path}", file=sys.stderr)
            sys.exit(1)
            
        # Clear the mbox after reading
        with open(mbox_path, 'w') as f:
            f.write('')
            
        # Output the content (this goes to Odoo)
        print(content)
        
    except PermissionError as e:
        print(f"ERROR: Permission denied: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()