#AvivoreXT

###The Twitter-searching Data Miner

AvivoreXT is a multi-threaded, Python-based tool that searches Twitter for
keywords and then parses any tweets that are found. For maximum data coverage
AvivoreXT uses a mix of issuing classic search queries to the Twitter API and
monitoring the Twitter Streaming API.  

A configuration file defines search terms and regular expressions that are used
to extract data. It presently uses a SQLite back-end to store the data that is
found and outputs results via stdout.

With the sample configuration file AvivoreXT looks for the following sort of
data:

* Phone numbers in NPA-NXX format (ex: 604-555-1212)
* IPv4 addresses (127.0.0.1)
* Blackberry PINs (ABCDEF12)

**Of course, more data sets can be defined in the configuration file.**

AvivoreXT is based on Avivore originally developed by [Colin Keigher](https://github.com/ColinKeigher/Avivore).


###Requirements

* Python 2.7
* SQLite3
* [Python Twitter API](https://github.com/soxohsix/twitter)

Optional:

* [sqliteboy](https://github.com/nopri/sqliteboy) for SQLite web front-end


###Installation

Follow these installation steps in order to install AvivoreXT in a virtual
python environment. In case `virtualenv` is not available on your system, you'll need to install
package `python-virtualenv` for Debian/Ubuntu based distros or Archlinux.

1. Clone AvivoreXT repository:

        $ git clone https://github.com/rc0r/AvivoreXT

2. Create a virtual environment using `virtualenv` pointing it to `python2.7`
(we don't have Python3 support yet):

        $ cd AvivoreXT
        $ virtualenv -p /usr/bin/python2.7 venv

3. Switch to virtual environment:

        $ source venv/bin/activate

4. Run the provided setup script to install AvivoreXT and all requirements:

        $ python setup.py install

5. Now in your virtual environment you can run AvivoreXT like this:

        $ avivore --help

Now you're almost good to go. Check the next section for configuration and
usage instructions.


###Configuration & Usage

First, an AvivoreXT configuration file needs to be created. Probably the easiest
way to do this is to make a copy from the provided sample configuration file.
Now, with the editor of your choice set configuration options `consumer_key`
and `consumer_secret` in section `twitter_auth`. Both values can be obtained
from https://dev.twitter.com/apps after registration of a new Twitter app.
Comments explain all remaining options in the config file. After defining data
sets and search terms as needed you're good to go. Both are located in sections
`twitter_search_objects` and `twitter_search` respectively. [Tracking keywords](
https://dev.twitter.com/streaming/overview/request-parameters#track)
that are used to monitor the Twitter Streaming API can be configured by setting
the option `stream_tracking_keyword` which is also found in section
`twitter_search`. Check out the sample config file `sample.conf` for more
information regarding the configuration options!

Running AvivoreXT is quite easy:

	$ cp sample.conf avivore.conf
	# edit config file according to needs
	# start mining
	$ python ./avivore.py -c avivore.conf
	
When AvivoreXT is executed for the first time you'll be redirected to your
browser to authenticate AvivoreXT to your user account. This is necessary
because access to the Twitter Streaming API requires user based authentication.
After you approved AvivoreXT in your browser, a PIN number is displayed. Switch
back to the terminal and enter it. This step has to be performed only once. The
generated user tokens will be stored in the credentials file that was set in the
configuration file (option `credentials_file` in section `twitter_auth`).

An alternative to using a classic configuration file is to use a SQLite3
database that holds the AvivoreXT settings. Check out the provided
`sample_conf.db` for the necessary tables and table layouts. It is possible to
use the same database file for configuration and data storage. When using an
appropriate front-end database configuration allows for remote miner setup. To
run AvivoreXT with a database configuration use:

	$ python ./avivore.py -d sample_conf.db

Be sure to add both `consumer_key` and `consumer_secret` in table `config` of
`sample_conf.db` before running AvivoreXT!


###Notes on a front-end

Since AvivoreXT uses a SQLite3 database there exist quite a few options to use
some kind of graphical front-end for database management and inspection.
Recently I have been using [sqliteboy](https://github.com/nopri/sqliteboy) (see
screenshots below) as it is quite lean, provides a clean web interface and
allows for remote database access.

If the need arises for special AvivoreXT-related features, it's conceivable to
integrate a similar interface into AvivoreXT with some useful extensions. If you
think there's such a feature or AvivoreXT should have an integrated front-end,
just let me know. Ideas and feature requests are always welcome.


###Hacking

You've got an idea for a nice AvivoreXT feature, found some bugs or just want
to get your hands on some AvivoreXT coding? Then you're kindly invited to
check out the [Issues](https://github.com/rc0r/AvivoreXT/issues) section of the
repo for feature requests, open tasks or any questions you might have. Your pull
requests with some bugfix or some shiny new feature are always welcome! Don't
know where to start? Following you'll find a (rather incomplete) list of things
that would be nice to have:  

* python3 support
* notification support (see [#8](https://github.com/rc0r/AvivoreXT/issues/8))
* add more data sources (just to name a few: pastebin, google, facebook, reddit)
* tests! (perspective: some integrated build, test, deployment work flow)
* some neat UI for configuration and result display (preferentially web based)
* anything else found in [Issues](https://github.com/rc0r/AvivoreXT/issues)

Feel free to get in touch outside of Github. My  Twitter handle is [@_rc0r](https://twitter.com/_rc0r).


###Screenshots

AvivoreXT v1.2.1 back-end

![ScreenShot](https://raw.github.com/rc0r/AvivoreXT/master/scrots/AvivoreXT-Backend.png)

[sqliteboy](https://github.com/nopri/sqliteboy) featured web front-end

![ScreenShot](https://raw.github.com/rc0r/AvivoreXT/master/scrots/AvivoreXT-Webfront.png)
