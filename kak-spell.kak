declare-option str kak_spell_lang
declare-option range-specs spell_errors

define-command -params 1 kak-spell-enable %{
  evaluate-commands %sh{
    echo "set buffer kak_spell_lang $1"
  }
  add-highlighter buffer/spell ranges spell_errors
  hook -group kak-spell buffer BufWritePost .* kak-spell
}

define-command kak-spell-disable %{
  remove-highlighter buffer/spell
  remove-hooks buffer kak-spell
}

define-command kak-spell -docstring "check the current buffer for spelling errors" %{
  evaluate-commands %sh{
    kak-spell \
      --lang "${kak_opt_kak_spell_lang}" \
      check \
      --filetype "${kak_opt_filetype}" \
      "${kak_buffile}" \
      --kak-timestamp ${kak_timestamp} \
      --kakoune
  }
}

define-command kak-spell-next -docstring "go to the next spelling error" %{
   evaluate-commands %sh{
     kak-spell next \
      --ranges "${kak_opt_spell_errors}" \
      --pos "${kak_cursor_line}.${kak_cursor_column}"
   }
}

define-command kak-spell-previous -docstring "go to the previous spelling error" %{
   evaluate-commands %sh{
     kak-spell previous \
      --ranges "${kak_opt_spell_errors}" \
      --pos "${kak_cursor_line}.${kak_cursor_column}"
   }
}

define-command kak-spell-add -params 0..1 -docstring "add the selection to the user dict" %{
  evaluate-commands %sh{
    if [ -z "${kak_opt_kak_spell_lang}" ]; then
      printf %s\\n 'echo -markup {Error}The `kak_spell_lang` option is not set'
      exit 1
    fi
  }
  nop %sh{
    if [ -z "$1" ]; then
      kak-spell --lang $kak_opt_kak_spell_lang add $kak_selection
    else
      kak-spell --lang $kak_opt_kak_spell_lang add $1
    fi
  }
  write
}

define-command kak-spell-remove -params 0..1 -docstring "remove the selection from the user dict" %{
  evaluate-commands %sh{
    if [ -z "${kak_opt_kak_spell_lang}" ]; then
      printf %s\\n 'echo -markup {Error}The `kak_spell_lang` option is not set'
      exit 1
    fi
  }
  nop %sh{
    if [ -z "$1" ]; then
      kak-spell --lang $kak_opt_kak_spell_lang remove $kak_selection
    else
      kak-spell --lang $kak_opt_kak_spell_lang remove $1
    fi
  }
  write
}

define-command kak-spell-replace -docstring "replace the selection with a suggestion " %{
  evaluate-commands %sh{
    if [ -z "${kak_opt_kak_spell_lang}" ]; then
      printf %s\\n 'echo -markup {Error}The `kak_spell_lang` option is not set'
      exit 1
    fi
  }

  evaluate-commands %sh{ kak-spell --lang $kak_opt_kak_spell_lang replace $kak_selection --kakoune }
}
