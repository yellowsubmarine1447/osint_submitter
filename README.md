# osint_submitter
Template website for submitting solutions to OSINT CTF challenges via a map (through lat/long coords). Hosted at [http://yellowsubmarine.xyz:8000/](http://yellowsubmarine.xyz:8000).

Code is super unclean and probably prone to issues like floating point accuracy and time desyncs.

The originally intended RATELIMIT (see [/app.py](/app.py)) was 60 seconds, but for the purposes of demonstration it's set to 10 seconds.
