#!/usr/bin/python

import time
import praw
import re
import logging

r = praw.Reddit('GNU/Linux rms Reddit bot'
                'https://github.com/013'
				'')
r.login('WhatYouAreReferring2', 'linnit')
# All comments that have been replied to shall be put into the 'already_done' list
already_done = []
# Subreddits to find comments
subSearch = 'linux+gnu+linuxquestions+linuxadmin+linux4noobs+kernel+unixporn+DistroHopping+LinuxActionShow+Ubuntu+linuxmint+opensuse+Gentoo+Fedora+Debian+crunchbang+centos+ArchLinux+unix+technology+games+gaming'

RMSPasta = """
I'd just like to interject for one moment. What you're referring to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.

Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called "Linux", and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.

There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine's resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called "Linux" distributions are really distributions of GNU/Linux.
"""
SealPasta = """
What the fuck did you just fucking say about me, you little proprietary bitch? I'll have you know I graduated top of my class in the FSF, and I've been involved in numerous secret raids on Apple patents, and I have over 300 confirmed bug fixes. I am trained in Free Software Evangelizing and I'm the top code contributer for the entire GNU HURD. You are nothing to me but just another compile time error. I will wipe you the fuck out with precision the likes of which has never been seen before
on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am building a GUI using GTK+ and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can decompile you in over seven hundred ways, and that's just with my Model M. Not only am I extensively
trained in EMACS, but I have access to the entire arsenal of LISP functions and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little "clever" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit Freedom all over you and you will drown in it.
"""

gnuPastaEX = '(^|\s)L\s*(i\W*n\W*u\W*|l\W*u\W*n\W*i\W*|o\W*o\W*n\W*i\W*)x(?!\s+kernel)' # Expression to find comments
hatePastaEX = 'fuck (linux|stallman|gpl)|stallman bot|stallmanbot|stallmanbots|stallbots|stallbot|rmsbot|stallman pls go|Shut your filthy hippy mouth, Richard' # Find hate comments

# All comment IDs will be logged in interject.log
logging.basicConfig(filename="interject.log", level=logging.INFO)

def logInterject(id):
	logging.info("Interjected Comment ID: {0}".format(id))

def interject(pasta, cID, r=False):
	# Once a comment has been found, this function will try and reply to it
	try:
		comment.reply(pasta)
	except Exception, e:
		# If the bot has commented to much - It will throw an error
		
		nEX = re.compile('.+?(\d+)')
		# print e
		a = int( nEX.search(str(e)).group(1) )
		# Find the waiting time in the error
		# and sleep for that amount of time
		if a > 10:
			print "Interject error - Sleeping for 120"
			time.sleep(120)
		else:
			t2s = (a+1) * 60
			print "Interject error - Sleeping for {0}".format(t2s)
			time.sleep(t2s)
		interject(pasta, cID, True)
	if r == False:
		logInterject(cID)
		already_done.append(cID)
		print "Interjecting: {0}".format(cID)
		time.sleep(60)
		# Wait a minute after every comment to avoid spam

try:
	# Load previously interjected comments
	# as not to interject them again
	file = open('interject.log', 'r')
	for text in file.readlines():
		text = text.rstrip()
		regex = re.findall(r'.+:.+:.+?ID:.(.+)', text)
		if len(regex) == 1:
			regex = regex[0]
			if regex is not None and regex not in already_done:
				already_done.append(regex)
	file.close
except IOError, (errno, strerror):
	print "I/O Error(%s) : %s" % (errno, strerror)

while True:
	multiReddit = r.get_subreddit(subSearch)
	multiRedditComments = multiReddit.get_comments()
	
	for comment in multiRedditComments:
		if comment.id not in already_done:
			if re.search(hatePastaEX, comment.body, re.M|re.I):
				interject(SealPasta, comment.id)
			elif re.search(gnuPastaEX, comment.body, re.M|re.I):
				interject(RMSPasta, comment.id)
	# Wait 2 minutes before searching for more comments
	print "Sleeping for 120"
	time.sleep(120)

