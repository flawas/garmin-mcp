"""MCP-Server für die Garmin Connect Personal API."""


def main() -> None:
    """Garmin Connect MCP Server – eigene Garmin-Daten für LLMs, read-only."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="mcp-server-garmin-connect",
        description=(
            "MCP-Server für die Garmin Connect Personal API (stdio). "
            "Der API-Key wird aus GARMIN_PERSONAL_API_KEY gelesen."
        ),
    )
    parser.parse_args()

    from .server import serve

    serve()


if __name__ == "__main__":
    main()
