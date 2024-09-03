"""
Developed at Karlsruhe Institute of Technology (KIT), December 2019
This script uses pymongo commands to automate user management of mongodb instances.
"""
import argparse
import getpass
from bson.json_util import dumps
from pymongo import MongoClient


def pass_set():
    """Return a set password with password retype checking."""
    pwd = -999
    re_pwd = 111
    while pwd != re_pwd:
        pwd = getpass.getpass('New password for user: ')
        re_pwd = getpass.getpass('Re-type password: ')
        if pwd == re_pwd:
            return pwd
        print('Passwords do not match, try again: ')
    return None


def main():
    """the main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True,
                        help='Hostname of MongoDB instance')
    parser.add_argument('--cacert', required=True,
                        help='Path to CA certificate')
    parser.add_argument('--clcert', default=None, required=False,
                        help='Path to client certificate')
    args = parser.parse_args()
    opt = 0

    while True:
        try:
            print('\nYour login credentials for '+args.host+':\n')
            x509 = input('Do you use x509 authentication? [no/yes]\n' +
                         '(press "Enter" if you don\'t know or "0" to quit): ')
            assert x509.lower() in ['yes', 'no', '', '0']
            if x509.lower() == 'yes':
                certkeyfile = input('Locate your certificate/key file: ')
                client = MongoClient(host=args.host, authSource='$external',
                                     tlsCertificateKeyFile=certkeyfile,
                                     tlsCAFile=args.cacert, tls=True,
                                     authMechanism='MONGODB-X509')
                db = client['$external']
                client.server_info()
            elif x509.lower() in ['no', '']:
                db_auth = input('Your authentication database: ')
                user_auth = input('Your username to login: ')
                pwd_auth = getpass.getpass(f'Your password for {user_auth}: ')
                client = MongoClient(host=args.host, username=user_auth,
                                     authSource=db_auth, password=pwd_auth,
                                     tlsCertificateKeyFile=args.clcert,
                                     tlsCAFile=args.cacert, tls=True)
                db = client[db_auth]
                client.server_info()
            elif x509 == '0':
                opt = 'quit'
            break
        except Exception as err:
            print(err)

    while opt != 'quit':
        try:
            choice = input("""
        1: Create user
        2: Change password
        3: Remove user
        4: Grant a role to user
        5: Revoke a role from user
        6: Show users
        7: List available databases
        8: Create a database
        9: Drop a database
        0: Quit/Log out

        your choice (0 for Quit): """)

            if choice == '1':
                opt = 'createUser'
            elif choice == '2':
                opt = 'updatePass'
            elif choice == '3':
                opt = 'dropuser'
            elif choice == '4':
                opt = 'grant'
            elif choice == '5':
                opt = 'revoke'
            elif choice == '6':
                opt = 'showusers'
            elif choice == '7':
                opt = 'listdb'
            elif choice == '8':
                opt = 'createdb'
            elif choice == '9':
                opt = 'dropdb'
            elif choice == '0':
                opt = 'quit'
            else:
                raise Exception('WrongChoice')

            if opt == 'createUser':
                try:
                    x509_newuser = input('Do you use X509 authentication for new user [no/yes]: ')
                    if x509_newuser == 'yes':
                        subject_dn = input('Subject DN of new user: ')
                        role_newuser = input('Role of new user: ')
                        db = client['$external']
                        db.command({'createUser': subject_dn,
                                    'roles': [{'role': role_newuser, 'db': 'admin'}]})
                        print(f'\n {subject_dn} is created for admin database with {role_newuser} role.')
                    else:
                        new_user = input('New username: ')
                        db_sibling_in = input('Authentication database of new user: ')
                        db_sibling = client[db_sibling_in]
                        pass_newuser = pass_set()
                        role_newuser = input('Role of new user: ')
                        db_sibling.command(opt, new_user, pwd=pass_newuser,
                                           roles=[{'role': role_newuser, 'db': db_sibling_in}])
                        print(f'\n {new_user} is created for {db_sibling} database with {role_newuser} role.')
                except Exception as err:
                    print(err)

            elif opt == 'updatePass':
                try:
                    user_update = input('Username to update the password: ')
                    db_sibling_in = input('Authentication database of user: ')
                    db_sibling = client[db_sibling_in]
                    pass_newuser = pass_set()
                    db_sibling.command('updateUser', user_update, pwd=pass_newuser)
                    print(f'\n Password is changed successfully for {user_update}.')
                except Exception as err:
                    print(err)

            elif opt == 'dropuser':
                try:
                    user_drop = input('Username to be removed: ')
                    db_sibling_in = input(f'Authentication database of {user_drop}: ')
                    db_sibling = client[db_sibling_in]
                    db_sibling.command('dropUser', user_drop)
                    print(f'The user {user_drop} is removed from {db_sibling_in} database.')
                except Exception as err:
                    print(err)

            elif opt == 'grant':
                try:
                    user_grant = input('Username to be granted: ')
                    db_sibling_in = input('Authentication database of user: ')
                    db_sibling = client[db_sibling_in]
                    target_db = input('Database for which new role will be granted, target database: ')
                    new_role = input(f'New role for {user_grant}: ')
                    db_sibling.command('grantRolesToUser', user_grant,
                                       roles=[{'role': new_role, 'db': target_db}])
                    print(f'\n The {new_role} role is granted to {user_grant} on {target_db} database.')
                except Exception as err:
                    print(err)

            elif opt == 'revoke':
                try:
                    user_revoked = input('Username to revoke a role from: ')
                    db_sibling_in = input('Authentication database of user: ')
                    db_sibling = client[db_sibling_in]
                    target_db = input('Database for which role will be revoked, target database:')
                    role_drop = input('Role to be revoked from {user_revoked}: ')
                    db_sibling.command('revokeRolesFromUser', user_revoked,
                                       roles=[{'role': role_drop, 'db': target_db}])
                    print(f'\n The {role_drop} role is revoked from {user_revoked} on {target_db} database.')
                except Exception as err:
                    print(err)

            elif opt == 'showusers':
                try:
                    db_sibling_in = input('Database to print: ')
                    db_sibling = client[db_sibling_in]
                    command_exit = db_sibling.command('usersInfo')
                    print(dumps(command_exit, indent=4))
                except Exception as err:
                    print(err)

            elif opt == 'listdb':
                try:
                    db_sibling = client['admin']
                    command_exit = db_sibling.command('listDatabases')
                    print(dumps(command_exit, indent=4))
                except Exception as err:
                    print(err)

            elif opt == 'createdb':
                try:
                    db_name = input('Name of new database: ')
                    db_sibling = client[db_name]
                    privs = [{'resource': {'db': db_name, 'collection': ''},
                              'actions': ['changeOwnPassword']}]
                    command_exit = db_sibling.command('createRole',
                                                      'changeOwnPassword',
                                                      privileges=privs,
                                                      roles=[])
                    print(dumps(command_exit, indent=4))
                except Exception as err:
                    print(err)

            elif opt == 'dropdb':
                try:
                    db_name = input('Database to drop: ')
                    db_sibling = client[db_name]
                    command_exit = db_sibling.command('dropAllUsersFromDatabase')
                    print(dumps(command_exit, indent=4))
                    client.drop_database(db_name)
                except Exception as err:
                    print(err)

        except Exception:
            print('Wrong choice. Please try again.')
