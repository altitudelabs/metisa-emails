# -*- coding: utf-8 -*-
import pandas as pd
from email.utils import parseaddr

""" Parameters """
input_file = '/Users/justinyek/Sites/venture-env/metisa-mailinglist/magento.csv'
output_file = '/Users/justinyek/Sites/venture-env/metisa-mailinglist/magento_output.csv'
description = 'magento'

""" Helper methods """
def expand_emails_into_separate_rows(df):
    """
    Email column contains a ; separated list of emails
    This method expands each email into a separate row
    """
    df = df[pd.notnull(df['Emails'])]
    df_emails = pd.DataFrame(df.Emails.str.split(';').tolist(), index=df.Domain).stack()
    df_emails = df_emails.reset_index()
    del df_emails['level_1']
    df_emails.columns = ['Domain', 'Email']

    del df['Emails']
    return df_emails.merge(df, on='Domain', how='left')

def is_valid_email(x):
    """
    Checks whether an email is a valid lead
    e.g. do not send emails to privacy@ email addresses
    """
    email = x['Email']
    stopwords = [
        'abuse',
        'account',
        'admin',
        'advert',
        'affiliate',
        'ask',
        'assist',
        'bcc',
        'blog',
        'broker',
        'buy',
        'cancel',
        'care',
        'catalog',
        'catering',
        'championship',
        'circulation',
        'comm',
        'commercial',
        'compliance',
        'concierge',
        'contact',
        'copyright',
        'corp',
        'courier',
        'courrier',
        'cs@',
        'csr',
        'cust',
        'customer',
        'decline',
        'delivery',
        'design',
        'digital',
        'dispatch',
        'donotcall',
        'donat',
        'drive',
        'employment',
        'english',
        'enquiries',
        'espanol',
        'event',
        'fabric',
        'facebook',
        'fans',
        'feedback',
        'formation',
        'freight',
        'global',
        'group',
        'headquarter',
        'hello',
        'help',
        'hny',
        'hr',
        'image',
        'impact',
        'info',
        'inquiry',
        'insider'
        'international',
        'issue',
        'ir',
        'job',
        'learn',
        'legal',
        'letter',
        'licensing',
        'lost',
        'mail',
        'management',
        'marketing',
        'media',
        'member',
        'merch',
        'newsletter',
        'office',
        'online',
        'order',
        'part',
        'permission',
        'picture',
        'pinterest',
        'post',
        'pr@',
        'press',
        'privacy',
        'product',
        'public',
        'radio',
        'reach',
        'reader',
        'recruit',
        'regulatory',
        'repairs',
        'research',
        'resources',
        'return',
        'review',
        'rivacy',
        'rsvp',
        'sale',
        'secretar',
        'seminar',
        'sender',
        'serv',
        'service',
        'shipping',
        'shop',
        'social',
        'staff',
        'store',
        'submissions',
        'subscribe',
        'support',
        'system',
        'team',
        'tech',
        'tickets',
        'track',
        'training',
        'twitter',
        'volunteer',
        'warranty',
        'web',
        'wecare',
        'welcome',
    ]

    # Is email format valid?
    f, e = parseaddr(email)
    if not e:
        return False

    # Does email contain any invalid words
    if any(w in email for w in stopwords):
        return False

    return True

""" Main script starts here """
df = pd.read_csv(input_file)
df = expand_emails_into_separate_rows(df)

df = df[df.apply(is_valid_email, axis=1)]

df_result = df[['Email', 'Domain', 'Company']]
df_result.columns = ['email', 'first_name', 'last_name']
df_result['description'] = description

print len(df_result), 'contacts filtered.'
df = df_result.to_csv(output_file, index=False)