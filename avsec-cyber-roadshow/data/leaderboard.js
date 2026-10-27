/* =====================================================================
 *  AVSEC CYBER ROADSHOW — LEADERBOARD DATA BLOCK  (the only file to edit)
 * =====================================================================
 *
 *  1. Replace each [BRACKETED] value with the confirmed result.
 *  2. Save, then rerender:   npm run render
 *
 *  RULES
 *  - rank      1 = first place. Cards reveal 3 → 2 → 1, so order comes
 *              from this number, not from the order of the lines below.
 *  - name      As the person wants it shown. Up to ~22 characters fits
 *              on one line; longer names wrap to two lines automatically.
 *  - points    A number (1000) or text. Numbers are shown as "1,000".
 *  - time      ONLY a real recorded completion time, e.g. "16.2s".
 *              Set to null to hide the time row for that person.
 *  - Ranking rule used by the Spot the Security Risk board:
 *              highest points first, then the fastest completion time.
 *
 *  While any value is still in [BRACKETS], the video shows a red
 *  "PREVIEW · RESULTS PENDING" tag on the rank cards so it cannot be
 *  mistaken for a final cut.
 * ===================================================================== */

window.AVSEC_DATA = {
  leaderboard: [
    { rank: 1, name: "[FIRST PLACE NAME]",  points: "[POINTS]", time: "[TIME]" },
    { rank: 2, name: "[SECOND PLACE NAME]", points: "[POINTS]", time: "[TIME]" },
    { rank: 3, name: "[THIRD PLACE NAME]",  points: "[POINTS]", time: "[TIME]" },
  ],

  /* Public participant link for the end card and the QR code.
   * Verified 2026-10-27: the booth host page builds its join link as
   * <site>/play, and the official booth QR (/qr.svg) decodes to this URL.
   * NEVER put the /host or organizer URLs here.
   * Set to "" to show the [PUBLIC SPOT THE RISK LINK] placeholder and
   * hide the QR code. */
  challengeUrl: "https://airasia-avsec-spot-the-risk.vercel.app/play",

  /* Logos shown on the opening and the end card (supplied by the client).
   *   "assets/logos/x.png"  show that file (PNG with transparency is best)
   *   ""                    show a dashed [LOGO] placeholder slot
   *   null                  leave that logo out entirely */
  logos: {
    avsec: "assets/logos/avsec.png",
    allstars: "", // add assets/logos/allstars.png, then set "assets/logos/allstars.png"
  },
};
