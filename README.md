# Schoology Scraper

## What is it?

This will use a Schoology API token to grab events and assignments from Schoology, and puts them into a google sheet.

From there, you can do whatever you'd like.  

### But why?

It is difficult to track assignments in Schoology (as used by at least one school) - 
Each class displays an upcoming list of items, but they go away on their due dates.  Any 
looking backwards requires looking at a calendar view.  

### Implementation details

* Schoology has two structures of interested - events and assignments.
* Nearly all assignments have correlated events.  It looks like events
are the record used for calendar and upcoming views. 
* There is a lot of overlap between events and assignments - maybe 80% overlap, but 
each list has 10-20% unique entries for my child.
* Since events have an assignment_id field, I first get events, and then add assignments
that are not linked from the events to get 100% coverage.  I believe assignments are linked
to grade objects, etc, but I haven't spent time there.  
* The code assumes you are using a 'parent' account API token, and discovers your child
from that.  At one point I had support for multiple children per parent, but took it out 
to make debugging easier.  It's not hard to add back in.  

---

#### what do you need to get started? 
in config/config.py:
* Schoology creds
  * ology_key , ology_sec = key and sec token (strings) from your account
* header translation
  * the headers you want to put in sheets (per event and assignment types)
  * ev_hdrs = ['id',  'course_title', 'title', 'start',  'web_url']
  * as_hdrs = ['id',  'course_title', 'title', 'due',    'web_url']
* sheets info
  * hw_ss_id = string, sheet ID of your google sheet
  * he_range = string, ID of the sheet/range.  I use an entire sheet

Additionally, you need to create config/credentials.json with google API creds.

You will still need to auth to google - running sheets_test.py will do this like
the google quickstart example using a hacky localhost webserver. 
Once you do that, it will write config/token.pickle.  

---

### TODOs
* That token will expire, and running this from cron would fail poorly.  
(hang forever?) Probably need to separate loading creds from pickle 
(failing if creds are bad) and obtaining cresds. 
* My use case needs some checkboxes added to each row - 
i currently add them later by selecting an area and 'insert checkbox'.  
Looks like it requires a little dance, but should be able to append 'n' 
checkboxes to each row via API instead.  
* to ensure no conflict, assignments are added as negative IDs in the target sheet
* deal with changed/removed events/assignments ... 
* hold local state and make sheets input and destroyable...
 
