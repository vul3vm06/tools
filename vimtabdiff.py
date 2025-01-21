#! /usr/bin/env python

from __future__ import division           # ensure / does NOT truncate
import os
import pexpect
import psutil
import string
import subprocess
import sys
import tempfile

if sys.version_info[0] == 2:
  def trans(s):
    return s.translate(string.maketrans("", ""), string.printable)
elif sys.version_info[0] == 3:
  def trans(s):
    return s.translate(str.maketrans("", "", string.printable))
else:
  def trans(s):
    return s

# Adapt from Python Cookbook Andrew Dalke
def istext(s, threshold=0.30):
  # if s contains any null, it's not text:
  if "\0" in s:
      return False
  # an "empty" string is "text" (arbitrary but reasonable choice):
  if not s:
      return True
  # Get the substring of s made up of non-text characters
  t = trans(s)
  # s is 'text' if less than 30% of its characters are non-text ones:
  return len(t)/len(s) <= threshold

def tabdiff_with_vim(root1, root2, filelist):
  cmd = ['vim', '-p']
  non_text_filelist = []
  for file_path in filelist:
    file_path_in_root1 = os.path.join(root1, file_path)
    if os.path.exists(file_path_in_root1):
      if os.path.isfile(file_path_in_root1):
        with open(file_path_in_root1) as fp:
          if not istext(fp.read(1024)):
            print('skip non-text file ' + os.path.join(root1, file_path))
            non_text_filelist.append(file_path)
          else:
            cmd.append(file_path_in_root1)
      elif os.path.isdir(file_path_in_root1):
        cmd.append(file_path_in_root1)
      else:
        print('skip file ' + os.path.join(root1, file_path))
    else:
      cmd.append(os.devnull)

  script_content = ''
  for file_path in filelist:
    if file_path in non_text_filelist:
      print('skip non-text file ' + os.path.join(root2, file_path))
      continue
    file_path_in_root2 = os.path.join(root2, file_path)
    if os.path.exists(file_path_in_root2):
      script_content += ":vertical diffsplit %s\n" % file_path_in_root2
    else:
      script_content += ":vertical diffsplit %s\n" % os.devnull
    script_content += ':wincmd l\n'
    script_content += ':tabn\n'

  with tempfile.NamedTemporaryFile(suffix = '_' + os.path.basename(__file__), mode = 'w') as fp:
    fp.write(script_content)
    fp.flush()

    cmd += ['-s', fp.name]
    try:
      subprocess.check_call(cmd)
      #print(' '.join(cmd))
      #print(script_content)
    except Exception as e:
      print('Failed: ' + str(e))
      print(' '.join(cmd))
      print(script_content)

def list_diff_files(root1, root2):
  dcmp = dircmp(root1, root2)
  diff_files = dcmp.diff_files

  if dcmp.same_files:
    print("Warning: dcmp.same_files: " + str(dcmp.same_files))
  if dcmp.left_only:
    print(' Left Only:\n\t' + '\n\t'.join(dcmp.left_only))
    diff_files += dcmp.left_only
  if dcmp.right_only:
    print(' Right Only:\n\t' + '\n\t'.join(dcmp.right_only))
    diff_files += dcmp.right_only
  if dcmp.funny_files:
    print(' Files cannot be compared:\n\t' + '\n\t'.join(dcmp.funny_files))
  for subdir, sub_dcmp in dcmp.subdirs.items():
    diff_files += [os.path.join(subdir, x) for x in list_diff_files(os.path.join(root1, subdir), os.path.join(root2, subdir))]

  return diff_files

def diff_two_roots(root1, root2):
  if os.path.isfile(root1) and os.path.isfile(root2):
    subprocess.check_call(['vimdiff', root1, root2])
    sys.exit(0)

  if os.path.isdir(root1) and os.path.isdir(root2):
    filelist = list_diff_files(root1, root2)
  else:
    raise ValueError('Please assign two directories or two files!')

  if filelist:
    if len(filelist) > 50:
      print('Too many diff files to display. Total [%d] files' % len(filelist))
      sys.exit(-1)
    tabdiff_with_vim(root1, root2, filelist)
  else:
    print('No difference')
    sys.exit(0)

if '__main__' == __name__:
  from argparse import ArgumentParser
  from filecmp import dircmp

  bin_name = os.path.basename(sys.argv[0])

  if bin_name.startswith('vimtabdiff') or bin_name.startswith('tdf'):
    parser = ArgumentParser(description='Diff by vim, switching with tabs')
    parser.add_argument('root1', help='right tab', type=str)
    parser.add_argument('root2', help='left tab', type=str)
    opt = parser.parse_args(sys.argv[1:])
    diff_two_roots(opt.root2, opt.root1)
  else:
    child = pexpect.spawn('git difftool --dir-diff --no-prompt ' + ' '.join(sys.argv[1:]))
    print('spawn git difftool pid ' + str(child.pid))
    child.expect('\"')
    if not child.isalive():
      print('Error. child is not alive. pid ' + child.pid)
    children = psutil.Process(child.pid).children(recursive=True)
    # possible example of children:
    # /usr/lib/git-core/git difftool--helper /tmp/git-difftool.DxqQaw/left/ /tmp/git-difftool.DxqQaw/right/
    # /bin/sh /usr/lib/git-core/git-difftool--helper /tmp/git-difftool.DxqQaw/left/ /tmp/git-difftool.DxqQaw/right/
    # vim -R -f -d -c wincmd l -c cd $GIT_PREFIX /tmp/git-difftool.DxqQaw/left/ /tmp/git-difftool.DxqQaw/right/
    # /bin/bash -c diff -a /tmp/vzECZxX/0 /tmp/vzECZxX/1 >/tmp/vzECZxX/2 2>&1
    for c in children:
      if c.name() == 'vim':
        root1 = c.cmdline()[-1]
        root2 = c.cmdline()[-2]
        break
      else:
        continue
    else:
      print('Error. unexpected children:\n' +
            '\n'.join([' '.join(c.cmdline()) for c in children]))
      sys.exit(-1)

    diff_two_roots(root1, root2)
    child.kill(0)
