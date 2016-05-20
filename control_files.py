# -*- coding: utf-8 -*-
"""
   Search a directory tree for CUPS control files

"""
from __future__ import division, print_function
import os
import sys
import re
from collections import OrderedDict, defaultdict
from pprint import pprint


def read_file(path):
    with open(path, 'rb') as f:
        return f.read()


def split_all(path):
    parts = []
    d = path
    for _ in range(20):
        d, name = os.path.split(d)
        # print('@@@', d, name)
        if not name:
            break
        parts.append(name)
        if not d:
            break
    parts.reverse()

    # print('##')
    # print(path)
    # print(parts)
    # assert False
    return parts


RE_ISSSUE = re.compile(r'^(?:\d{6}$|\w{3}-\d{3}-\d{5})')


def get_issue(parts):
    for p in parts:
        if RE_ISSSUE.match(p):
            return p
    return None


def recursive_glob(dir_name, mask):
    """Like glob.glob() except that it sorts directories and
        recurses through subdirectories.
    """
    # assert False
    print('_recursive_glob', dir_name, mask)
    RE_MASK = re.compile(mask)
    recursive_list = os.walk(dir_name)
    print('recursive_list=%s' % recursive_list)
    sys.stdout.flush()
    # assert False
    # out = []
    for i, (root, dirs, files) in enumerate(recursive_list):
        print('root=%d:%d:%s' % (i, len(files), root))
        path_list = [path for path in files if RE_MASK.search(path)]
        # print('!%d,' % len(path_list), end='')
        path_list.sort(key=lambda s: (s.lower(), s))
        # print('#%d,' % len(path_list), end='')
        # path_list = sorted(fnmatch.filter(files, mask), key=lambda s: (s.lower(), s))
        for filename in path_list:
            # pass
            full_path = os.path.join(root, filename)
            parts = split_all(root)
            issue = get_issue(parts)
            if issue is None and parts:
                issue = parts[-1]
            if issue is None:
                print('*** no issue: %s' % path)
                continue
            print('!!!', full_path)
            print('   ', parts, filename)
            print('   ', issue)
            yield(full_path, issue, filename)
            # out.append((full_path, issue, filename))
        # print('$%d' % len(path_list))
    # return out



def glob(dir_name, mask):
    """Like glob.glob() except that it sorts directories and
        optionally recurses through subdirectories and
        optionally returns full paths.

        Params:
            path_pattern: path to match
            recursive: recurse through directories?
            abs_path: use abspath to create returned names?
            include_dirs: return directories as well as plain files?
            do_reverse: return paths in reverse order/
        Returns:
            Generator returning paths
    """
    print('glob', dir_name, mask)
    text_path = {}
    path_text = {}
    isfn_paths = defaultdict(list)
    isfn_list = []

    for path, issue, filename in recursive_glob(dir_name, mask):
        text = read_file(path)
        if text in text_path:
            continue
        text_path[text] = path
        path_text[path] = text
        isfn = tuple((issue, filename))
        # assert isfn not in isfn_dict, '\n'.join((str(isfn), path, isfn_dict[isfn]))

        isfn_paths[isfn].append(path)
        isfn_list.append(isfn)

    path_dict = OrderedDict()
    for isfn in isfn_list:
        issue, filename = isfn
        for i, path in enumerate(isfn_paths[isfn]):
            text = path_text[path]
            path_dict[path] = tuple((issue, i, filename, text))

    print('5555')
    return path_dict


def mkdir(path):
    try:
        os.mkdir(path)
    except Exception as e:
        print('mkdir', path, e)

CONTROL = 'control.files'


def find_control_files(root):
    import shutil
    mask = r'^c\d{3,10}$'
    print('mask=%s' % mask)
    path_dict = glob(root, mask)
    print('@' * 80)
    lengths = [len(text) for _, _ , _ , text in path_dict.values()]
    print('%d files,min=%d,max=%d' % (len(path_dict), min(lengths), max(lengths)))
    # for i, (path, (issue, j, filename, text)) in enumerate(path_dict.items()):
    #     print('%4d: %5d %s %s' % (i, len(text), [issue, j, filename], path))

    mkdir(CONTROL)
    for i, (path, (issue, j, filename, text)) in enumerate(path_dict.items()):
        dest_dir = os.path.join(CONTROL, issue)
        dest_name = '%s_%02d' % (filename, j)
        dest_path = os.path.join(dest_dir, dest_name)
        mkdir(dest_dir)
        print('%4d: %5d %s %s' % (i, len(text), [issue, j, filename], path))
        try:
            shutil.copy(path, dest_path)
        except Exception as e:
            print('==> copy %s failed %s' % (path, e))


if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Usage: python %s <root>' % sys.argv[0]
    find_control_files(sys.argv[1])
