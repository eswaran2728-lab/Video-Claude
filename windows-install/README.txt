Windows install (Claude Code on your PC):
1. Install Node 22+, Python 3, ffmpeg, then:  pip install numpy soundfile
2. Unzip clean-cut-windows.zip into  %USERPROFILE%\.claude\skills\   (gives clean-cut\ and video-style-picker\)
3. Run once:  python %USERPROFILE%\.claude\skills\clean-cut\setup\apply_profile.py --set transcriber=local font_main_name=Inter "font_main_bold={\"file\":\"Inter-Bold.otf\"}"
   then: python %USERPROFILE%\.claude\skills\clean-cut\setup\apply_profile.py
4. Add HyperFrames:  claude plugin marketplace add heygen-com/hyperframes ; claude plugin install hyperframes@hyperframes
5. npx hyperframes doctor   (Chrome shell + FFmpeg must be green; Docker/TTS/BGM are optional)
Never paste an ElevenLabs key in chat; if you want it, set ELEVENLABS_API_KEY as a Windows environment variable yourself.
