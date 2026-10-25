#!/usr/bin/env python3
"""Read-only dependency report; does not install tools."""
import sys, shutil, json
report={'python':sys.version.split()[0], 'python_supported':sys.version_info >= (3,9), 'tools':{x:shutil.which(x) for x in ['ffmpeg','ffprobe','node','npm']}, 'advanced_tools':'Not detected automatically. Verify Hyperframes, transcription, masks and tracking in the project.'}
print(json.dumps(report,indent=2))
sys.exit(0 if report['python_supported'] and report['tools']['ffmpeg'] and report['tools']['ffprobe'] else 1)
