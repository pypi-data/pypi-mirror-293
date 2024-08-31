# 31075

git@github.com:Enkidu-Aururu/31075.git# minimal-reproduction-template

Based on [Renovate minimal reproduction instructions](https://github.com/renovatebot/renovate/blob/main/docs/development/minimal-reproductions.md).

## Problem

TODO:

```bash
python3.12 -m venv venv
. venv/bin/activate
grep -v "renovate-" requirements.txt | xargs -i pip install {}
python3.12 -m build
twine upload dist/*
```

## Expectation

TODO

## References

[Renovate discussion #31075](https://github.com/renovatebot/renovate/discussions/31075 "Could PYPI datasource accept also look into url field?")
