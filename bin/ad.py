from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException
import getpass

# Configuration parameters
AD_SERVER = 'DC-PDX1B-BKP01.ant.amazon.com'
AD_SEARCH_BASE = 'DC=example,DC=com'  # The base DN to search for groups (change this accordingly)

def get_group_members(conn, group_dn, seen_groups=None):
    if seen_groups is None:
        seen_groups = set()

    if group_dn in seen_groups:
        return []

    seen_groups.add(group_dn)

    # Search for the group's members
    conn.search(search_base=group_dn,
                search_filter='(objectClass=group)',
                search_scope=SUBTREE,
                attributes=['member'])

    group_members = []
    for entry in conn.entries:
        if 'member' in entry:
            for member in entry.member.values:
                group_members.append(member)
                # Check if the member is a group itself
                if 'CN=' in member and 'OU=' in member:  # Adjust this condition as needed to detect group DNs
                    group_members.extend(get_group_members(conn, member, seen_groups))

    return group_members


def query_ad_groups(ldap_server, ldap_username, ldap_password, search_base, group_list):
    try:
        # Connect to the LDAP server
        server = Server(ldap_server, get_info=ALL)
        conn = Connection(server, user=ldap_username, password=ldap_password, auto_bind=True)

        all_group_members = {}

        for group_cn in group_list:
            # Construct the group's distinguished name (DN)
            group_dn = f'CN={group_cn},{search_base}'
            print(f"Querying members of group: {group_dn}")

            # Get members recursively
            members = get_group_members(conn, group_dn)
            all_group_members[group_cn] = members

        conn.unbind()
        return all_group_members

    except LDAPException as e:
        print(f"LDAP error: {e}")
        return None


if __name__ == "__main__":
    # Prompt the user for login credentials
    username = input("Enter your AD username: ")
    password = getpass.getpass("Enter your AD password: ")

    # List of groups to query
    group_list = ['Group1', 'Group2', 'Group3']  # Replace with your groups

    # Query the AD for the group members
    group_members = query_ad_groups(AD_SERVER, username, password, AD_SEARCH_BASE, group_list)

    if group_members:
        for group, members in group_members.items():
            print(f"Members of {group}:")
            for member in members:
                print(f" - {member}")
