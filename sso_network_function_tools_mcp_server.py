#fastmcp dev sso_network_function_tools_mcp_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("NetworkTools")

@mcp.tool()
def detect_device_type(ip: str, username: str, password: str) -> str:
    """Detect device type for a given IP, username, and password."""
    from netmiko import ConnectHandler, redispatch
    import time
    import re
    IDENTIFY_COMMANDS = ['show version', 'display version']

    try:
        server = {
            'device_type': 'terminal_server',
            'host': '10.1.100.88',
            'username': username,
            'password': password,
            'port': 22,
            'conn_timeout': 80,
            'global_delay_factor': 40,
            'session_log': 'output.log'
        }

        jump_conn = ConnectHandler(**server)
    except Exception as e:
        result= f'ip:{ip},  sso_ssh:False, device_ssh:False, device_type:False'
        return str(result)
    else:
        try:
            # Hedef remote_host'a SSH bağlantı denemesi
            jump_conn.write_channel(f"ssh {username}@{ip}\n")
            time.sleep(2)
            # Handle the password prompt
            jump_conn.read_until_pattern(pattern=r"Password|password|PASSWORD:", read_timeout=50)
            jump_conn.write_channel(f"{password}\n")
            time.sleep(1)
            read_for_sso_problems = jump_conn.read_channel()
            sso_problems=["Received disconnect from","Disconnected from"]
            for x in sso_problems:
                if x in read_for_sso_problems:
                    raise ValueError()
            redispatch(jump_conn, device_type='autodetect')
            time.sleep(1)
            device_type = None
            for cmd in IDENTIFY_COMMANDS:
                output=jump_conn.send_command(cmd)
                if 'Huawei' in output or 'HUAWEI' in output:
                    device_type = 'huawei'
                    break
                elif 'Cisco' in output:
                    if 'Cisco IOS-XE software,' in output or 'IOS-XE ROMMON' in output:
                        device_type = 'cisco_xe'
                        break
                    elif 'Cisco IOS Software' in output:
                        device_type = 'cisco_ios'
                        break
                    elif 'Cisco Nexus Operating System' in output:
                        device_type = 'cisco_nxos'
                        break
                    elif 'Cisco IOS XR Software' in output:
                        device_type = 'cisco_xr'
                        break
                elif 'Arista' in output:
                    device_type = 'arista_eos'
                    break
            if device_type:
                result= f'ip:{ip},sso_ssh:True, device_ssh:True, device_type:{device_type}'
                return str(result)
            if not device_type:
                result= f'ip:{ip},sso_ssh:True, device_ssh:True, device_type:{device_type}'
                return str(result)
        except Exception as e:
            result= f'ip:{ip},sso_ssh:True, device_ssh:False, device_type:False'
            return str(result)
        finally:
            jump_conn.disconnect()

@mcp.tool()
def backup_device(ip: str, username: str, password: str) -> str:
    """Get backup for a given IP, username, password"""
    from netmiko import ConnectHandler, redispatch
    import time
    import re
    import os
    from datetime import datetime
    IDENTIFY_COMMANDS = ['show version', 'display version']

    try:
        server = {
            'device_type': 'terminal_server',
            'host': '10.1.100.88',
            'username': username,
            'password': password,
            'port': 22,
            'conn_timeout': 80,
            'global_delay_factor': 40,
            'session_log': 'output.log'
        }

        jump_conn = ConnectHandler(**server)
    except Exception as e:
        result= f'ip:{ip},  sso_ssh:False, device_ssh:False, device_type:False'
        return str(result)
    else:
        try:
            # Hedef remote_host'a SSH bağlantı denemesi
            jump_conn.write_channel(f"ssh {username}@{ip}\n")
            time.sleep(2)
            # Handle the password prompt
            jump_conn.read_until_pattern(pattern=r"Password|password|PASSWORD:", read_timeout=50)
            jump_conn.write_channel(f"{password}\n")
            time.sleep(1)
            read_for_sso_problems = jump_conn.read_channel()
            sso_problems=["Received disconnect from","Disconnected from"]
            for x in sso_problems:
                if x in read_for_sso_problems:
                    raise ValueError()
            redispatch(jump_conn, device_type='autodetect')
            time.sleep(1)
            device_type = None
            for cmd in IDENTIFY_COMMANDS:
                output=jump_conn.send_command(cmd)
                if 'Huawei' in output or 'HUAWEI' in output:
                    device_type = 'huawei'
                    output_backup=jump_conn.send_command('display current-configuration')
                    now=datetime.now()
                    backup=f'{ip}_{device_type}_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}'
                    with open(f'{backup}.txt','w') as f:
                        f.write(output_backup)
                    result=f'{backup}.txt at folder:{os.getcwd()}'
                    return str(result)
                    break

                elif 'Cisco' in output or 'Arista' in output:
                    if 'Cisco IOS-XE software,' in output or 'IOS-XE ROMMON' in output:
                        device_type = 'cisco_xe'
                    elif 'Cisco IOS Software' in output:
                        device_type = 'cisco_ios'
                    elif 'Cisco Nexus Operating System' in output:
                        device_type = 'cisco_nxos'
                    elif 'Cisco IOS XR Software' in output:
                        device_type = 'cisco_xr'
                    elif 'Arista' in output:
                        device_type = 'arista_eos'
                    output_backup=jump_conn.send_command('show run')
                    now=datetime.now()
                    backup=f'{ip}_{device_type}_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}'
                    with open(f'{backup}.txt','w') as f:
                        f.write(output_backup)
                    result=f'{backup}.txt at folder:{os.getcwd()}'
                    return str(result)
                    break

            if not device_type:
                result= f'ip:{ip},sso_ssh:True, device_ssh:True, device_type:{device_type}. Backup could not be taken'
                return str(result)
        except Exception as e:
            result= f'ip:{ip},sso_ssh:True, device_ssh:False, device_type:False. Backup could not be taken.'
            return str(result)
        finally:
            jump_conn.disconnect()


if __name__ == "__main__":
    mcp.run(transport="stdio")
