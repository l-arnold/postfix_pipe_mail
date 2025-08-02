from odoo import api, fields, models
import subprocess
import logging
import os

_logger = logging.getLogger(__name__)

class FetchmailServer(models.Model):
    _inherit = 'fetchmail.server'
    
    server_type = fields.Selection(
        selection_add=[('postfix_pipe', 'Postfix Pipe')],
        ondelete={'postfix_pipe': 'cascade'}
    )
    
    script_path = fields.Char(
        string='Script Path',
        help='Path to script that processes the mbox file',
        default='/opt/odoo/scripts/read_mbox.py'
    )
    
    mbox_path = fields.Char(
        string='Mbox File Path',
        help='Path to the mbox file created by Postfix pipe',
        default='/opt/odoo/mail/incoming_mail.mbox'
    )
    
    def fetch_mail(self):
        """Override to handle Postfix pipe processing"""
        if self.server_type == 'postfix_pipe':
            return self._fetch_postfix_pipe_mails()
        else:
            return super(FetchmailServer, self).fetch_mail()
    
    def _fetch_postfix_pipe_mails(self):
        """Process mails from Postfix pipe mbox file"""
        try:
            mail_count = 0
            
            if self.script_path and os.path.exists(self.script_path):
                # Run the custom script
                _logger.info(f"Running script: {self.script_path}")
                result = subprocess.run(
                    ['python3', self.script_path], 
                    capture_output=True, 
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0 and result.stdout:
                    # Process the mail content
                    mail_content = result.stdout.strip()
                    if mail_content:
                        mail_count += self._process_mail_content(mail_content)
                        _logger.info(f"Processed mail from script {self.script_path}")
                else:
                    _logger.warning(f"Script returned error: {result.stderr}")
                    
            elif self.mbox_path and os.path.exists(self.mbox_path):
                # Direct mbox processing
                mail_count += self._process_mbox_direct()
            else:
                _logger.warning(f"Neither script ({self.script_path}) nor mbox file ({self.mbox_path}) exists")
                
            return mail_count
                
        except Exception as e:
            _logger.error(f"Error processing Postfix pipe mail: {e}")
            raise e
    
    def _process_mail_content(self, mail_content):
        """Process individual mail content"""
        try:
            if mail_content.strip():
                # Use Odoo's built-in mail processing
                self.env['mail.thread'].message_process(
                    self.object_id.model if self.object_id else None,
                    mail_content,
                    save_original=True
                )
                return 1
            return 0
        except Exception as e:
            _logger.error(f"Error processing mail content: {e}")
            return 0
    
    def _process_mbox_direct(self):
        """Direct mbox file processing"""
        try:
            mail_count = 0
            if os.path.exists(self.mbox_path) and os.path.getsize(self.mbox_path) > 0:
                with open(self.mbox_path, 'r') as f:
                    content = f.read()
                
                if content.strip():
                    mail_count += self._process_mail_content(content)
                    # Clear the file after processing
                    with open(self.mbox_path, 'w') as f:
                        f.write('')
                    _logger.info(f"Processed and cleared mbox file: {self.mbox_path}")
                    
            return mail_count
        except Exception as e:
            _logger.error(f"Error processing mbox file: {e}")
            return 0