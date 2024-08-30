from netbox.plugins import PluginConfig

__version__ = "1.0.7"


class DNSConfig(PluginConfig):
    name = "netbox_dns"
    verbose_name = "NetBox DNS"
    description = "NetBox plugin for DNS data"
    min_version = "4.0.0"
    version = __version__
    author = "Peter Eckel"
    author_email = "pete@netbox-dns.org"
    required_settings = []
    default_settings = {
        "zone_default_ttl": 86400,
        "zone_soa_ttl": 86400,
        "zone_soa_serial": 1,
        "zone_soa_refresh": 43200,
        "zone_soa_retry": 7200,
        "zone_soa_expire": 2419200,
        "zone_soa_minimum": 3600,
        "feature_ipam_coupling": False,
        "tolerate_characters_in_zone_labels": "",
        "tolerate_underscores_in_labels": False,
        "tolerate_underscores_in_hostnames": False,  # Deprecated, will be removed in 1.2.0
        "tolerate_leading_underscore_types": [
            "TXT",
            "SRV",
        ],
        "tolerate_non_rfc1035_types": [],
        "enable_root_zones": False,
        "enforce_unique_records": True,
        "enforce_unique_rrset_ttl": True,
        "menu_name": "NetBox DNS",
        "top_level_menu": True,
    }
    base_url = "netbox-dns"


#
# Initialize plugin config
#
config = DNSConfig
