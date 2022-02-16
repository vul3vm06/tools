#! /usr/bin/env python
import sys
import os
import subprocess
import tempfile

if '__main__' == __name__:
  subprocess.check_call(['git', 'config', 'core.worktree', os.getcwd()])
  file_list = subprocess.check_output(['git', 'diff', '--name-only'] + sys.argv[1:]).split()
  if not file_list:
    print "No diff found."
    sys.exit(0)

  proj_path = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip()

  cmd = ['vim', '-p'] + [os.path.join(proj_path, i) for i in file_list]

  bin_name = os.path.basename(sys.argv[0])

  if bin_name in ['gdf', 'gdfs']:
    script_content = ''
    vim_gdf_cmd = ':Gvdiffsplit\r\n' if bin_name == 'gdf' else ':Gdiffsplit\r\n'
    for i in xrange(len(file_list)):
      script_content += vim_gdf_cmd
      script_content += ':wincmd l\n'
      script_content += ':tabn\n'
    with tempfile.NamedTemporaryFile(suffix = '_' + bin_name) as fp:
      fp.write(script_content)
      fp.flush()

      cmd += ['-s', fp.name]
      try:
        subprocess.check_call(cmd)
      except Exception, e:
        print 'Failed: ' + str(e)
        print ' '.join(cmd)
        print script_content
  elif bin_name == 'vdf':
    try:
      print cmd
      subprocess.check_call(cmd)
    except Exception, e:
      print 'Failed: ' + str(e)
      print ' '.join(cmd)

