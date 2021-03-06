"""
Using this script you can actually redact your data,
be careful to not delete stuff you want to keep!
"""

# TODO: Use functions in package instead of the nested mess here

import re

from aw_client import ActivityWatchClient


def main(dryrun=True):
    # TODO: Use wordlist instead of argument
    sensitive_words = ["sensitive"]

    aw = ActivityWatchClient(testing=True)

    re_word = r'\b{}\b'

    buckets = aw.get_buckets()
    for bid in buckets.keys():
        if "window" not in bid:
            continue

        print("Checking bucket: {}".format(bid))

        events = aw.get_events(bid, limit=-1)
        old_matches = set()
        for event in events:
            for key, val in event.data.items():
                if isinstance(val, str):
                    matches = [re.findall(re_word.format(word), val.lower())
                               for word in sensitive_words]
                    matches = set(sum(matches, []))
                    if matches:
                        event.data[key] = "REDACTED"
                        if val not in old_matches:
                            print(f"{'(DRYRUN) ' if dryrun else ''} Matches: {matches}, redacting: {val}")
                            old_matches.add(val)
                        if not dryrun:
                            aw.insert_event(bid, event)


if __name__ == "__main__":
    main()
