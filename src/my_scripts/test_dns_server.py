import dns.resolver
import time
import argparse
import sys
from datetime import datetime

def test_dns_server(dns_server, domains, record_types=None, verbose=False):
    """
    Test a DNS server by querying for specified domains and record types.
    
    Args:
        dns_server (str): IP address of the DNS server to test
        domains (list): List of domain names to query
        record_types (list): List of DNS record types to query (default: A, AAAA, MX, NS, TXT)
        verbose (bool): Whether to print detailed information
    
    Returns:
        dict: Results of the DNS queries
    """
    if record_types is None:
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
    
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    resolver.timeout = 5
    resolver.lifetime = 5
    
    results = {
        'success': 0,
        'fail': 0,
        'queries': [],
        'errors': []
    }
    
    print(f"Testing DNS server: {dns_server}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing {len(domains)} domains with {len(record_types)} record types")
    print("-" * 60)
    
    for domain in domains:
        for record_type in record_types:
            query_result = {
                'domain': domain,
                'record_type': record_type,
                'success': False,
                'response_time': None,
                'records': []
            }
            
            try:
                start_time = time.time()
                answers = resolver.resolve(domain, record_type)
                end_time = time.time()
                response_time = end_time - start_time
                
                # Process the answers
                records = []
                for rdata in answers:
                    if record_type == 'A' or record_type == 'AAAA':
                        records.append(str(rdata.address))
                    elif record_type == 'MX':
                        records.append(f"{rdata.preference} {rdata.exchange}")
                    elif record_type == 'TXT':
                        records.append(rdata.strings[0].decode('utf-8'))
                    else:
                        records.append(str(rdata))
                
                query_result['success'] = True
                query_result['response_time'] = response_time
                query_result['records'] = records
                results['success'] += 1
                
                if verbose:
                    print(f"✓ {domain} ({record_type}): {response_time:.3f}s")
                    for record in records:
                        print(f"  - {record}")
                else:
                    print(f"✓ {domain} ({record_type}): {response_time:.3f}s")
                
            except dns.exception.Timeout:
                error_msg = "Timeout"
                query_result['error'] = error_msg
                results['fail'] += 1
                results['errors'].append(f"{domain} ({record_type}): {error_msg}")
                print(f"✗ {domain} ({record_type}): {error_msg}")
                
            except dns.resolver.NXDOMAIN:
                error_msg = "Domain does not exist"
                query_result['error'] = error_msg
                results['fail'] += 1
                results['errors'].append(f"{domain} ({record_type}): {error_msg}")
                print(f"✗ {domain} ({record_type}): {error_msg}")
                
            except dns.resolver.NoAnswer:
                error_msg = "No answer"
                query_result['error'] = error_msg
                results['fail'] += 1
                results['errors'].append(f"{domain} ({record_type}): {error_msg}")
                print(f"✗ {domain} ({record_type}): {error_msg}")
                
            except Exception as e:
                error_msg = str(e)
                query_result['error'] = error_msg
                results['fail'] += 1
                results['errors'].append(f"{domain} ({record_type}): {error_msg}")
                print(f"✗ {domain} ({record_type}): {error_msg}")
                
            results['queries'].append(query_result)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"DNS Test Summary")
    print(f"Server: {dns_server}")
    print(f"Successful queries: {results['success']}")
    print(f"Failed queries: {results['fail']}")
    success_rate = results['success'] / (results['success'] + results['fail']) * 100
    print(f"Success rate: {success_rate:.1f}%")
    
    if results['errors'] and verbose:
        print("\nErrors:")
        for error in results['errors']:
            print(f"- {error}")
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test a DNS server')
    parser.add_argument('dns_server', help='IP address of the DNS server to test')
    parser.add_argument('--domains', nargs='+', default=['google.com', 'amazon.com', 'microsoft.com', 'facebook.com', 'apple.com'],
                        help='List of domains to test')
    parser.add_argument('--record-types', nargs='+', default=['A', 'AAAA', 'MX', 'NS', 'TXT'],
                        help='List of DNS record types to test')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print verbose output')
    
    args = parser.parse_args()
    
    try:
        test_dns_server(args.dns_server, args.domains, args.record_types, args.verbose)
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
