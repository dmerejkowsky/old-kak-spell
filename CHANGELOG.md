# 0.2.1 (2020-04-13)

* Add `kak-spell-list`. Fix #5

# 0.2.0 (2020-04-12)

* Allow adding or removing words without selecting them first
* Better mypy config
* Fix deprecation warnings with latest `path.py` version
* Rewrite plugin so we don't depend on `lint.kak` at all 
* Replace `lint-on-save` with a proper hook

## Breaking changes
* `kak-spell` no longer creates the `<lang>` option and no longer takes
  a language as first argument, instead you should run `kak-spell-enable <lang>` before calling `kak-spell`
* Rename `kak-spell-clear` to `kak-spell-disable`


# 0.1.2 (2020-03-16)

* Bump PyEnchant to the latest release

# 0.1.1 (2020-28-03)

* Relax Python version
* Add missing lint-on-save command

# 0.1.0 (2020-28-02)

Initial release

