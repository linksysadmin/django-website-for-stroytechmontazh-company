import logging

from jinja2 import Environment, FileSystemLoader

from config import BASE_DIR


logger = logging.getLogger()


def render(template: str, context: dict):
    templateLoader = FileSystemLoader(searchpath=f"{BASE_DIR}/templates/")
    templateEnv = Environment(loader=templateLoader)
    template_ = templateEnv.get_template(template)
    generated_text = template_.render(context)
    return generated_text


