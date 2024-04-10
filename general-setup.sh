set -o xtrace

TOOLS_LOCAL_PATH="$HOME/workspace/github-vul3vm06-tools"
MYBASHRC="$HOME/.bashrc"
MYVIMRC="$HOME/.vimrc"
MYVIMFOLDER="$HOME/.vim"

CREATE_BACKUPS=(
  $TOOLS_LOCAL_PATH
  $MYBASHRC
  $MYVIMRC
  $MYVIMFOLDER
)

for p in "${CREATE_BACKUPS[@]}"; do
  if test -f $p; then
    mv $p $p.backup
  fi
done

mkdir -p $TOOLS_LOCAL_PATH &&
git clone https://github.com/vul3vm06/tools.git $TOOLS_LOCAL_PATH &&

# vim setup
cp $TOOLS_LOCAL_PATH/vimrc $MYVIMRC &&

mkdir -p $HOME/.vim/colors &&
wget https://raw.githubusercontent.com/romainl/Apprentice/master/colors/apprentice.vim -O $HOME/.vim/colors/apprentice.vim &&

mkdir -p $HOME/.vim/pack/rhysd/start/ &&
git clone https://github.com/rhysd/vim-clang-format $HOME/.vim/pack/rhysd/start/vim-clang-format &&

mkdir -p $HOME/.vim/pack/tpope/start/ &&
git clone https://tpope.io/vim/fugitive.git $HOME/.vim/pack/tpope/start/fugitive &&

mkdir -p $HOME/.vim/pack/preservim/start/ &&
git clone https://github.com/preservim/tagbar.git $HOME/.vim/pack/preservim/start/tagbar &&

# pip and pexpect and psutil for vimtabdiff.py
wget https://bootstrap.pypa.io/get-pip.py &&
python get-pip.py &&
pip install pexpect psutil &&

# git config setup
bash $TOOLS_LOCAL_PATH/git-config-setup.sh &&

# bashrc setup
cat $TOOLS_LOCAL_PATH/bashrc-to-append >> $MYBASHRC &&

set +o xtrace

echo "$0 done."
echo "To make bashrc change take effect immediately too:"
echo "source $TOOLS_LOCAL_PATH/bashrc-to-append"

