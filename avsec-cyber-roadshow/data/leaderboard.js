/* =====================================================================
 *  AVSEC CYBER ROADSHOW — DATA BLOCK  (the only file to edit)
 * =====================================================================
 *
 *  Edit the values below, save, then rerender:   npm run render
 * ===================================================================== */

window.AVSEC_DATA = {
  /* Spot the Security Risk leaderboard, shown as the real booth screen.
   * List the screenshots top of the board first. They are joined into one
   * board (assets/leaderboard/board.png) automatically on every render:
   * the header is taken from the first screenshot, rows that appear in two
   * screenshots are shown once. Ranking is the board's own: highest
   * points first, then the fastest completion time. */
  leaderboardScreenshots: [
    "assets/leaderboard/screens/1.png", // header + 01–05
    "assets/leaderboard/screens/2.png", // 04–12
    "assets/leaderboard/screens/3.png", // 13–20
  ],

  /* Human Firewall video quiz leaderboard, typeset in the quiz's own style.
   * Copied from the quiz leaderboard screenshots (27 Oct 2026); order as the
   * quiz board shows it (each name once, best score, highest first). */
  videoQuiz: [
    { rank: 1, name: "Sofian Akasah", score: "100%" },
    { rank: 2, name: "Helmy", score: "100%" },
    { rank: 3, name: "Azq", score: "100%" },
    { rank: 4, name: "Daniel", score: "100%" },
    { rank: 5, name: "MC", score: "100%" },
    { rank: 6, name: "Dahri", score: "100%" },
    { rank: 7, name: "Lilian", score: "100%" },
    { rank: 8, name: "Tan", score: "100%" },
    { rank: 9, name: "Hariz roszeli", score: "100%" },
    { rank: 10, name: "Kethees", score: "100%" },
    { rank: 11, name: "Harry", score: "100%" },
    { rank: 12, name: "Rahman", score: "90%" },
    { rank: 13, name: "Aizulrizwan", score: "90%" },
    { rank: 14, name: "Hakim", score: "90%" },
    { rank: 15, name: "Yohanraj", score: "90%" },
    { rank: 16, name: "Dzaqwan", score: "90%" },
    { rank: 17, name: "Prunthaasini", score: "90%" },
    { rank: 18, name: "Afifi Albarr", score: "90%" },
    { rank: 19, name: "Afiqah Isa", score: "90%" },
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
