# -*- coding: utf-8 -*-
import markdown
import yaml
import re
import os
import mimetypes
import filecmp
import shutil

CODEHILITE_CSS = '''
pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.codehilite .hll { background-color: #ffffcc }
.codehilite { background: #f8f8f8; }
.codehilite .c { color: #3D7B7B; font-style: italic } /* Comment */
.codehilite .err { border: 1px solid #F00 } /* Error */
.codehilite .k { color: #008000; font-weight: bold } /* Keyword */
.codehilite .o { color: #666 } /* Operator */
.codehilite .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.codehilite .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.codehilite .cp { color: #9C6500 } /* Comment.Preproc */
.codehilite .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.codehilite .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.codehilite .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.codehilite .gd { color: #A00000 } /* Generic.Deleted */
.codehilite .ge { font-style: italic } /* Generic.Emph */
.codehilite .ges { font-weight: bold; font-style: italic } /* Generic.EmphStrong */
.codehilite .gr { color: #E40000 } /* Generic.Error */
.codehilite .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.codehilite .gi { color: #008400 } /* Generic.Inserted */
.codehilite .go { color: #717171 } /* Generic.Output */
.codehilite .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.codehilite .gt { color: #04D } /* Generic.Traceback */
.codehilite .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.codehilite .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.codehilite .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.codehilite .kp { color: #008000 } /* Keyword.Pseudo */
.codehilite .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.codehilite .kt { color: #B00040 } /* Keyword.Type */
.codehilite .m { color: #666 } /* Literal.Number */
.codehilite .s { color: #BA2121 } /* Literal.String */
.codehilite .na { color: #687822 } /* Name.Attribute */
.codehilite .nb { color: #008000 } /* Name.Builtin */
.codehilite .nc { color: #00F; font-weight: bold } /* Name.Class */
.codehilite .no { color: #800 } /* Name.Constant */
.codehilite .nd { color: #A2F } /* Name.Decorator */
.codehilite .ni { color: #717171; font-weight: bold } /* Name.Entity */
.codehilite .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.codehilite .nf { color: #00F } /* Name.Function */
.codehilite .nl { color: #767600 } /* Name.Label */
.codehilite .nn { color: #00F; font-weight: bold } /* Name.Namespace */
.codehilite .nt { color: #008000; font-weight: bold } /* Name.Tag */
.codehilite .nv { color: #19177C } /* Name.Variable */
.codehilite .ow { color: #A2F; font-weight: bold } /* Operator.Word */
.codehilite .w { color: #BBB } /* Text.Whitespace */
.codehilite .mb { color: #666 } /* Literal.Number.Bin */
.codehilite .mf { color: #666 } /* Literal.Number.Float */
.codehilite .mh { color: #666 } /* Literal.Number.Hex */
.codehilite .mi { color: #666 } /* Literal.Number.Integer */
.codehilite .mo { color: #666 } /* Literal.Number.Oct */
.codehilite .sa { color: #BA2121 } /* Literal.String.Affix */
.codehilite .sb { color: #BA2121 } /* Literal.String.Backtick */
.codehilite .sc { color: #BA2121 } /* Literal.String.Char */
.codehilite .dl { color: #BA2121 } /* Literal.String.Delimiter */
.codehilite .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.codehilite .s2 { color: #BA2121 } /* Literal.String.Double */
.codehilite .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.codehilite .sh { color: #BA2121 } /* Literal.String.Heredoc */
.codehilite .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.codehilite .sx { color: #008000 } /* Literal.String.Other */
.codehilite .sr { color: #A45A77 } /* Literal.String.Regex */
.codehilite .s1 { color: #BA2121 } /* Literal.String.Single */
.codehilite .ss { color: #19177C } /* Literal.String.Symbol */
.codehilite .bp { color: #008000 } /* Name.Builtin.Pseudo */
.codehilite .fm { color: #00F } /* Name.Function.Magic */
.codehilite .vc { color: #19177C } /* Name.Variable.Class */
.codehilite .vg { color: #19177C } /* Name.Variable.Global */
.codehilite .vi { color: #19177C } /* Name.Variable.Instance */
.codehilite .vm { color: #19177C } /* Name.Variable.Magic */
.codehilite .il { color: #666 } /* Literal.Number.Integer.Long */
'''

