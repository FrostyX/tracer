from tracer.resources.lang import _

def render(args=None, total_count=None, session_count=None, static_count=None):

	if not args.quiet and (session_count > 0 or static_count > 0):

		print "\n" + _("note_unlisted_apps")
		if session_count > 0:
			print _("requiring_session").format(session_count)

		if static_count > 0:
			print _("requiring_reboot").format(static_count)

