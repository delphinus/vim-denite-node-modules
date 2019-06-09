# vim-denite-node-modules

Denite source for node packages

<img width="647" alt="スクリーンショット 0001-06-09 14 52 19" src="https://user-images.githubusercontent.com/1239245/59155528-5c682e80-8ac6-11e9-8403-eea73baaab11.png">

## What's this?

This is a source for [denite.nvim][]. This can list up packages as `directory`
kinds and you can do narrow, open, chdir, and so on.

[denite.nvim]: https://github.com/Shougo/denite.nvim

## Dependencies

This plugin depends on the same components as Denite.

* Neovim 0.3.0+, Vim 8.0+ (Python binding enabled)
* Python 3.6.1

## Usage

```vim
:Denite node_modules
```

## See also

* [neoclide/npm.nvim](https://github.com/neoclide/npm.nvim)
  - vim-denite-node-modules owes a lot idea from this. It has more features to
    manage `npm` tasks within (Neo)Vim.
