import click
from colorama import init, Fore, Back, Style
from sleuth_kit.api.transpose import query_ethereum_account, query_ethereum_transactions
from sleuth_kit.helpers.storage import save_to_csv, save_to_sqlite
from sleuth_kit.helpers.setup_schema import setup_database_schema
from sleuth_kit.config import Config, save_api_key
from tqdm import tqdm
import os

init(autoreset=True)  # Initialize colorama

SLEUTH_LOGO = '''
███████╗██╗     ███████╗██╗   ██╗████████╗██╗  ██╗    ██╗  ██╗██╗████████╗
██╔════╝██║     ██╔════╝██║   ██║╚══██╔══╝██║  ██║    ██║ ██╔╝██║╚══██╔══╝
███████╗██║     █████╗  ██║   ██║   ██║   ███████║    █████╔╝ ██║   ██║   
╚════██║██║     ██╔══╝  ██║   ██║   ██║   ██╔══██║    ██╔═██╗ ██║   ██║   
███████║███████╗███████╗╚██████╔╝   ██║   ██║  ██║    ██║  ██╗██║   ██║   
╚══════╝╚══════╝╚══════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝   ╚═╝   
'''

def print_step(step, message):
    click.echo(f"{Fore.YELLOW}[Step {step}]{Fore.RESET} {message}")

@click.group(invoke_without_command=True)
@click.pass_context
def sleuth(ctx):
    """
    Sleuth is a command-line tool for blockchain investigations.
    """
    if ctx.invoked_subcommand is None:
        click.echo(Fore.CYAN + Style.BRIGHT + SLEUTH_LOGO)
        click.echo(Fore.GREEN + "Sleuth Kit is a flexible and extensible toolkit for blockchain investigation and intelligence gathering.")
        click.echo("\n" + Fore.YELLOW + Style.BRIGHT + "Setup:")
        click.echo(Fore.WHITE + "To setup Sleuth Kit, run: " + Fore.MAGENTA + "sleuth setup")
        click.echo("\n" + Fore.YELLOW + Style.BRIGHT + "Options and Usage:")
        click.echo(Fore.WHITE + "- " + Fore.MAGENTA + "sleuth accounts -address <address>" + Fore.WHITE + ": Query Ethereum account details")
        click.echo(Fore.WHITE + "- " + Fore.MAGENTA + "sleuth transactions -address <address>" + Fore.WHITE + ": Query Ethereum transactions")
        click.echo(Fore.WHITE + "- " + Fore.MAGENTA + "sleuth secrets transpose <key>" + Fore.WHITE + ": Set Transpose API key")

        if not Config.TRANSPOSE_API_KEY:
            click.echo(Fore.RED + "\nWarning: Transpose API key is not set. Please run 'sleuth setup' or 'sleuth secrets transpose <key>' to set it.")
    else:
        setup_database_schema()

@sleuth.command()
@click.option('-address', required=True, help='Ethereum addresses to query (comma-separated)')
def accounts(address):
    """
    Query Ethereum account details using the provided addresses.
    """
    try:
        addresses = [addr.strip() for addr in address.split(',')]
        print_step(1, f"Querying Ethereum account details for {len(addresses)} address(es)")
        
        for addr in addresses:
            data = query_ethereum_account(addr)
            
            if Config.SAVE_AS_CSV:
                print_step(2, f"Saving data to CSV for address {addr}")
                save_to_csv(data, 'data/csv/ethereum-accounts.csv', ['address', 'created_timestamp', 'creator_address', 'last_active_timestamp', 'type'])
            
            if Config.SAVE_AS_SQLITE:
                print_step(3, f"Saving data to SQLite for address {addr}")
                save_to_sqlite(data, 'ethereum_accounts')
            
            click.echo(Fore.GREEN + f"\nRetrieved account data for address {addr}")
        
    except Exception as e:
        click.echo(Fore.RED + f"An error occurred while querying account data: {str(e)}")

@sleuth.command()
@click.option('-address', required=True, help='Ethereum addresses to query transactions for (comma-separated)')
def transactions(address):
    """
    Query Ethereum transactions for the provided addresses.
    """
    try:
        addresses = [addr.strip() for addr in address.split(',')]
        print_step(1, f"Querying Ethereum transactions for {len(addresses)} address(es)")
        
        with tqdm(total=len(addresses), desc="Fetching transactions", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            data = query_ethereum_transactions(addresses)
            pbar.update(1)
        
        if not data:
            click.echo(Fore.YELLOW + f"No transactions found for the provided address(es)")
            return

        total_transactions = len(data)
        with tqdm(total=total_transactions, desc="Processing transactions", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            for transaction in data:
                if Config.SAVE_AS_CSV:
                    save_to_csv([transaction], 'data/csv/ethereum-transactions.csv', list(transaction.keys()))
                if Config.SAVE_AS_SQLITE:
                    save_to_sqlite([transaction], 'ethereum_transactions')
                pbar.update(1)

        click.echo(Fore.GREEN + f"\nRetrieved and processed {total_transactions} transactions for {len(addresses)} address(es)")
    except Exception as e:
        click.echo(Fore.RED + f"An error occurred while querying transactions: {str(e)}")
        click.echo(Fore.YELLOW + "Please check your input and try again.")

@sleuth.command()
def setup():
    """
    Set up the database schema and configure API keys.
    """
    print_step(1, "Setting up database schema")
    setup_database_schema()
    click.echo(Fore.GREEN + "Database schema set up successfully.")

    print_step(2, "Configuring API keys")
    if not Config.TRANSPOSE_API_KEY:
        click.echo(Fore.YELLOW + "Transpose API key is not set.")
        key = click.prompt("Please enter your Transpose API key", type=str)
        save_api_key('TRANSPOSE_API_KEY', key)
        click.echo(Fore.GREEN + "Transpose API key saved successfully.")
    else:
        click.echo(Fore.GREEN + "Transpose API key is already set.")

@sleuth.command()
@click.argument('service')
@click.argument('key')
def secrets(service, key):
    """
    Set API keys for different services.
    """
    if service.lower() == 'transpose':
        save_api_key('TRANSPOSE_API_KEY', key)
        click.echo(Fore.GREEN + "Transpose API key saved successfully.")
    else:
        click.echo(Fore.RED + f"Unknown service: {service}")

if __name__ == '__main__':
    sleuth()