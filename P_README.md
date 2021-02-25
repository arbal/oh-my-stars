## FORKED CHANGES

This simplifies the summary to one line each, and doesn't print a count/summary, and just prints the matches one after another; that makes it easier to process with common shell tools like `grep` or `fzf`.

Example:

```shell
 $ mystars mint
kevinschaich/mintable [https://github.com/kevinschaich/mintable] TypeScript 🍃 Automate your personal finances – for free, with no ads, and no data collection.
# just print all results
$ mystars --list
...
$ mystars --list | wc -l
139
```

I commonly use the following script, to search for a repo I've starred and copy the link to my clipboard.

```
>>>PMARK
perl -E 'print "`"x3, "bash", "\n"'
curl -s https://sean.fish/d/mystarsfzf
perl -E 'print "`"x3, "\n"'
```
- Uses [`urlextract`](https://pypi.org/project/urlextract/), and some of my personal clipboard/browser scripts, see [here](https://sean.fish/d/?dark) for an index/reference.


I've also removed the limit for the number of entries the `-3` flag returns (`JSON`), so this can be used with [`jq`](https://stedolan.github.io/jq/) to parse/search the results:

```bash
mystars --list -c=never -3 | jq -r '.items | .[16]'
{
  "title": "tmcw/big",
  "subtitle": "presentations for busy messy hackers [JavaScript]",
  "arg": "https://github.com/tmcw/big"
}
mystars --list -c=never -3 | jq -r '.items | .[] | .arg' | shuf -n5
https://github.com/bootandy/dust
https://github.com/karlicoss/HPI
https://github.com/jameslittle230/stork
https://github.com/ripienaar/free-for-dev
https://github.com/paulgalow/albumart-dl
```

To Install:

`pip install git+https://github.com/seanbreckenridge/oh-my-stars`

---

# oh-my-stars

Search your stars locally.

```
usage: mystars [-h] [-l LANGUAGE [LANGUAGE ...]] [-u] [-r] [-a] [-3] [-i]
                   [-v]
                   [keywords [keywords ...]]

a CLI tool to search your starred Github repositories.

positional arguments:
  keywords              Search by keywords

optional arguments:
  -h, --help            show this help message and exit
  -l LANGUAGE [LANGUAGE ...], --language LANGUAGE [LANGUAGE ...]
                        Filter by language
  -u, --update          Create(first time) or update the local stars index
  -r, --reindex         Re-create the local stars index
  -c WHEN, --color WHEN
                        Colorize the output; WHEN can be 'always' (default if
                        omitted), 'auto', or 'never'
  -a, --alfred          Format search result as Alfred Script Filter output
  -3, --three           Alfred 3 support
  -i, --install         Import Alfred workflow
  -v, --version         show program's version number and exit

```

![oh-my-stars](https://raw.github.com/wolfg1969/my-stars-pilot/master/oh-my-stars.png)
##### Works with Alfred Workflow

![oh-my-stars-alfred-workflow](https://raw.github.com/wolfg1969/my-stars-pilot/master/oh-my-stars-alfred-workflow.png)

### Configuration
You can avoid entering your GitHub API credentials every time you update the index, by adding them to the ``~/.netrc`` file as follows:

```ini
machine api.github.com
    login ‹GH_USERNAME›
    password ‹GH_API_TOKEN›
```
Use an API token as the password – you can create one via *Settings » Developer settings » Personal access tokens* in the GitHub web interface.

Once you have stored credentials, you can also automate the index update by adding a job with ``crontab -e``:

```sh
# GitHub stars
0 6 * * *	~/.local/bin/mystars -u
```

### Installation (Mac OSX)
```sh
$ pip install oh-my-stars --upgrade --user
$ mystars --help
$ mystars --update
$ mystars angular upload
$ mystars --language python
$ mystars awesome python
``` 

if install failed, try following commands
```sh
$ pip uninstall distribute
$ pip install setuptools
$ pip install --upgrade setuptools
```

### Integration with Alfred
```sh
$ mystars -i -3
```
For Alfred v2
```sh
$ mystars -i
```

### Change logs

#### v1.5.1
- Fix error 'IOError: [Errno 32] Broken pipe'

##### v1.5.0
- Disable the pagination and add a --color option. Thanks for the suggestions from @jhermann
- Speed up result display with CachingMiddleware of TinyDB

##### v1.4.9
- Fix workflow for Alfred v2

##### v1.4.8
- Fix Alfred XML output
- Rewrite Alfred workflow script

##### v1.4.5
- Drop Python 2.6 Support
- Update docs: using ~/.netrc + cron. @jhermann

##### v1.3.5
- Output Alfred 3 JSON ouput with "-a -3" option.
- Import Alfred Workflow with "-i" (append "-3" for Alfred 3) option.

##### v1.2.3
- Get user + password from netrc. @jhermann.
- Use pipenv to manage project requirements.

##### v1.1.3
- Upgrade to TinyDB 3.7.0.
- Build index when updating.
- Search result pagination.

*Note*
- Uninstall existing version.
- Rebuild existing index with `mystars -r`.

##### v1.0.2
- Rename to oh-my-stars.

##### v1.0.1
- Support Github two-factor authentication. @yanyaoer

##### v1.0.0

- Replace kc with [TinyDB](https://github.com/msiemens/tinydb), no more non-python dependencies.
- Only update stars since last time.
