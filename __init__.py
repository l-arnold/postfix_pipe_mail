from . import models

def post_init_hook(cr, registry):
    import shutil, os
    base = os.path.dirname(__file__)
    script_dir = os.path.join(base, 'scripts')
    shutil.copy(os.path.join(script_dir, 'odoo-mail-handler.sh'), '/opt/odoo/scripts/odoo-mail-handler.sh')
    shutil.copy(os.path.join(script_dir, 'read_mbox.py'), '/opt/odoo/scripts/read_mbox.py')
