#!/usr/bin/env python
# encoding: utf-8

import questionary
from prompt_toolkit.styles import Style
from . import *

style = Style(
    [
        ("separator", "fg:#6C6C6C"),
        ("qmark", "fg:#FF9D00 bold"),
        ("question", ""),
        ("selected", "fg:#2e82c7 bg:#d9d9d9"),
        ("pointer", "fg:#FF9D00 bold"),
        ("answer", "fg:#2e9dd1 bold bg:#363636"),
    ]
)


def main():
    generator = questionary.autocomplete(
        "What do you want to generate?",
        choices=[
            "Apache Config",
        ],
        style=style,
    ).ask()

    if generator == "Apache Config":
        gen = ApacheConfigGenerator()

        apache_path: str = questionary.path(
            "Where is apache2 located?",
            default="/etc/apache2",
            style=style,
        ).ask()
        if apache_path == None:
            print("Failed to generate: missing apache path!")
            exit(1)

        domains: str = questionary.text(
            "What domains to you want to serve? (Seperated by commas)",
            default="example.com",
            style=style,
        ).ask()
        if domains == None:
            print("Failed to generate: missing domain(s)!")
            exit(1)

        web_loc = questionary.path(
            "What is the path of your website files? (Optional)",
            default="",
            style=style,
        ).ask()
        if web_loc == None:
            print("Failed to generate: missing webroot!")
            exit(1)

        uri_to_forward = questionary.text(
            "What URI do you want to proxy to? (Optional)",
            default="",
            style=style,
        ).ask()
        if uri_to_forward == None:
            print("Failed to generate: missing proxy URI!")
            exit(1)

        if apache_path != "" and domains != "":
            gen.generate(
                apache_path=apache_path,
                domains=domains,
                uri_to_forward=uri_to_forward,
                web_loc=web_loc,
            )
        else:
            print("Failed to generate: missing answers!")
    else:
        print("Nothing to generate, exiting...")
