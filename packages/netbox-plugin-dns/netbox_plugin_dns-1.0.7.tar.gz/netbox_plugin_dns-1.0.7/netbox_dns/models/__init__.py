from .zone import *
from .nameserver import *
from .record import *
from .view import *
from .contact import *
from .registrar import *
from .zone_template import *
from .record_template import *

# +
# Backwards compatibility fix, will be removed in version 1.1
# -
from netbox_dns.choices import *

from netbox_dns.signals import ipam_coupling
