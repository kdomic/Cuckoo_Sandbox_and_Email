#!/usr/bin/env python
import imaplib


def get_emails(email_ids):
    data = []
    for e_id in email_ids:
        _, response = imap_server.fetch(e_id, '(UID BODY[TEXT])')
        data.append(response[0][1])
    return data

def get_subjects(email_ids):
    subjects = []
    for e_id in email_ids:
        _, response = imap_server.fetch(e_id, '(body[header.fields (subject)])')
        subjects.append( response[0][1][9:] )
    return subjects

def emails_from(name,imap_server):
    '''Search for all mail from name'''
    status, response = imap_server.search(None, '(FROM "%s")' % name)
    email_ids = [e_id for e_id in response[0].split()]
    print 'Number of emails from %s: %i. IDs: %s' % (name, len(email_ids), email_ids)
    return email_ids


###MAIN


print "start"
imap_server = imaplib.IMAP4("localhost.com",143)
imap_server.login("korisnik1@localhost.com", "123456")

imap_server.select('INBOX')


#LAST 3
for email in get_emails(emails_from("kdomic",imap_server)):
    print email

imap_server.close()
imap_server.logout()



print "end"

'''

# Count the unread emails
status, response = imap_server.status('INBOX', "(UNSEEN)")
unreadcount = int(response[0].split()[2].strip(').,]'))
print unreadcount

# Search for all new mail
status, email_ids = imap_server.search(None, '(UNSEEN)')
print email_ids


import imaplib

imap_server = imaplib.IMAP4("localhost.com",143)
imap_server.login("korisnik1", "123456")

imap_server.select('INBOX')


imap_server.close()


#status, size = imap_server.select('Inbox')
#print status

#rv, mailbox = imap_server.list()
#print mailbox


typ, data = imap_server.select('Inbox')

for num in data[0].split():
    typ, data = imap_server.fetch(num, '(RFC822)')
    print 'Message %s\n%s\n' % (num, data[0][1])





'''