LANGUAGE_HTML_CSS = '''
code{
  color: #000;
  background-color:#F6F6CB;
  font-family: Courier, monosce;
  font-size: 13px;
}
pre{
  border-top:#FFCC66 1px solid;
  border-bottom:#888899 1px solid;
  border-left:#FFCC66 1px solid;
  border-right:#888899 1px solid;
  background-color:#F6F6CB;
  padding: 0.5em 0.8em;
  color: #000;
 *width: 100%;
 _width: 100%;
  overflow: auto;
}
h1 {
  padding: 4px 4px 4px 6px;
  border: 1px solid #999;
  color: #000;
  background-color: #ddd;
  font-weight:900;
  font-size: xx-large;
}
h2 {
  padding: 4px 4px 4px 6px;
  border: 1px solid #999;
  color: #900;
  background-color: #eee;
  font-weight:800;
  font-size: x-large;
}
h3 {
  padding: 4px 4px 4px 6px;
  border: 1px solid #aaa;
  color: #900;
  background-color: #eee;
  font-weight: normal;
  font-size: large;
}
h4 {
  padding: 4px 4px 4px 6px;
  border: 1px solid #bbb;
  color: #900;
  background-color: #fff;
  font-weight: normal;
  font-size: large;
}
h5 {
  padding: 4px 4px 4px 6px;
  color: #900;
  font-size: normal;
}
#navcolumn h5 {
  font-size: smaller;
  border-bottom: 1px solid #aaaaaa;
  padding-top: 2px;
  color: #000;
}
'''


def main():
    pass


def makedoc_filename(src: str, dest: str, check_mode: bool, css_file_list, extensions, replace_list, overview) -> bool:
    if not os.path.isdir(src):
        return makedoc_filename_src_is_file(src, dest, check_mode, css_file_list, extensions, replace_list, overview)
    os.path.basename(src)
    changed = False
    for src_new in os.listdir(src):
        src_new = os.path.join(src, src_new)
        extension = os.path.splitext(src_new)[1]
        extension = extension.lower()
        changed = changed | makedoc_filename_src_is_file(src_new, dest, check_mode, css_file_list, extensions, replace_list, overview)
    return changed


def makedoc_filename_src_is_file(src: str, dest: str, check_mode: bool, css_file_list, extensions, replace_list, overview) -> bool:
    mime_type = mimetypes.guess_type(src)[0]
    src_extension = os.path.splitext(src)[1]
    if 'galaxy.yml' in src:
        dest = os.path.join(os.path.dirname(src), 'README.md')
    else:
        dest_extention = ".html"
        image_flag = False
        if mime_type and (mime_type.startswith('image/') or mime_type.startswith('video/') or mime_type.startswith('application/')):
            image_flag = True
            dest_extention = src_extension
        if (css_file_list is None) and (extensions is None):
            # css や extentions が None なら md に変換しようとしている
            dest_extention = ".md"
        #
        if dest is None:
            # dest が None なら src の名称で拡張子を変える
            dest = src
            if not image_flag:
                dest = dest.replace(os.path.splitext(dest)[1], dest_extention)
        #
        if os.path.isdir(dest):
            # dest がフォルダなら destのフォルダ上で src のファイル名にする
            dest = os.path.join(dest, os.path.basename(src))
            if not image_flag:
                dest = dest.replace(os.path.splitext(dest)[1], dest_extention)
    #
    if src == dest:
        # 移動元と先が同じの場合はエラー
        raise TypeError(f'same name from {src} to {dest}')
    #
    if 'galaxy.yml' in src:
        return makedoc_filename_src_is_galaxy(src, dest, check_mode, css_file_list, extensions, replace_list, overview)
    elif '.md' == src_extension:
        return makedoc_filename_src_is_md(src, dest, check_mode, css_file_list, extensions, replace_list)
    elif '.py' == src_extension:
        return makedoc_filename_src_is_py(src, dest, check_mode, css_file_list, extensions, replace_list, overview)
    elif image_flag:
        return makedoc_filename_src_is_image(src, dest, check_mode)
    else:
        raise TypeError(f'unkown file={src}')
    return False


def makedoc_filename_src_is_image(src: str, dest: str, check_mode):
    if os.path.exists(dest) and filecmp.cmp(src, dest, shallow=False):
        # destが存在して中身が同じなら
        return False
    #
    shutil.copy(src, dest)
    return True


