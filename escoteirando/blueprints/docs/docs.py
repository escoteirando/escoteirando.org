import os

from cache_gs import CacheGS

from escoteirando.ext.configs import Configs

cache = CacheGS(Configs.Instance().CACHE_STRING_CONNECTION)


def get_privacidade():
    return md_to_html('privacidade.md')


def get_termos():
    return md_to_html('termos.md')


def md_to_html(file):
    global cache
    html = cache.get_value('docs', file)
    if not html:
        html = {"html": process_md(file)}
        if html:
            cache.set_value('docs', file, html, 60*60*24*7)

    return html['html']


def process_md(file):
    file = os.path.abspath(os.path.join(
        os.path.curdir, 'escoteirando', 'static', 'docs', file))
    if os.path.isfile(file):
        lines = []
        with open(file) as f:
            list_type = None
            list_started = False
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                tag = None
                if line.startswith('####'):
                    tag = 'h4'
                    line = line[4:].strip()
                elif line.startswith('###'):
                    tag = 'h3'
                    line = line[3:].strip()
                elif line.startswith('##'):
                    tag = 'h2'
                    line = line[2:].strip()
                elif line.startswith('#'):
                    tag = 'h1'
                    line = line[1:].strip()
                elif line.startswith('*'):
                    tag = 'li'
                    line = line[1:].strip()
                    list_type = 'ul'
                elif '0' <= line[0] <= '9':
                    tag = 'li'
                    line = line[1:].strip()
                    list_type = 'ol'
                else:
                    tag = 'p'

                if list_type and not list_started:
                    lines.append('<'+list_type+'>')
                    list_started = True

                if list_started and tag != 'li':
                    lines.append('</'+list_type+'>')
                    list_started = False
                    list_type = None

                lines.append(f'<{tag}>{line}</{tag}>')

            if list_started and tag != 'li':
                lines.append('</'+list_type+'>')
                list_started = False
                list_type = None

        return '\n'.join(lines)
    return ""
