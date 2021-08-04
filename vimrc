set encoding=utf-8

set foldmethod=syntax
set expandtab
set softtabstop=0
set shiftwidth=2
set tabstop=2
set tags=tags;/

syntax on
set number
set ruler
set nowrap
set cursorline
set hlsearch
xnoremap p pgvy

set tabpagemax=70

au BufReadPost,BufNewFile,BufRead *.jsm set syntax=javascript
au BufReadPost,BufNewFile,BufRead *.ipdl set syntax=cpp
au BufReadPost,BufNewFile,BufRead *.webapp set syntax=json
au BufReadPost,BufNewFile,BufRead *.webidl set syntax=cpp
au BufReadPost,BufNewFile,BufRead *.idl set syntax=cpp
au BufReadPost,BufNewFile,BufRead *.py set foldmethod=indent
au BufReadPost,BufNewFile,BufRead *.jsm set foldmethod=indent

" resize horzontal split window
nmap <S-Left> <C-W><
nmap <S-Right> <C-W>>

" scroll horizontally
nmap <S-l> zl
nmap <S-h> zh

nnoremap n nzz
nnoremap N Nzz
nnoremap * *zz
nnoremap # #zz
nnoremap g* g*zz
nnoremap g# g#zz

colorscheme apprentice

highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$/
autocmd BufWinEnter * match ExtraWhitespace /\s\+$/
autocmd InsertEnter * match ExtraWhitespace /\s\+\%#\@<!$/
autocmd InsertLeave * match ExtraWhitespace /\s\+$/
autocmd BufWinLeave * call clearmatches()

highlight ColorColumn ctermbg=black
set colorcolumn=80
