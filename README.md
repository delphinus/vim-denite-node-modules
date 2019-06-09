# vim-denite-npm-packages

Denite source for node packages

<img width="649" alt="スクリーンショット 2019-06-08 18 35 32" src="https://user-images.githubusercontent.com/1239245/59145275-56b60e80-8a1c-11e9-8718-64fe141c2002.png">

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
:Denite packages
```

## See also

* [neoclide/npm.nvim](https://github.com/neoclide/npm.nvim)
  - vim-denite-npm-packages owes a lot idea from this. It has more features to
    manage `npm` tasks within (Neo)Vim.