def makedoc_filename_src_is_md(src: str, dest: str, check_mode: bool, css_file_list, extensions, replace_list) -> bool:
    #
    # print(f'\nf={src} t={dest}')
    #
    # 元ネタを読み込む
    src_text = ''
    with open(src, 'r', encoding='utf-8') as f:
        src_text = f.read()
    #
    if ('.md' in dest.lower() or '.md' in dest.lower()):
        # destの拡張子があるなら確認する
        return file_save(dest, src_text, check_mode)
    #
    md = markdown.Markdown(extensions=extensions)
    text = md.convert(src_text)
    title = re.search(r'<h1>([^<]*)<', text)
    if title:
        title = title.group(1)
    else:
        title = None
    text = re.sub(r"<h([\d+])>([^<]*)<", r'<h\1 id="\2">\2<', text)
    text = re.sub(r"<h([\d+])>([^<]*)<", r'<h\1 id="\2">\2<', text)
    while True:
        result = re.search(r'<h[\d+]\s+id="([^"]+)"', text)
        if not result:
            break
        work_from = result.group(1)
        work_to = re.sub(r'\s', '-', work_from.strip())
        work_to = work_to.lower()
        work_to = work_to.replace(';', '').replace(':', '')
        work_to = work_to.replace(',', '').replace('.', '')
        work_to = work_to.replace('[', '').replace(']', '')
        work_to = work_to.replace('(', '').replace(')', '')
        work_from = r'<h([\d+])\s+id="' + re.escape(work_from) + '"'
        work_to = r'<XXX\1 id="' + work_to + '"'
        text = re.sub(work_from, work_to, text)
    text = re.sub(r'<XXX([\d+])', r'<h\1', text)
    for replace in replace_list:
        before = replace['before']
        after = replace['after']
        # print(f'act! {before} / {after}')
        text_new = re.sub(before, after, text)
        if text_new != text:
            # print(f'hit! {before} / {after}')
            text = text_new
    src_text = '<html>\n'
    src_text = src_text + '<head>\n'
    src_text = src_text + '<meta charset="UTF-8">\n'
    src_text = src_text + f'<title>{title}</title>\n'
    for css_file in css_file_list:
        src_text = src_text + f'<link rel="stylesheet" href="{css_file}">\n'
    src_text = src_text + '</head>\n'
    src_text = src_text + '<body>\n'
    src_text = src_text + text
    src_text = src_text + '</body>\n'
    src_text = src_text + '</html>\n'

    flag = False
    flag = create_css(dest, css_file_list, 'codehilite.css', CODEHILITE_CSS, check_mode) | flag
    flag = create_css(dest, css_file_list, 'language_html.css', LANGUAGE_HTML_CSS, check_mode) | flag
    return file_save(dest, src_text, check_mode) | flag


def create_css(dest: str, css_file_list: str, target: str, target_text: str, check_mode: bool) -> bool:
    flag = False
    for css_file in css_file_list:
        if target == css_file:
            flag = True
            break
    if not flag:
        return  # no hit!
    #
    # print(f'flag={flag}/ {css_file_list} /{target}')
    css_file = os.path.join(os.path.dirname(dest), target)
    return file_save(css_file, target_text, check_mode)


