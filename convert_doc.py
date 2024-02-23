import re
import json

import click
import fitz


def convert_page_to_text(page):
    text = page.get_text().replace("\n", " ")
    return re.sub(r"\s+", " ", text)


def convert_doc_to_json(input_file):
    doc_data = []
    with fitz.open(input_file) as doc:
        for page in doc:
            page_text = convert_page_to_text(page)
            doc_data.append({"page_number": page.number + 1, "text": page_text})
    return doc_data


@click.command()
@click.option(
    "--input-file",
    "-i",
    help="Input document file path",
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--output-file", "-o", help="Output file path", required=True, type=click.Path()
)
@click.option(
    "--output-format",
    "-f",
    help="Output format (text or json)",
    default="text",
    type=click.Choice(["text", "json"]),
)
def convert_doc(input_file, output_file, output_format):
    if output_format == "text":
        with open(output_file, "w") as f:
            with fitz.open(input_file) as doc:
                for page in doc:
                    text = convert_page_to_text(page)
                    f.write(text)
                    f.write("\n")
    elif output_format == "json":
        json_data = convert_doc_to_json(input_file)
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, indent=2, ensure_ascii=False)
    else:
        click.echo("Invalid output format. Choose 'text' or 'json'.")


if __name__ == "__main__":
    convert_doc()
