# kak-spell

PyEnchant wrapper for Kakoune.

## Installation


1. Install the Enchant library, and the required dictionaries. See [PyEnchant documentation](https://pyenchant.github.io/pyenchant/install.html) for details.

2. Install the `kak-spell` script, for instance with [pipx](https://pipxproject.github.io/pipx/):

```
pipx install kak-spell
```

3. Install [plug.kak](https://github.com/andreyorst/plug.kak) and add the following lines in your `kakrc`:

```kak
plug "dmerejkowsky/kak-spell"

define-command lint-on-save "hook buffer BufWritePre .* lint"```
```


4. (optional): declare a user mode and some mappings:

```kak
declare-user-mode kak-spell
map global user s ': enter-user-mode kak-spell<ret>' -docstring 'enter spell user mode'
map global kak-spell e ': kak-spell %opt{spell_lang}<ret>' -docstring "enable spell checking"
map global kak-spell c ': kak-spell-clear<ret>' -docstring 'clear spelling highlighters'
map global kak-spell n ': kak-spell-next<ret>' -docstring 'go to next spell error'
map global kak-spell r ': kak-spell-replace<ret>' -docstring 'suggest a list of replacements'
map global kak-spell a ': kak-spell-add<ret>' -docstring 'add the selection to the user dict'
map global kak-spell x ': kak-spell-remove<ret>' -docstring 'remove the selection from the user dict'
```



## Discuss

You can discuss features of this plugin on [discuss.kakoune.com](https://discuss.kakoune.com/t/alternate-implementation-for-spell-checker/781).

I'd like to thank all the people who contributed code and ideas to make usage of this plugin easier.
