#!/usr/bin/env python3

from urllib import request, error
import json, os, fnmatch, textwrap, time, sys, re

srs = ["worldnews", "usnews", "deals", "gamedeals", "leetcode"]
URL_TEMPLATE = "https://www.reddit.com/r/{subreddit}/hot.json?limit=10&t=today"
def url_gen(subs):
    for s in subs:
        yield (URL_TEMPLATE.format(subreddit=s), s)

def url_dump(url_gen):
    ret = []
    for url, subreddit in url_gen:
        try:
            u = request.urlopen(url)
        except error.HTTPError as err:
            if err.code == 429:
                print(f'Have to sleep for {subreddit}')
                time.sleep(5)
                try:
                    u = request.urlopen(url)
                except error.HTTPError as err:
                    if err.code == 429:
                        print(f'failed again... return stale data')
                        break

        resp = json.loads(u.read().decode('utf-8'))
        with open(f'./reddit-{subreddit}.json', 'wt') as f:
            json.dump(resp, f)
        ret.append(f"./reddit-{subreddit}.json")
    return ret


def filenames_gen(root):
    pat_str = "(" + "|".join(srs) + ").json"
    pat = re.compile(pat_str)
    for f in fnmatch.filter(os.listdir(root), '*.json'):
        if pat.search(f):
            yield os.path.join(os.path.abspath(os.curdir), f)

def openfile_gen(files):
    for f in files:
        with open(f) as fs:
            data = json.load(fs)
            print(format(f.split('/')[-1], "*^80s"), end="\n\n")
            [print(textwrap.fill(t['data']['title'], 85),t['data']['url'], sep="\n", end="\n\n") for t in data['data']['children']]
            
if __name__ == '__main__':
    args = sys.argv
    ug = url_gen(srs)
    fn = url_dump(ug)
    fns = filenames_gen(".")
    openfile_gen(fns)


# dict_keys(['approved_at_utc', 'subreddit', 'selftext', 'author_fullname', 'saved', 
# 'mod_reason_title', 'gilded', 'clicked', 'title', 'link_flair_richtext', 
# 'subreddit_name_prefixed', 'hidden', 'pwls', 'link_flair_css_class', 'downs', 
# 'top_awarded_type', 'hide_score', 'name', 'quarantine', 'link_flair_text_color', 
# 'upvote_ratio', 'author_flair_background_color', 'subreddit_type', 'ups', 
# 'total_awards_received', 'media_embed', 'author_flair_template_id', 
# 'is_original_content', 'user_reports', 'secure_media', 'is_reddit_media_domain', 
# 'is_meta', 'category', 'secure_media_embed', 'link_flair_text', 'can_mod_post', 
# 'score', 'approved_by', 'is_created_from_ads_ui', 'author_premium', 'thumbnail', 
# 'edited', 'author_flair_css_class', 'author_flair_richtext', 'gildings', 
# 'content_categories', 'is_self', 'mod_note', 'created', 'link_flair_type', 
# 'wls', 'removed_by_category', 'banned_by', 'author_flair_type', 'domain', 
# 'allow_live_comments', 'selftext_html', 'likes', 'suggested_sort', 
# 'banned_at_utc', 'url_overridden_by_dest', 'view_count', 'archived', 'no_follow', 
# 'is_crosspostable', 'pinned', 'over_18', 'all_awardings', 'awarders', 'media_only', 
# 'can_gild', 'spoiler', 'locked', 'author_flair_text', 'treatment_tags', 'visited', 
# 'removed_by', 'num_reports', 'distinguished', 'subreddit_id', 'author_is_blocked', 
# 'mod_reason_by', 'removal_reason', 'link_flair_background_color', 'id', 
# 'is_robot_indexable', 'report_reasons', 'author', 'discussion_type', 'num_comments', 
# 'send_replies', 'whitelist_status', 'contest_mode', 'mod_reports', 
# 'author_patreon_flair', 'author_flair_text_color', 'permalink', 
# 'parent_whitelist_status', 'stickied', 'url', 'subreddit_subscribers', 
# 'created_utc', 'num_crossposts', 'media', 'is_video'])
