import logging

import click
import logging

import click
from mbpy.mpip import find_and_sort
from minspect.inspecting import inspect_library
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

from msearch.search import search_github, search_huggingface, search_web

custom_theme = Theme({"default": "on white"})
console = Console(theme=custom_theme)
logger = logging.getLogger(__name__)

@click.command()
@click.argument('query', nargs=-1)
@click.option('--engine', '-e', default='web', help='Search engine to use: web, github, inspect, pypi, hf')
def cli(query, engine: str):
    """Search for info on the web, github, pypi, or inspect a library"""
    query = ' '.join(query)
    
    if engine == 'web':
        results = search_web(query)
        if not results:
            console.print(Panel("No results found.", title="Web Search Results"))
        else:
            table = Table(title="Web Search Results", show_header=True, header_style="bold magenta")
            table.add_column("Title", style="cyan", width=40, overflow="fold")
            table.add_column("URL", style="blue", width=40, overflow="fold")
            table.add_column("Snippet", style="green", width=40, overflow="fold")
            for result in results:
                table.add_row(
                    result.get('title', 'No title'),
                    result.get('url', 'No URL'),
                    result.get('snippet', 'No snippet')
                )
            console.print(Panel(table, expand=True))
    elif engine == 'github':
        results = search_github(query)
        if not results['results']:
            console.print(Panel("No results found.", title="GitHub Search"))
        else:
            table = Table(title="GitHub Search Results")
            table.add_column("Repository", style="cyan", no_wrap=True)
            table.add_column("URL", style="magenta")
            table.add_column("Description", style="green")
            table.add_column("Stars", justify="right", style="yellow")
            table.add_column("Forks", justify="right", style="yellow")
            for repo in results['results']:
                table.add_row(repo['name'], repo['html_url'], repo['description'], str(repo['stars']), str(repo['forks']))
            console.print(Panel(table))
    elif engine == 'inspect':
        result = inspect_library(query, depth=1, docs=True, code=False, imports=False, all=False)
        console.print(Panel(f"Inspecting module: {query}", title="Module Inspection"))
        console.print(Panel(result.get('functions', 'No functions found'), title="Functions"))
        console.print(Panel(result.get('classes', 'No classes found'), title="Classes"))
        console.print(Panel(result.get('variables', 'No variables found'), title="Variables"))
    elif engine == "pypi":
        results = find_and_sort(query)
        table = Table(title="PyPI Search Results")
        table.add_column("Package", style="cyan", no_wrap=True)
        table.add_column("Version", style="magenta")
        table.add_column("Description", style="green")
        for package in results:
            table.add_row(package['name'], package['version'], package['summary'])
        console.print(Panel(table))
    elif engine == "hf":
        results = search_huggingface(query)
        if not results:
            console.print(Panel("No results found.", title="HuggingFace Search"))
        else:
            table = Table(title="HuggingFace Search Results", show_header=True, header_style="bold magenta")
            table.add_column("Type", style="cyan", no_wrap=True)
            table.add_column("Name", style="magenta")
            table.add_column("URL", style="blue")
            table.add_column("Downloads", justify="right", style="green")
            table.add_column("Likes", justify="right", style="yellow")
            for item in results:
                table.add_row(item['type'].capitalize(), item['name'], item['url'], str(item['downloads']), str(item['likes']))
            console.print(Panel(table, expand=False))
            console.print(Panel(f"Total results: {len(results)}", title="Summary", style="bold green"))
    else:
        console.print(f"Invalid search engine: {engine}")
        return 1

    return 0

if __name__ == "__main__":
    exit(cli())
