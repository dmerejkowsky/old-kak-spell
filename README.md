# kak-spell

PyEnchant wrapper for Kakoune.

## Installation


1. Install the C Enchant library, and the required dictionaries. See [PyEnchant documentation](https://pyenchant.github.io/pyenchant/install.html) for details.

2. Install the `kak-spell` script, for instance with [pipx](https://pipxproject.github.io/pipx/):

```
pipx install kak-spell
```

3. Install [plug.kak](https://github.com/andreyorst/plug.kak) and add the following lines in your `kakrc`:

```kak
plug "dmerejkowsky/kak-spell"
```


4. (optional): declare a user mode and some mappings:

```kak
plug "dmerejkowsky/kak-spell" config %{
  declare-user-mode kak-spell
  map global user s ': enter-user-mode -lock kak-spell<ret>' -docstring 'enter spell user mode'
  map global kak-spell a ': kak-spell-add<ret>' -docstring 'add the selection to the user dict'
  map global kak-spell d ': kak-spell-disable<ret>' -docstring 'clear spelling highlighters'
  map global kak-spell e ': kak-spell-enable en_US<ret> :kak-spell <ret>' -docstring 'enable spell check in English'
  map global kak-spell f ': kak-spell-enable fr_FR<ret> :kak-spell <ret>' -docstring 'run spell check in French'
  map global kak-spell l ': kak-spell-list <ret>' -docstring 'list spelling errors in a buffer'
  map global kak-spell n ': kak-spell-next<ret>' -docstring 'go to next spell error'
  map global kak-spell p ': kak-spell-previous<ret>' -docstring 'go to next spell error'
  map global kak-spell r ': kak-spell-replace<ret>' -docstring 'suggest a list of replacements'
  map global kak-spell x ': kak-spell-remove<ret>' -docstring 'remove the selection from the user dict'
}
```

Note that `kak-spell-enable` does several things:
* Set a buffer scoped option `kak_spell_lang` that is used by other commands
* Add a highlighter so that spelling errors are colored with the `Error` face
* Adds a `BufWritePost` hook to spell check the buffer each time it gets written

The command `kak-spell-disable` undoes all of the above.

For now, there's no option to disable the hook, or to have it run in response to other events. Please open an issue if this bothers you.

## Discuss

You can discuss features of this plugin on [discuss.kakoune.com](https://discuss.kakoune.com/t/alternate-implementation-for-spell-checker/781).

I'd like to thank all the people who contributed code and ideas to make usage of this plugin easier.
