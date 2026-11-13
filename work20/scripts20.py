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
SAY = [(r"Handed over by, you\.", "Handed over by. You."), (r"\bNOTOC\b", "No-tock"), (r"\bCBTO\b", "C B T O"), (r"\bIDs?\b", "I D"), (r"\bPDF\b", "P D F"), (r"[‘’“”]", lambda m: "" if m.group(0) in "‘“" else ("'" if m.group(0) == "’" else "")),
       (r"There's", "There's")]


def spoken(t):
    t = t.replace("’", "'")
    for a, b in SAY:
        t = re.sub(a, b, t)
    t = re.sub(r"(?<=\w)'(?=\s|[.,])", "", t)          # closing single quotes used as marks
    return t


def sentences(p):
    return [s.strip() for s in re.split(r"(?<=[.?!’])\s+(?=[A-Z‘])", p) if s.strip()]


# ---------------- v02: every slide explained, in deck order (text taken from each slide; no new facts) ----------------
# scene = (title, [(slide, voiceover for that slide), ...])
_CHANGED = ("Here is what changed. Before, this was a printed paper form, signed with a pen. Now it is the same form, on the Security officer’s phone. "
            "You sign with your finger, and the signed PDF is saved automatically, in a restricted AirAsia folder.")
_STEPS = ("Every form works in four steps. Security fills the form, and hands you the phone. You check, type your name and ID, and sign. "
          "Then the phone goes back, and Security signs and saves. Blue is Security. Orange is you.")
_NEED = ("You need nothing to install, and no account. Security brings the phone. Have your own name and ID or staff number ready. "
         "Read the form before you sign, and if it is wrong, say so. Sign only for yourself.")
_REMEMBER = ("Remember: check your name and role on screen, and read the details before signing. Type your own name and ID if asked. Sign with your finger, then Confirm, and hand the phone back to Security. "
             "Don’t sign for someone else, or if the details are wrong. Don’t close the app, press Back, or take photos of the screen.")
_WHERE = ("Your signature goes into one signed PDF per form, with every signature and a Record ID. It is saved to a restricted AirAsia folder, with a record log. "
          "A PDF copy of the signed {f} is shared with you by email. Have a question? Ask the Security staff on duty.")
