declare-option str kak_spell_lang
declare-option range-specs spell_errors

define-command kak-spell \
  -params 0..1 \
  -docstring %{kak-spell [<language>]: enable spell checking for the current buffer %} \
  %{
     # add the highlighter (only once)
     try %{
       add-highlighter buffer/spell ranges spell_errors
     %}

    hook -once -group kak-spell buffer BufWritePost .* kak-spell

    evaluate-commands %sh{
      if [ -n "$1" ]; then
         echo "set buffer kak_spell_lang $1"
      fi
      kak-spell \
        --lang "en_US" \
        check \
        --filetype "${kak_opt_filetype}" \
        "${kak_buffile}" \
        --kak-timestamp ${kak_timestamp} \
        --kakoune
     }

  }

define-command kak-spell-clear -docstring "disable spell checking for the current buffer" \
  %{
    remove-highlighter buffer/spell
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


define-command kak-spell-add -params 0..1 -docstring "add the selection to the user dict" %{ \
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

define-command kak-spell-remove -params 0..1 -docstring "remove the selection from the user dict" %{ \
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

define-command kak-spell-replace -docstring "replace the selection with a suggestion " %{ \
  evaluate-commands %sh{
    if [ -z "${kak_opt_kak_spell_lang}" ]; then
      printf %s\\n 'echo -markup {Error}The `kak_spell_lang` option is not set'
      exit 1
    fi
  }

  evaluate-commands %sh{ kak-spell --lang $kak_opt_kak_spell_lang replace $kak_selection --kakoune }
}
