from rich.console import Console
from rich.panel import Panel
import subprocess
import sys
import os
from mobproxy.core import live_analyze

def start_mitmdump():
    script_path = os.path.abspath("mitm_scripts/intercept.py")
    subprocess.Popen([
        "osascript", "-e",
        f'tell app \"Terminal\" to do script \"cd {os.getcwd()} && source venv/bin/activate && mitmdump -s {script_path}\"'
    ])

def show_banner():
    console = Console()
    console.print(Panel("[bold green]🛡 MobSafe Proxy CLI[/bold green]\n[white]by Rifnas Mohd[/white]",
                        title="Mobile Traffic Analyzer", border_style="green"))

def main():
    console = Console()
    show_banner()

    user_input = input("\n[?] Press [1] and Enter to begin capture and live analysis: ")
    if user_input.strip() != "1":
        console.print("[red]❌ Exiting...[/red]")
        sys.exit(1)

    start_mitmdump()

    console.print("\n[green]✅ mitmdump started in a new terminal.[/green]")
    console.print("[cyan]🧪 To test the proxy, run this in another terminal:[/cyan]\n")
    console.print("[white]curl -x http://localhost:8080 -X POST -d \"username=admin&password=1234\" http://httpbin.org/post[/white]\n")
    console.print("[bold yellow]⚠️  This is a dummy test. Do not use real credentials.[/bold yellow]\n")
    console.print("[cyan]🔍 Now starting real-time log analysis below...[/cyan]\n")

    live_analyze()

if __name__ == "__main__":
    main()
