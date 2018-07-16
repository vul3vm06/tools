#! /usr/bin/env python

# From https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s12.html
from __future__ import division           # ensure / does NOT truncate
import os
import sys
import subprocess
import tempfile

import string
text_characters = "".join(map(chr, range(32, 127))) + "\n\r\t\b"
_null_trans = string.maketrans("", "")
def istext(s, text_characters=text_characters, threshold=0.30):
  # if s contains any null, it's not text:
  if "\0" in s:
      return False
  # an "empty" string is "text" (arbitrary but reasonable choice):
  if not s:
      return True
  # Get the substring of s made up of non-text characters
  t = s.translate(_null_trans, text_characters)
  # s is 'text' if less than 30% of its characters are non-text ones:
  return len(t)/len(s) <= threshold

def tabdiff_with_vim(root1, root2, filelist):
  cmd = ['vim', '-p']
  non_text_filelist = []
  for file_path in filelist:
    if file_path.endswith('.pyc') or file_path.endswith('.swp'):
      continue
    with open(os.path.join(root1, file_path)) as fp:
      if not istext(fp.read(1024)):
        print 'skip non-text file ' + os.path.join(root1, file_path)
        non_text_filelist.append(file_path)
        continue
    cmd.append(os.path.join(root1, file_path))

  script_content = ''
  for file_path in filelist:
    if file_path.endswith('.pyc') or file_path.endswith('.swp'):
      continue
    if file_path in non_text_filelist:
      print 'skip non-text file ' + os.path.join(root2, file_path)
      continue
    script_content += ":vertical diffsplit %s\n" % os.path.join(root2, file_path)
    script_content += ':tabn\n'

  with tempfile.NamedTemporaryFile(suffix = '_' + os.path.basename(__file__)) as fp:
    fp.write(script_content)
    fp.flush()

    cmd += ['-s', fp.name]
    try:
      subprocess.check_call(cmd)
      print ' '.join(cmd)
      print script_content
    except Exception, e:
      print 'Failed: ' + str(e)
      print ' '.join(cmd)
      print script_content

def list_diff_files(parent, dcmp):
  diff_files = [os.path.join(parent, x) for x in dcmp.diff_files]
  #diff_files += [os.path.join(parent, x) for x in dcmp.left_only]
  #diff_files += [os.path.join(parent, x) for x in dcmp.right_only]
  #diff_files += [os.path.join(parent, x) for x in dcmp.funny_files]
  if dcmp.left_only:
    print 'Files Left Only:\n\t' + '\n\t'.join(dcmp.left_only)
    pass
  if dcmp.right_only:
    print 'Files Right Only:\n\t' + '\n\t'.join(dcmp.right_only)
    pass
  if dcmp.funny_files:
    print 'Files cannot be compared:\n\t' + '\n\t'.join(dcmp.funny_files)
    pass
  for subdir, sub_dcmp in dcmp.subdirs.iteritems():
    diff_files += list_diff_files(os.path.join(parent, subdir), sub_dcmp)
  return diff_files

if '__main__' == __name__:
  from argparse import ArgumentParser
  from filecmp import dircmp
  parser = ArgumentParser(description='Diff by vim, switching with tabs')
  parser.add_argument('root1', help='right tab', type=str)
  parser.add_argument('root2', help='left tab', type=str)
  opt = parser.parse_args(sys.argv[1:])

  if os.path.isdir(opt.root1) and os.path.isdir(opt.root2):
    dcmp = dircmp(os.path.realpath(opt.root1), os.path.realpath(opt.root2))
    filelist = list_diff_files('', dcmp)
  elif os.path.isfile(opt.root1) and os.path.isfile(opt.root2):
    subprocess.check_call(['vimdiff', opt.root1, opt.root2])
    sys.exit(0)
  else:
    raise ValueError('Please assign two directories or two files!')

  if filelist:
    if len(filelist) > 50:
      print 'Too many diff files to display. Total [%d] files' % len(filelist)
      sys.exit(-1)
    tabdiff_with_vim(opt.root1, opt.root2, filelist)
  else:
    print 'No difference'
    sys.exit(0)
