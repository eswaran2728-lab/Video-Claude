"""Tamil TTS via edge-tts, trusting the sandbox proxy CA.
usage: tamil_tts.py VOICE OUT.mp3 "text" [rate] [pitch]"""
import asyncio, os, ssl, sys
import edge_tts.communicate as c
c._SSL_CTX = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE', '/root/.ccr/ca-bundle.crt'))
import edge_tts

async def main():
    voice, out, text = sys.argv[1:4]
    rate = sys.argv[4] if len(sys.argv) > 4 else '+0%'
    pitch = sys.argv[5] if len(sys.argv) > 5 else '+0Hz'
    com = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, proxy=os.environ.get('HTTPS_PROXY'))
    await com.save(out)

asyncio.run(main())
