# gaveta

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

Vanilla utility functions for different projects.

- [Source code](https://gitlab.com/joaommpalmeiro/gaveta)
- [Documentation](https://gaveta.joao.tools/)
- [PyPI package](https://pypi.org/project/gaveta/)
- [Snyk Advisor](https://snyk.io/advisor/python/gaveta)

## Development

Install [pyenv](https://github.com/pyenv/pyenv) (if necessary).

```bash
pyenv install && pyenv versions
```

```bash
pip install hatch==1.9.3 && hatch --version
```

```bash
hatch config set dirs.env.virtual .hatch
```

```bash
hatch config show
```

```bash
hatch env create
```

```bash
hatch status
```

```bash
hatch env show
```

```bash
hatch dep show table
```

```bash
hatch run qa:lint
```

```bash
hatch run qa:format
```

```bash
hatch run docs:dev
```

```bash
hatch project metadata
```

## Deployment

### Package

```bash
hatch version micro
```

```bash
hatch version minor
```

```bash
hatch version major
```

```bash
hatch build --clean
```

```bash
echo "v$(hatch version)" | pbcopy
```

- Commit and push changes.
- Create a tag on [GitHub Desktop](https://github.blog/2020-05-12-create-and-push-tags-in-the-latest-github-desktop-2-5-release/).
- Check [GitLab](https://gitlab.com/joaommpalmeiro/gaveta/-/tags).

```bash
hatch publish
```

- Check [PyPI](https://pypi.org/project/gaveta/).

```bash
BROWSER="firefox" glab auth login --hostname gitlab.com
```

```bash
glab release create "v$(hatch version)"
```

### Documentation

#### Cloudflare Pages

```bash
npx wrangler@3.67.1 login
```

```bash
npx wrangler@3.67.1 whoami
```

```bash
npx wrangler@3.67.1 pages project create gaveta
```

```bash
hatch run docs:build
```

```bash
npx wrangler@3.67.1 pages deploy site --project-name=gaveta
```
