declare-option str kak_spell_lang

# notes
#   we re-use the existing lint.kak script to display and navigate errors
#   we use `write` to trigger a spell check automatically

define-command kak-spell \
  -params 1 \
  -docstring %{kak-spell [<language>]: enable spell checking for the current buffer %} \
  %{
    evaluate-commands %sh{
      printf "set buffer kak_spell_lang %s" $1
    }
    # need a separate evaluate-commands block because we just set the option :)
    evaluate-commands %sh{
      printf "set buffer lintcmd \"kak-spell --lang $kak_opt_kak_spell_lang check --filetype $kak_opt_filetype \""
    }
    lint-enable
    lint-on-save
    write
  }

define-command kak-spell-clear -docstring "disable spell checking for the current buffer" \
  %{
     unset-option buffer lintcmd
     lint-disable
   }

define-command kak-spell-next -docstring "go to the next spelling error" %{
  lint-next-error
  execute-keys e
}


define-command kak-spell-add -docstring "add the selection to the user dict" %{ \
  evaluate-commands %sh{
    if [ -z "${kak_opt_kak_spell_lang}" ]; then
      printf %s\\n 'echo -markup {Error}The `kak_spell_lang` option is not set'
      exit 1
    fi
  }
  nop %sh{ kak-spell --lang $kak_opt_kak_spell_lang add $kak_selection }
  write
}

define-command kak-spell-remove -docstring "remove the selection from the user dict" %{ \
  evaluate-commands %sh{
    if [ -z "${kak_opt_kak_spell_lang}" ]; then
      printf %s\\n 'echo -markup {Error}The `kak_spell_lang` option is not set'
      exit 1
    fi
  }
  nop %sh{ kak-spell --lang $kak_opt_kak_spell_lang remove $kak_selection }
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
