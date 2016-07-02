import os, os.path
import commands
import dateparser
import humanize

EMAIL_INDEX = 1
DATE_INDEX = 2

def context(page, config):
    input_path = os.path.join(config['docs_dir'], page.input_path)
    input_directory = os.path.dirname(input_path)
    # Path into the directory of the file so that submodule git logs are
    # utilised inplace of the top level repo log.
    git_command = 'cd "%s";git log --pretty=format:%%aN,%%ae,%%cd "%s"' \
    % (input_directory, input_path)
    commits_meta_str = list(commands.getoutput(git_command).split('\n'))
    commits_meta = map(lambda x: x.split(','), commits_meta_str)
    contributors_by_email = {}
    for meta in commits_meta:
        contributors_by_email[meta[EMAIL_INDEX]] = meta[:2]
    contributors = contributors_by_email.values()
    commit_dates = map(lambda x: dateparser.parse(x[DATE_INDEX]), commits_meta)
    last_commit_date = reduce(lambda x, y: x if x>y else y, commit_dates)
    return {'contributors': contributors,
            'last_modified': last_commit_date,
            'last_modified_relative' : humanize.naturaltime(last_commit_date)}
