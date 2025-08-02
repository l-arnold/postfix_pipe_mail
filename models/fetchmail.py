from odoo import api, fields, models
import subprocess
import logging

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
    
    @api.model
    def _fetch_mails(self):
        """Override to handle Postfix pipe processing"""
        for server in self:
            if server.server_type == 'postfix_pipe':
                server._fetch_postfix_pipe_mails()
            else:
                super(FetchmailServer, server)._fetch_mails()
    
    def _fetch_postfix_pipe_mails(self):
        """Process mails from Postfix pipe mbox file"""
        try:
            if self.script_path:
                # Run the custom script
                result = subprocess.run(
                    [self.script_path], 
                    capture_output=True, 
                    text=True,
                    user='odoo'  # Run as odoo user
                )
                
                if result.stdout:
                    # Process the mail content
                    mail_content = result.stdout
                    self._process_mail_content(mail_content)
                    _logger.info(f"Processed mail from {self.script_path}")
                    
            elif self.mbox_path:
                # Direct mbox processing
                self._process_mbox_direct()
                
        except Exception as e:
            _logger.error(f"Error processing Postfix pipe mail: {e}")
    
    def _process_mail_content(self, mail_content):
        """Process individual mail content"""
        if mail_content.strip():
            # Use Odoo's built-in mail processing
            self.env['mail.thread'].message_process(
                self.object_id.model if self.object_id else None,
                mail_content,
                save_original=True
            )
    
    def _process_mbox_direct(self):
        """Direct mbox file processing"""
        import os
        if os.path.exists(self.mbox_path) and os.path.getsize(self.mbox_path) > 0:
            with open(self.mbox_path, 'r') as f:
                content = f.read()
            
            if content.strip():
                self._process_mail_content(content)
                # Clear the file after processing
                open(self.mbox_path, 'w').close()