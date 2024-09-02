import click


@click.command()
@click.option("--count", prompt="How many", help="Number of drinks.", type=int)
@click.option("--name", prompt="Your name", help="The person to greet.")
def get_drink(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Here's your drink, {name}!")


if __name__ == "__main__":
    get_drink()
