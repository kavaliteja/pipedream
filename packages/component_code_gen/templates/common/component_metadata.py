# ---------------------------- action example ---------------------------- #
action_example = """```
export default {
  key: "google_drive-list-all-drives",
  name: "List All Drives",
  description: "Lists all drives in an account.",
  version: "0.0.{{ts}}",
  type: "action",
};
```"""


# ---------------------------- source example ---------------------------- #
source_example = """```
export default {
  key: "google_drive-new-shared-drive-created",
  name: "New Shared Drive Created",
  description: "Emits a new event any time a shared drive is created.",
  version: "0.0.{{ts}}",
  type: "source",
  dedupe: "unique",
};
```"""


# ---------------------------- component metadata ---------------------------- #
component_metadata = """## Component Metadata

Registry components require a unique key and version, and a friendly name and description. E.g.

{example}

Component keys are in the format app_name_slug-slugified-component-name.
You should come up with a name and a description for the component you are generating.
In the description, you should include a link to the app docs, if they exist. Or add this as a placeholder: [See docs here]().
Action keys should use active verbs to describe the action that will occur, (e.g., linear_app-create-issue).
Always add version "0.0.{{ts}}".
Always put {component_type}.
You MUST add metadata to the component code you generate."""


# ---------------------------- action metadata ---------------------------- #
action_metadata = component_metadata.format(
    example=action_example, component_type='"type": "action"')


# ---------------------------- source metadata ---------------------------- #
source_metadata = component_metadata.format(
    example=source_example, component_type='"type": "source" and "dedupe": "unique"')
