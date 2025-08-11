# PyStand build

Automatically deploy your Python project with PyStand!

## Use Example

```yaml
jobs:
  build:
    runs-on: windows-latest
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build Python Application Standalone Package
        id: pystand-build
        uses: BHznJNs/pystand-build@release-6
        with:
          application-name: "YourApplicationName"
          python-version: "3.11.9"
          requirements-path: "backend/requirements.txt"
          included-files: |
            backend/ # this is the python source directory
            # there can be other assets files or directories here

      - name: Create Zip Archive
        shell: bash
        run: |
          build_path="${{ steps.pystand-build.outputs.build-directory }}"
          (cd "$build_path" && 7z a -tzip "$RUNNER_TEMP/YouApplicationName.zip" .)

      # upload package with `${{ runner.temp }}/YouApplicationName.zip`
```

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
