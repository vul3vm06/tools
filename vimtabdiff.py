#! /usr/bin/env python

import os
import sys
import subprocess

def tabdiff_with_vim(root1, root2, filelist):
	cmd = ['vim', '-p']
	for file in filelist:
		cmd.append(os.path.join(root1, file))
	for file in filelist:
		cmd.append('-c')
		cmd.append("vertical diffsplit %s" % os.path.join(root2, file))
		cmd.append('-c')
		cmd.append('tabn')
	cmd[-1] = 'tabm 0'
	subprocess.check_call(cmd)

def list_diff_files(parent, dcmp):
	diff_files = [os.path.join(parent, x) for x in dcmp.diff_files]
	diff_files += [os.path.join(parent, x) for x in dcmp.left_only]
	diff_files += [os.path.join(parent, x) for x in dcmp.right_only]
	diff_files += [os.path.join(parent, x) for x in dcmp.funny_files]
	for subdir, sub_dcmp in dcmp.subdirs.iteritems():
		diff_files += list_diff_files(subdir, sub_dcmp)
	return diff_files

if '__main__' == __name__:
	from argparse import ArgumentParser
	from filecmp import dircmp
	parser = ArgumentParser(description='Diff by vim, switching with tabs')
	parser.add_argument('root1', help='right tab', type=str)
	parser.add_argument('root2', help='left tab', type=str)
	opt = parser.parse_args(sys.argv[1:])

	if os.path.isdir(opt.root1) and os.path.isdir(opt.root2):
		dcmp = dircmp(opt.root1, opt.root2)
		filelist = list_diff_files('', dcmp)
	else:
		raise ValueError('Please assign two directories!')

	if filelist:
		tabdiff_with_vim(opt.root1, opt.root2, filelist)
	else:
		print 'No difference'
		sys.exit(0)
