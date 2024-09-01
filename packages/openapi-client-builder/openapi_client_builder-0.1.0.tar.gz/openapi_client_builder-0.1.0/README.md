# `openapi-client-builder`

**Usage**:

```console
$ api-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `api`
* `type`

## `api-cli api`

**Usage**:

```console
$ api-cli api [OPTIONS]
```

**Options**:

* `--host TEXT`: [default: 127.0.0.1]
* `--port TEXT`: [default: 8000]
* `--path TEXT`: [default: /api/openapi.json]
* `--url TEXT`
* `--output TEXT`: [default: ./dist]
* `--name TEXT`: [default: db_api.d.ts]
* `--help`: Show this message and exit.

## `api-cli type`

**Usage**:

```console
$ api-cli type [OPTIONS]
```

**Options**:

* `--host TEXT`: [default: 127.0.0.1]
* `--port TEXT`: [default: 8000]
* `--path TEXT`: [default: /api/openapi.json]
* `--url TEXT`
* `--output TEXT`: [default: ./dist]
* `--name TEXT`: [default: api.types.d.ts]
* `--help`: Show this message and exit.
