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
set virtualedit=all
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

function VerticalScrollAndKeepWinView(down)
  let view = winsaveview()
  let winheight = winheight('%')

  if a:down == 1
    let view.lnum = view.lnum + winheight
  else
    let view.lnum = view.lnum - winheight
  endif

  if a:down == 1
    let view.topline = view.topline + winheight
  else
    let view.topline = view.topline - winheight
  endif

  call winrestview(view)
endfunction

nmap <silent> <C-f> :call VerticalScrollAndKeepWinView(1)<Enter>
nmap <silent> <C-b> :call VerticalScrollAndKeepWinView(0)<Enter>

nnoremap n nzz
nnoremap N Nzz
nnoremap * *zz
nnoremap # #zz
nnoremap g* g*zz
nnoremap g# g#zz

nnoremap gs :call IwhiteToggle()<Enter>
  function! IwhiteToggle()
    if &diff
      if has("patch-8.1.0393")
        if &diffopt =~ 'iwhiteall'
          set diffopt-=iwhiteall
        else
          set diffopt+=iwhiteall
        endif
      else
        if &diffopt =~ 'iwhite'
          set diffopt-=iwhite
        else
          set diffopt+=iwhite
        endif
      endif
    endif
endfunction

" windows reserved paste on control-v
nnoremap <C-q> <C-v>

nnoremap ver :windo wincmd H<Enter>
nnoremap hor :windo wincmd K<Enter>

"" Windows reserves control-v for 'paste' action, use control-q instead.
"nnoremap <C-q> <C-v>

colorscheme apprentice

"" This varies from environments.
"set termguicolors

highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$/
autocmd BufWinEnter * match ExtraWhitespace /\s\+$/
autocmd InsertEnter * match ExtraWhitespace /\s\+\%#\@<!$/
autocmd InsertLeave * match ExtraWhitespace /\s\+$/
autocmd BufWinLeave * call clearmatches()

highlight ColorColumn ctermbg=black
set colorcolumn=80

if !empty(globpath(&rtp, 'pack/preservim/start/tagbar'))
  set laststatus=2
  set statusline=%<%f\ %h%m%r%=%{tagbar#currenttag('%s\ ','','f')}%-.(%l,%c%V%)\ %P
endif
