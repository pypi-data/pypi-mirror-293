import click
import httpx
import json
from rich.console import Console
import time
import threading
from tqdm import tqdm
import asyncio
import sys
from itertools import cycle

API_BASE_URL = "https://ceplatform-api.rdpnt.com" 
AUTH_URL = "https://ceplatform-api.rdpnt.com/api/v1/auth/login"
console = Console()

# Get Authentication Token
def get_auth_token(username, password):
    """Request an authentication token from the API."""
    payload = {
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }
    try:
        response = httpx.post(AUTH_URL, data=payload, follow_redirects=True)
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            raise ValueError("Authentication failed, no token returned.")
        return token
    except httpx.RequestError as e:
        console.print(f"An error occurred during authentication: {e}", style="bold red")
        return None
    except ValueError as e:
        console.print(f"{e}", style="bold red")
        return None

# Create progress indicator
def spinner():
    """Display a spinner to indicate progress."""
    spinner_chars = ['|', '/', '-', '\\']
    for char in cycle(spinner_chars):
        if not spinner_running[0]:
            break
        sys.stdout.write(f'\r{char} Processing...')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!')

def post_with_spinner(url, data, headers, retries=3, timeout=120):
    """Post data with retries and show a spinner during the request."""
    global spinner_running
    spinner_running = [True]
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    try:
        response = httpx.post(url, json=data, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except httpx.RequestError as e:
        click.echo(f"Request failed: {e}")
        raise
    finally:
        spinner_running[0] = False
        spinner_thread.join()

def get_with_spinner(url, headers=None, retries=3, timeout=120):
    """Get data with retries and show a spinner during the request."""
    global spinner_running
    spinner_running = [True]
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    try:
        response = httpx.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except httpx.RequestError as e:
        click.echo(f"Request failed: {e}")
        raise
    finally:
        spinner_running[0] = False
        spinner_thread.join()
        
# VM Commandline 
@click.group()
def cepapi():
    """The CEPAPI CLI is a command-line tool designed to provide a seamless interaction with the Redpoint Cloud Engineering Platform API"""
    pass

# Create SQA Virtual Machine
@cepapi.command()
@click.option('--os', prompt='Operating System', help='Operating System for the VM')
@click.option('--expiry', prompt='Expiry in days', help='Expiry duration for the VM', type=int)
@click.option('--requester_name', prompt='Requester Name', help='Name of the requester')
@click.option('--requester_email', prompt='Requester Email', help='Email of the requester')
@click.option('--username', prompt='API Username', help='Username for authentication')
@click.option('--password', prompt='API Password', hide_input=True, help='Password for authentication')

def create_sqa_vm(os, expiry, requester_name, requester_email, username, password):
    """Create new SQA virtual machine."""
    token = get_auth_token(username, password)
    if not token:
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "operating_system": os,
        "expiry": expiry,
        "requester_name": requester_name,
        "requester_email": requester_email
    }

    response = post_with_spinner(f"{API_BASE_URL}/api/v1/rpdm/vm/create", data=payload, headers=headers)
    
    if response.status_code == 201:
        click.echo(f"VM created successfully:\n{json.dumps(response.json(), indent=4)}")
    else:
        click.echo(f"Failed to create VM: {response.text}")

# Get SQA Virtual Machine Status
@cepapi.command()
@click.option('--name', prompt='name', help='Name of the VM')
@click.option('--rg', prompt='resource_group', help='Resource Group of the VM')
def get_sqa_vm(name, rg):
    """Get SQA Vitual Machine details"""

    response = get_with_spinner(f"{API_BASE_URL}/api/v1/rpdm/vm/status/{name}/{rg}")
    
    if response.status_code == 200:
        click.echo(f"VM Status:\n{json.dumps(response.json(), indent=4)}")
    else:
        click.echo(f"Failed to get VM status: {response.text}")

# Get List of SQA Virtual Machines
@cepapi.command()
def list_sqa_vms():
    """Get List of SQA virtual machines."""
    
    response = get_with_spinner(f"{API_BASE_URL}/api/v1/rpdm/vms/list")
    if response.status_code == 200:
        click.echo(f"VM List:\n{json.dumps(response.json(), indent=4)}")
    else: 
        click.echo(f"Failed to get Virtual Machine List: {response.text}")

# Stop Virtual Machine
@cepapi.command()
@click.option('--action', prompt='action', type=click.STRING, help='Allowed values are stop hibernate or deallocate')
@click.option('--vm_name', prompt='vm_name', type=click.STRING, help='Name of the Virtual Machine')
@click.option('--vm_resource_group', prompt='vm_resource_group', type=click.STRING, help='Resource Group of the Virtual Machine')
@click.option('--hibernate', prompt='hibernate', type=click.BOOL, default=False, help='true or false')
def stop_vm(action, vm_resource_group, vm_name, hibernate):
    """Stop Virtual Machine"""
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
        }
    
    payload = {
        "action": action,
        "vm_resource_group": vm_resource_group,
        "vm_name": vm_name,
        "hibernate": hibernate
    }
    
    response = post_with_spinner(f"{API_BASE_URL}/api/v1/rpdm/vm/stop", data=payload, headers=headers)
    
    if response.status_code == 202:
        click.echo(f"VM Stopped Successfully")
    else:
        click.echo(f"Failed to stop Virtual Machine: {response.text}")
 
# Start Virtual Machine
@cepapi.command()
@click.option('--vm_name', prompt='vm_name', type=click.STRING, help='Name of the Virtual Machine')
@click.option('--vm_resource_group', prompt='vm_resource_group', type=click.STRING, help='Resource Group of the Virtual Machine')
def start_vm(vm_name, vm_resource_group):
    """Start Virtual Machine"""
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
        }
    
    payload = {
        "vm_name": vm_name,
        "vm_resource_group": vm_resource_group,
    }
    
    response = post_with_spinner(f"{API_BASE_URL}/api/v1/rpdm/vm/start", data=payload, headers=headers)
    
    if response.status_code == 202:
        click.echo(f"VM Started Successfully")
    else:
        click.echo(f"Failed to Start Virtual Machine: {response.text}")
        
##### CLI Entry Point
if __name__ == '__main__':
    cepapi()

