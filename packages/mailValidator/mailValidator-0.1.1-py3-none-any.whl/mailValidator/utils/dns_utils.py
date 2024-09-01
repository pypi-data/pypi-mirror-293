import dns.resolver
import dns.exception


def get_mx_record(domain):
    """
    Fetches the MX record for a given domain.
    """
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 2
        resolver.lifetime = 5
        records = resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)
        return mx_record
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException) as e:
        # print(f"DNS Error for MX record: {e}")
        return None


def get_domain_details(domain):
    """
    Fetches A, NS, and TXT records for a given domain.
    """
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 2
        resolver.lifetime = 5

        a_records = resolver.resolve(domain, 'A')
        ns_records = resolver.resolve(domain, 'NS')
        txt_records = resolver.resolve(domain, 'TXT')

        return {
            "A Record": [str(record) for record in a_records],
            "NS Record": [str(record) for record in ns_records],
            "TXT Record": [str(record) for record in txt_records],
        }
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException) as e:
        # print(f"DNS Error for domain details: {e}")
        return None