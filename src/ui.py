from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from src.session_manager import SessionManager

console = Console()

class UI:
    """Terminal UI with Rich"""
    
    @staticmethod
    def show_banner():
        """Display welcome banner"""
        banner = """
    ████████╗███████╗██╗     ███████╗ ██████╗ ██████╗ █████╗ ███╗   ███╗
    ╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝██╔════╝██╔══██╗████╗ ████║
       ██║   █████╗  ██║     █████╗  ██║     ██║     ███████║██╔████╔██║
       ██║   ██╔══╝  ██║     ██╔══╝  ██║     ██║     ██╔══██║██║╚██╔╝██║
       ██║   ███████╗███████╗███████╗╚██████╗╚██████╗██║  ██║██║ ╚═╝ ██║
       ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝
    """
        console.print(banner, style="bold cyan")
        console.print("[bold green]Telegram Scraper v1.6[/bold green] - By AbirHasan2005")
        console.print()
    
    @staticmethod
    def show_main_menu():
        """Display main menu"""
        menu_items = [
            ("01", "Login Telegram Account"),
            ("02", "Manage Sessions"),
            ("03", "Scrape Group Members"),
            ("04", "Add Members to Group"),
            ("05", "Broadcast Message"),
            ("06", "View Logs"),
            ("07", "Exit"),
        ]
        
        table = Table(title="[bold cyan]Main Menu[/bold cyan]", show_header=False)
        table.add_column("Option", style="cyan", width=10)
        table.add_column("Description", style="green")
        
        for code, desc in menu_items:
            table.add_row(code, desc)
        
        console.print(table)
    
    @staticmethod
    def show_sessions_table(sessions: list):
        """Display sessions table"""
        if not sessions:
            console.print("[yellow]No sessions found[/yellow]")
            return
        
        table = Table(title="[bold cyan]Active Sessions[/bold cyan]")
        table.add_column("Account Name", style="cyan")
        
        for session in sessions:
            table.add_row(session)
        
        console.print(table)
    
    @staticmethod
    def prompt_account_name(msg: str = "Enter account name") -> str:
        """Prompt for account name"""
        return Prompt.ask(f"[cyan]{msg}[/cyan]")
    
    @staticmethod
    def prompt_phone() -> str:
        """Prompt for phone number"""
        return Prompt.ask("[cyan]Enter phone number[/cyan]")
    
    @staticmethod
    def prompt_group_id() -> str:
        """Prompt for group ID or username"""
        return Prompt.ask("[cyan]Enter group ID or username (e.g., -1001234567890 or @groupname)[/cyan]")
    
    @staticmethod
    def prompt_group_input() -> str:
        """Prompt for group identifier (ID or username)"""
        value = Prompt.ask("[cyan]Enter group ID or @username[/cyan]").strip()
        if not value:
            console.print("[red]Invalid input - must provide group ID or username[/red]")
            return None
        return value
    
    @staticmethod
    def prompt_csv_file() -> str:
        """Prompt for CSV file name"""
        return Prompt.ask("[cyan]Enter CSV file name[/cyan]")
    
    @staticmethod
    def confirm(msg: str = "Do you want to continue?") -> bool:
        """Confirm action"""
        return Confirm.ask(f"[cyan]{msg}[/cyan]")
    
    @staticmethod
    def show_success(msg: str):
        """Show success message"""
        console.print(f"[bold green]✓ {msg}[/bold green]")
    
    @staticmethod
    def show_error(msg: str):
        """Show error message"""
        console.print(f"[bold red]✗ {msg}[/bold red]")
    
    @staticmethod
    def show_info(msg: str):
        """Show info message"""
        console.print(f"[bold blue]ℹ {msg}[/bold blue]")
    
    @staticmethod
    def show_warning(msg: str):
        """Show warning message"""
        console.print(f"[bold yellow]⚠ {msg}[/bold yellow]")