def file_save(filename: str, text: str, check_mode: bool):
    # print(f'target={filename}')
    dest_text = ''
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            dest_text = f.read()
    except IOError:
        dest_text = ''
    #
    changed = dest_text != text
    if check_mode:
        # チェックモードなら書き込みを行わない
        return changed
    #
    if changed:
        with open(filename, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
    return changed


def makedoc_filename_src_is_py(ansible_target: str, ansible_readme: str, check_mode: bool, css_file_list, extensions, replace_list, overview) -> bool:
    md_text = ''
    with open(ansible_target, 'r', encoding='utf-8') as f:
        md_text = f.read()
    state = 0
    for text in md_text.splitlines():
        if state == 0:
            if 'DOCUMENTATION' in text:
                md_text = text
                state = 1
        elif state == 1:
            if 'import AnsibleModule' in text:
                break
            md_text = md_text + '\n' + text
    local_scope = {}
    exec(md_text, {}, local_scope)
    # print(f'{json.dumps(local_scope, indent=4)}')
    doc = local_scope['DOCUMENTATION']
    example = local_scope['EXAMPLES']
    ret = local_scope['RETURN']
    title = 'collection'
    #
    doc_dict = yaml.safe_load(doc)
    #
    if 'short_description' in doc_dict:
        title = doc_dict['short_description']
    html = f'# Ansible {title}\n\n'
    if "" != overview:
        html = html + overview.strip() + '\n'

    if 0 < len(doc_dict):
        for k, v in doc_dict.items():
            html = html + f'## {k}\n\n'
            html = html + dict_to_md(0, v)
        html = html + '\n'
    #
    example = example.strip()
    if "" != example:
        html = html + '## Examples\n\n``` yaml\n' + example.strip() + '\n```\n\n'
    #
    html = html + '## Result\n\n'
    result_dict = yaml.safe_load(ret)
    html = html + dict_to_md(0, result_dict)
    #
    extention = os.path.splitext(ansible_readme)[1]
    if '.html' in extention:
        # 拡張子が html なら一旦 md で保存する
        dest_now = ansible_readme.replace(extention, 'md')
        flag = file_save(dest_now, html, check_mode)
        #
        # md を html に変換する
        return makedoc_filename_src_is_md(ansible_target, ansible_readme, check_mode, css_file_list, extensions, replace_list) | flag
    return file_save(ansible_readme, html, check_mode)


def dict_to_md(level, v) -> str:
    html = ''
    # print(f'{v}')
    if isinstance(v, dict):
        for kk, vv in v.items():
            if isinstance(vv, list) and 0 == len(vv):
                html = html + (' ' * (level))
                html = html + f'- **{kk}**: []\n'
            elif isinstance(vv, dict) or isinstance(vv, list):
                html = html + (' ' * (level))
                html = html + f'- **{kk}**:\n'
                html = html + dict_to_md(level + 4, vv)
            else:
                html = html + (' ' * (level))
                html = html + f'- **{kk}**: {str_print(vv)}\n'
    elif isinstance(v, list):
        for vv in v:
            if isinstance(vv, dict) or isinstance(vv, list):
                html = html + dict_to_md(level, vv)
            else:
                html = html + (' ' * (level))
                html = html + f'- {str_print(vv)}\n'
    else:
        html = str_print(v) + '\n'
    return html


def str_print(vv) -> str:
    if vv is None:
        return None
    if isinstance(vv, bool):
        return str(vv)
    if isinstance(vv, int):
        return str(vv)
    if len(vv) == 0:
        return '""'
    if 'https://' in vv:
        return f'<{vv}>'
    return str(vv)


def makedoc_filename_src_is_galaxy(src: str, dest: str, check_mode: bool, css_file_list, extensions, replace_list, overview) -> bool:
    src_text = ''
    with open(src, 'r', encoding='utf-8') as f:
        src_text = f.read()
    doc_dict = yaml.safe_load(src_text)
    html = f"# Ansible Collection - {doc_dict['namespace']}.{doc_dict['name']}\n\n"
    if "" != overview:
        html = html + overview.strip() + '\n\n'
    #
    py_files = os.path.join(os.path.dirname(src), 'plugins')
    py_files = os.path.join(py_files, 'modules')
    file_list = os.listdir(py_files)
    changed = False
    if file_list is not None and 0 < len(file_list):
        html = html + "## Modules\n\n"
        for file in file_list:
            if '.py' not in file and '__init__.py' not in file:
                continue
            name = os.path.splitext(file)[0]
            py_src = os.path.join(py_files, file)  # フォルダ付きファイル名に変換
            py_dest = os.path.join(os.path.dirname(src), 'docs')
            py_dest = os.path.join(py_dest, f'{name}.md')
            html = html + f"- **module**: [{doc_dict['namespace']}.{doc_dict['name']}.{name}](docs/{name}.md)\n"
            overview = ''  # すでに表示したので子供には反映させない
            changed = makedoc_filename_src_is_py(py_src, py_dest, check_mode, css_file_list, extensions, replace_list, overview) | changed
            #
        html = html + "\n"
    #
    html = html + "## Basic Data\n\n"
    html = html + "### galaxy.yml\n\n"
    html = html + dict_to_md(0, doc_dict)
    html = html + "\n"
    requirements = os.path.join(os.path.dirname(src), 'requirements.txt')
    if os.path.isfile(requirements):
        html = html + "### requirements.txt\n\n"
        with open(requirements, 'r', encoding='utf-8') as f:
            for line in f:
                html = html + "- " + line.strip() + "\n"
        html = html + "\n"
    #
    file_list = os.path.join(os.path.dirname(src), 'meta')
    for file in os.listdir(file_list):
        if '.yml' not in file:
            continue
        html = html + f"### {file}\n\n"
        file = os.path.join(file_list, file)  # フォルダ付きファイル名に変換
        with open(file, 'r', encoding='utf-8') as f:
            doc_dict = yaml.safe_load(f.read())
            html = html + dict_to_md(0, doc_dict)
    return file_save(dest, html, check_mode) | changed


if __name__ == '__main__':
    #
    main()
#