_LAST = "When the screen says so, give the phone back to Security. Security signs and saves the record."
VIDEOS2 = {
 "v1_foca": dict(VIDEOS["v1_foca"], scenes=[
  ("What changed", [(1, "Security has filled in the FOCA Checklist and hands you the phone. This guide is for Airline Representatives of foreign air carriers."), (2, _CHANGED)]),
  ("How it works", [(3, _STEPS), (4, _NEED), (5, "This part is for the Airline Representative of a foreign carrier.")]),
  ("The paper form we used", [(6, "This is the paper form we used. Security fills pages one and two. On page two, the Security Rep signs, and the Airline Representative signs. "
                                  "The app shows the same form, so your job is the same: check the checklist and sign it.")]),
  ("Check the details", [(7, "In the app, Security fills the form, then hands you the phone. Tap the orange button to show that you have the phone."),
                         (8, "Read the flight details. Then check each line that Security has ticked. If anything is wrong, tap ‘Something is wrong’. The phone goes back to Security.")]),
  ("Sign and confirm", [(9, "If everything is correct, type your own name and ID or staff number. Sign in the box with your finger."),
                        (10, "Not happy with the signature? Tap ‘Clear’ and sign again. Then tap ‘Confirm my signature’.")]),
  ("Phone back and the signed PDF", [(11, _LAST), (12, "Security saves, and the app creates the signed PDF. This is a real signed PDF from a TEST record. Security staff email the PDF to you. Keep it for your records.")]),
  ("Remember", [(13, _REMEMBER), (14, _WHERE.format(f="FOCA Checklist"))]),
 ]),
 "v2_notoc": dict(VIDEOS["v2_notoc"], scenes=[
  ("What changed", [(1, "Security fills in the NOTOC form and hands the phone to you, the Captain. The NOTOC for firearms is now signed on a phone."), (2, _CHANGED)]),
  ("How it works", [(3, _STEPS), (4, _NEED), (5, "This part is for the Captain, the Pilot in Command. Security fills, the Captain checks and signs, and Security signs and saves.")]),
  ("The paper form we used", [(6, "This is the paper form we used. Security fills the firearm details, and signs as ‘Loaded by’. "
                                  "The Captain checks the flight and firearm details, types their own name and ID, and signs to acknowledge.")]),
  ("Check the details", [(7, "In the app, Security fills the form, then hands you the phone. Tap the orange button marked ‘Captain has the phone’."),
                         (8, "Check the flight details. Review every firearm line on the form, and check the ‘Loaded by’ name.")]),
  ("Sign and confirm", [(9, "If everything is correct, type your own name in ‘Acknowledged by’. Enter your ID number. Sign in the box with your finger."),
                        (10, "If you need to sign again, tap ‘Clear’. If anything in the form is wrong, tap ‘Something is wrong’ and give the phone back to Security for correction. "
                             "When your signature is ready, tap ‘Confirm my signature’.")]),
  ("Phone back and the signed PDF", [(11, _LAST), (12, "This is a real Saved screen from a TEST record. The app creates the signed PDF, and the Record ID is in the PDF file name. "
                                                       "Security staff email the PDF to you. Keep it for your records.")]),
  ("Remember", [(13, _REMEMBER), (14, _WHERE.format(f="NOTOC"))]),
 ]),
 "v3_aor": dict(VIDEOS["v3_aor"], scenes=[
  ("What changed", [(1, "Security fills in the Acknowledgement of Receipt and brings the phone. This guide is for staff handing items to Security, CBTO staff, and witnesses."),
                    (2, "Before, this was a printed paper form, signed with a pen. Now it is the same form, on the Security officer’s phone, and the signed PDF is saved automatically.")]),
  ("How it works", [(3, "Every form works in four steps. Security fills the form, and hands you the phone. You check and sign. Then the phone goes back, and Security signs and saves. Blue is Security. Orange is you."),
                    (4, "There is nothing to install, and no account. Read the form before you sign, and sign only for yourself."),
                    (5, "One form, two situations. In Situation A, staff hand items to Security. In Situation B, Security hands items to CBTO. "
                        "In both, Security fills the form, the Recipient signs first, and a witness signs.")]),
  ("Situation A: staff hands items to Security", [
      (6, "Situation A: you hand items to Security. Security signs first, as Recipient."),
      (7, "In the app, the order is: Recipient, Security staff. Handed over by, you. Then the witness. Security types all names, items and IDs first. You only check and sign."),
      (8, "Security passes you the phone. The orange box shows your name. Check your name, your role, and the items listed."),
      (9, "If everything is correct, sign with your finger and tap ‘Confirm’. Tap ‘Clear’ if you need to sign again."),
      (10, "Next, the witness does the same: check their own name, sign, and tap ‘Confirm’."),
      (11, "When the screen says so, the witness gives the phone back to Security. Security saves the record.")]),
  ("Situation B: Security hands items to CBTO", [
      (12, "Situation B: Security hands items to CBTO. CBTO staff sign first, as Recipient."),
      (13, "In the app, the order is: Recipient, CBTO staff. Handed over by, Security staff. Then the witness. Check every item listed is what you received."),
      (14, "If you are the CBTO staff member, you sign first. Scroll up and check every item you received."),
      (15, "Sign with your finger and tap ‘Confirm’. Tap ‘Clear’ to sign again."),
      (16, "Pass the phone back to Security. Security signs as ‘Handed over by’. Then the witness checks, signs and confirms."),
      (17, "The witness does the same: check their own name, sign, and tap ‘Confirm’."),
      (18, "When the screen says so, the witness gives the phone back to Security. Security saves the record.")]),
  ("The signed copy", [(19, "This is a real Saved screen from a TEST record. The Record ID is in the PDF file name. Security staff email the PDF to you. Keep it for your records.")]),
  ("Remember", [(20, "Remember: check your name and role, and read the details before signing. Don’t sign for someone else, or if the details are wrong. Don’t close the app, press Back, or take photos of the screen."),
                (21, "Your signature goes into one signed PDF per form, with every signature and a Record ID. It is kept in a restricted AirAsia folder, with a record log, and a PDF copy is emailed to you.")]),
 ]),
 "v4_search": dict(VIDEOS["v4_search"], scenes=[
  ("What changed", [(1, "Security fills in the Search List and hands you the phone. This guide is for staff or workmen being searched, and witnesses."), (2, _CHANGED)]),
  ("How it works", [(3, _STEPS), (4, _NEED), (5, "This part is for the person searched, and the witness, if one is present. It is the same flow as FOCA and NOTOC.")]),
  ("The paper form we used", [(6, "This is the paper form we used. Security fills the form. In the app, the person searched signs first. The witness signs second, only if present. "
                                  "Then the Security staff who searched. Check the items found are listed correctly, or ‘Nil’, before you sign.")]),
  ("Check your name and the items", [(7, "Check it is your turn: the orange box shows your name. Scroll up and read the search details and the items found. "
                                         "If nothing was found, the form should say ‘Nil’. If anything is wrong, tell Security before you sign.")]),
  ("Sign and confirm", [(8, "If everything is correct, sign with your finger. Tap ‘Clear’ if you need to sign again. Then tap ‘Confirm’."),
                        (9, "If a witness is present, they do the same: check their own name, sign, and tap ‘Confirm’."),
                        (10, _LAST)]),
  ("The signed copy", [(11, "This is a real Saved screen from a TEST record. The app creates the signed PDF, and the Record ID is in the file name. "
                            "Security staff email you a copy of the signed Search List. Keep it for your records.")]),
  ("Remember", [(12, _REMEMBER), (13, _WHERE.format(f="Search List"))]),
 ]),
}
