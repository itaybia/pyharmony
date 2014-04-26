#!/usr/bin/env python2

"""Command line utility for querying the Logitech Harmony."""

import argparse
import logging
import pprint
import sys

from harmony import auth, client as harmony_client, HarmonyConnectionClient, HarmonyConnectionServer


def login_to_logitech(args):
    """Logs in to the Logitech service.

    Args:
      args: argparse arguments needed to login.

    Returns:
      Session token that can be used to log in to the Harmony device.
    """
    token = auth.login(args.email, args.password)
    if not token:
        sys.exit('Could not get token from Logitech server.')

    session_token = auth.swap_auth_token(
        args.harmony_ip, args.harmony_port, token)
    if not session_token:
        sys.exit('Could not swap login token for session token.')

    return session_token


def show_devices(args):
    """Connects to the Harmony and prints its configuration."""
    token = login_to_logitech(args)
    client = harmony_client.create_and_connect_client(
        args.harmony_ip, args.harmony_port, token)
    
    deviceListFile = open("d:\devices_list.txt", 'w')
    client.get_config()
    deviceListFile.write(client.get_config())
    #deviceListFile.write(str(client.get_config()))
    deviceListFile.close()
    client.disconnect(send_close=True)
    return 0

def show_current_activity(args):
    """Connects to the Harmony and prints the current activity."""
    token = login_to_logitech(args)
    client = harmony_client.create_and_connect_client(
        args.harmony_ip, args.harmony_port, token)
    pprint.pprint(client.get_current_activity())
    client.disconnect(send_close=True)
    return 0

def start_activity(args):
    """Connects to the Harmony and prints the current activity."""
    token = login_to_logitech(args)
    client = harmony_client.create_and_connect_client(
        args.harmony_ip, args.harmony_port, token)
    pprint.pprint(client.start_activity(args.activity_id))
    client.disconnect(send_close=True)
    return 0

def send_command_to_device(args):
    """Connects to the Harmony and prints the current activity."""
    token = login_to_logitech(args)
    client = harmony_client.create_and_connect_client(
        args.harmony_ip, args.harmony_port, token)
    pprint.pprint(client.send_button_press_to_device(args.command, args.device_id))
    client.disconnect(send_close=True)
    return 0

def start_tcp_client(args):
    tClient = HarmonyConnectionClient.ClientThread([56213])
    tClient.start()
    return tClient

def start_tcp_server(args):
    tServer = HarmonyConnectionServer.ServerThread([56213])
    tServer.start()
    return tServer

def start_tcp_test(args):
    client_thread = start_tcp_client(args)
    server_thread = start_tcp_server(args)
    client_thread.join()
    server_thread.stop_server_loop()
    server_thread.join()
    return


def main():    
    """Main method for the script."""
    parser = argparse.ArgumentParser(
        description='pyharmony utility script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Required flags go here.
    required_flags = parser.add_argument_group('required arguments')
    required_flags.add_argument('--email', required=True, help=(
        'Logitech username in the form of an email address.'))
    required_flags.add_argument(
        '--password', required=True, help='Logitech password.')
    required_flags.add_argument(
        '--harmony_ip', required=True, help='IP Address of the Harmony device.')

    # Flags with defaults go here.
    parser.add_argument('--harmony_port', default=5222, type=int, help=(
        'Network port that the Harmony is listening on.'))
    loglevels = dict((logging.getLevelName(level), level)
                     for level in [10, 20, 30, 40, 50])
    parser.add_argument('--loglevel', default='INFO', choices=loglevels.keys(),
        help='Logging level to print to the console.')

    subparsers = parser.add_subparsers()
    
    list_devices_parser = subparsers.add_parser(
        'show_devices', help='Print the Harmony device configuration.')
    list_devices_parser.set_defaults(func=show_devices)

    cur_activity_parser = subparsers.add_parser(
        'show_current_activity', help='Print the current activity.')
    cur_activity_parser.set_defaults(func=show_current_activity)
    
    start_activity_parser = subparsers.add_parser(
        'start_activity', help='start a specific activity.')
    start_activity_parser.add_argument(
        '--activity_id', required=True, help='Activity to start.')
    start_activity_parser.set_defaults(func=start_activity)
    
    send_command_to_device_parser = subparsers.add_parser(
        'send_command_to_device', help='send a command to a specific command.')
    send_command_to_device_parser.add_argument(
        '--device_id', required=True, help='Device to send a command to.')
    send_command_to_device_parser.add_argument(
        '--command', required=True, help='the command to perform.')
    send_command_to_device_parser.set_defaults(func=send_command_to_device)

    tcp_client_parser = subparsers.add_parser(
        'start_tcp_client', help='start the TCP client loop.')
    tcp_client_parser.set_defaults(func=start_tcp_client)

    tcp_server_parser = subparsers.add_parser(
        'start_tcp_server', help='start the TCP server loop.')
    tcp_server_parser.set_defaults(func=start_tcp_server)

    tcp_test_parser = subparsers.add_parser(
        'start_tcp_test', help='start the TCP test.')
    tcp_test_parser.set_defaults(func=start_tcp_test)
    
    

    args = parser.parse_args()

    logging.basicConfig(
        level=loglevels[args.loglevel],
        format='%(levelname)s\t%(name)s\t%(message)s')

    sys.exit(args.func(args))


if __name__ == '__main__':
    main()
