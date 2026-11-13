# The creator's four Partner Briefing scripts (voiceover verbatim). Each scene: (title, slides, voiceover). The voice gets
# pronunciation help only (spoken()); captions show the text as written.
import re
VIDEOS = {
 "v1_foca": dict(code="AA/SEC/F/070", name="FOCA Checklist", audience="Airline Representatives of foreign air carriers", export="01_FOCA_Checklist_Partner_Guide.mp4",
  signer="AIRLINE REPRESENTATIVE", scenes=[
  ("Security hands you the phone", "1–6", "Security has filled in the FOCA Checklist and hands you the phone. If you are the Airline Representative, your job is to check the checklist and sign it. You use Security’s phone. There’s no app to install and no account to sign in to."),
  ("Check the details", "7–8", "Tap the orange button to show that you have the phone. Read the flight details. Then check each line that Security has marked. If anything is wrong, tap ‘Something is wrong’ and give the phone back to Security."),
  ("Sign and confirm", "9–10", "If everything is correct, type your own name and ID or staff number. Sign in the box with your finger. If you need to redo your signature, tap ‘Clear’ and sign again. Then tap ‘Confirm my signature’."),
  ("Give the phone back and receive the PDF", "11–14", "When the screen asks, give the phone back to Security. Security signs and saves the record. The app creates a signed PDF with a Record ID. AirAsia Security keeps it in a restricted folder and logs the record. Security emails you a copy of the signed PDF. Keep it for your records."),
 ]),
 "v2_notoc": dict(code="AA-SEC-F-063", name="NOTOC (Firearm)", audience="Captains / Pilots in Command", export="02_NOTOC_Partner_Guide.mp4", signer="CAPTAIN", scenes=[
  ("Security hands the phone to the Captain", "1, 6–7", "Security fills in the NOTOC form and hands the phone to you, the Captain. You check and sign on that same phone. Tap the orange button marked ‘Captain has the phone’."),
  ("Review the details", "8, 10", "Check the flight details. Review each entry on the form and check the ‘Loaded by’ name. If anything is wrong, tap ‘Something is wrong’ and give the phone back to Security for correction."),
  ("Enter your details and sign", "9–10", "If everything is correct, type your own name in ‘Acknowledged by’. Enter your ID number. Sign with your finger. If you need to sign again, tap ‘Clear’. When your signature is ready, tap ‘Confirm my signature’."),
  ("Return the phone and receive the PDF", "11–14", "When the screen asks, give the phone back to Security. Security signs and saves the record. The signed PDF has a Record ID. AirAsia Security keeps it in a restricted folder and logs the record. Security emails you a copy for your records."),
 ]),
 "v3_aor": dict(code="AA/SEC/F/007", name="Acknowledgement of Receipt", audience="Staff handing over items, CBTO staff, and witnesses", export="03_Acknowledgement_of_Receipt_Partner_Guide.mp4",
  signer="SIGNER", scenes=[
  ("Find your situation", "1–5", "There are two situations. In Situation A, you hand items to Security. In Situation B, Security hands items to CBTO. Security fills in the form and brings the phone in both situations. First, check who is receiving the items."),
  ("Situation A — Staff hands items to Security", "6–11", "If you are handing items to Security, Security signs first as the recipient. Then it is your turn. Check your name, your role, and the items listed. If everything is correct, sign with your finger and tap ‘Confirm’. Tap ‘Clear’ if you need to sign again. Next, the witness checks their own name, signs, and taps ‘Confirm’. The witness gives the phone back to Security."),
  ("Situation B — Security hands items to CBTO", "12–18", "If Security hands items to CBTO, the CBTO staff member signs first as the recipient. If that is you, check your name. Scroll up and check each item you received. Sign with your finger and tap ‘Confirm’. Pass the phone back to Security. Security signs as ‘Handed over by’. The witness checks their own name, signs, taps ‘Confirm’, and gives the phone back to Security."),
  ("Wrong details and the signed copy", "19–21", "If a name, role, or item is wrong, tell Security before signing. Each person signs for themselves. After everyone has signed, Security saves the record. The app creates a signed PDF with a Record ID. AirAsia Security keeps it in a restricted folder and logs the record. Security emails you a copy for your records."),
 ]),
 "v4_search": dict(code="AA/SEC/F/008", name="Search List", audience="The person searched and the witness, if present", export="04_Search_List_Partner_Guide.mp4", signer="PERSON SEARCHED", scenes=[
  ("See who signs first", "1, 5–6", "Security fills in the Search List and hands you the phone. If you are the person searched, you sign first. If a witness is present, they sign next. Security signs and saves the record."),
  ("Check your name and the items", "6–7, 12", "Check that the orange box shows your name. Scroll up and read the search details. Check that the items found are listed correctly. If nothing was found, the form should say ‘Nil’. If anything is wrong, tell Security before you sign."),
  ("Sign and confirm", "8–10", "If everything is correct, sign with your finger. Tap ‘Clear’ if you need to sign again. Then tap ‘Confirm’. If a witness is present, they check their own name, sign, and tap ‘Confirm’. When the screen asks, give the phone back to Security."),
  ("Where the signed copy goes", "11–13", "Security signs and saves the record. The signed PDF has a Record ID. AirAsia Security keeps it in a restricted folder and logs the record. Security emails you a copy of the signed Search List. Keep it for your records."),
 ]),
}
SAY = [(r"\bNOTOC\b", "No-tock"), (r"\bCBTO\b", "C B T O"), (r"\bIDs?\b", "I D"), (r"\bPDF\b", "P D F"), (r"[‘’“”]", lambda m: "" if m.group(0) in "‘“" else ("'" if m.group(0) == "’" else "")),
       (r"There's", "There's")]


def spoken(t):
    t = t.replace("’", "'")
    for a, b in SAY:
        t = re.sub(a, b, t)
    t = re.sub(r"(?<=\w)'(?=\s|[.,])", "", t)          # closing single quotes used as marks
    return t


def sentences(p):
    return [s.strip() for s in re.split(r"(?<=[.?!’])\s+(?=[A-Z‘])", p) if s.strip()]
