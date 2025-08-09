# PyStand build

Automatically deploy your Python project with PyStand!

## Parameters

### Inputs

| Parameter            | Type   | Required | Default      | Description                                                                                                                                                                                             |
| -------------------- | ------ | -------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `application-name`   | string | ✔        | —            | The application name of standalone package. |
| `application-type`   | string | ✖        | `GUI`        | Application type. Must be `GUI` or `CLI`. |
| `python-version`     | string | ✖        | `3.11.9`     | The target Python embedded version to use. |
| `pystand-entry-file` | string | ✖        | `PyStand.py` | The entry file path for PyStand. |
| `requirements-path`  | string | ✔        | —            | The path to the requirements.txt file. |
| `included-files`     | string | ✔        | —            | Newline-separated list of files/directories.<br>- **Directories** → copied to `<build-directory>/<dir-name>`<br>- **Files** → copied to the root of `<build-directory>` |

### Outputs

| Name              | Type   | Description |
|-------------------|--------|-------------|
| `build-directory` | string | Absolute path to the fully-prepared build directory.<br>Use it for archiving, installer generation, etc.<br>Retrieve with `${{ steps.<id>.outputs.build-directory }}`. |
