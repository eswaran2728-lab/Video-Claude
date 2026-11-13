import json, subprocess, sys, os
VOICES = {  # voice, rate, pitch
 'narrator':   ('ta-MY-SuryaNeural', '-15%', '-2Hz'),
 'teacher':    ('ta-SG-AnbuNeural',  '-10%', '-4Hz'),
 'researcher': ('ta-IN-ValluvarNeural', '-4%', '+0Hz'),
 'elder':      ('ta-LK-KumarNeural', '-22%', '-10Hz'),
}
lines = json.load(open('lines.json'))
only = sys.argv[1:]
for L in lines:
    if only and L['id'] not in only: continue
    v, rate, pitch = VOICES[L['sp']]
    rate = L.get('rate', rate)
    mp3 = f"audio/voice/{L['id']}.mp3"
    subprocess.run(['python3', 'tools/tamil_tts.py', v, mp3, L['t'], rate, pitch], check=True)
    wav = mp3[:-4] + '.wav'
    # trim edge silence, 48 kHz mono
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',mp3,'-af',
        'silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse',
        '-ar','48000','-ac','1',wav], check=True)
    d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',wav]))
    win = L['e'] - L['s']
    print(f"{L['id']:6} {L['sp']:10} {d:5.2f}s window {win:4.1f}s {'OVER' if d > win + 0.3 else ''}")
