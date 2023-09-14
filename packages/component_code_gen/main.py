import os
import argparse
import templates.generate_actions
import templates.generate_webhook_sources
import templates.generate_polling_sources
import templates.generate_apps


available_templates = {
    'action': templates.generate_actions,
    'webhook_source': templates.generate_webhook_sources,
    'polling_source': templates.generate_polling_sources,
    'app': templates.generate_apps,
}


def main(component_type, app, instructions, tries, verbose=False):
    if verbose:
        os.environ['LOGGING_LEVEL'] = 'DEBUG'

    validate_inputs(app, component_type, instructions, tries)

    templates = available_templates[component_type]
    parsed_common_files = parse_common_files(app, component_type)

    validate_system_instructions(templates)

    # this is here so that the DEBUG environment variable is set before the import
    from code_gen.generate_component_code import generate_code
    result = generate_code(app, instructions, templates, parsed_common_files, tries)
    return result


def parse_common_files(app, component_type):
    file_list = []
    app_path = f'../../components/{app}'

    if "source" in component_type:
        component_type = "source"

    for root, _, files in os.walk(app_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if "dist/" in filepath or "node_modules/" in filepath:
                continue
            if "actions/" in filepath or "sources/" in filepath:
                if component_type == "app":
                    continue
                elif component_type in filepath and "common" in filepath:
                    file_list.append(filepath)
            else:
                if filepath.endswith(".mjs") or filepath.endswith(".ts"):
                    file_list.append(filepath)

    parsed_common_files = ""
    for common_file in file_list:
        with open(common_file, 'r') as f:
            common_file = common_file.split(f"{app}/")[1]
            parsed_common_files += f'### {common_file}\n\n{f.read()}\n'
    return parsed_common_files


def validate_inputs(app, component_type, instructions, tries):
    assert component_type in available_templates.keys(), f'Templates for {component_type}s are not available. Please choose one of {list(available_templates.keys())}'
    assert app and type(app) == str
    assert instructions and type(instructions) == str
    assert tries and type(tries) == int


def validate_system_instructions(templates):
    assert templates.system_instructions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', help='Which kind of code you want to generate?',
                        choices=available_templates.keys(), required=True)
    parser.add_argument('--app', help='The app_name_slug', required=True)
    parser.add_argument(
        '--instructions', help='Markdown file with instructions: prompt + api docs', required=True)
    parser.add_argument('--num_tries', dest='tries', help='The number of times we call the model to generate code',
                        required=False, default=3, type=int)
    parser.add_argument('--verbose', dest='verbose', help='Set the logging to debug',
                        required=False, default=False, action='store_true')
    args = parser.parse_args()

    with open(args.instructions, 'r') as f:
        instructions = f.read()

    result = main(args.type, args.app, instructions, args.tries, args.verbose)
    print(result)
