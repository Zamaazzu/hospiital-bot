function normalize(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function levenshtein(a, b) {
  const m = a.length;
  const n = b.length;
  if (m === 0) return n;
  if (n === 0) return m;

  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost);
    }
  }
  return dp[m][n];
}

// Slides a window of transcriptWords the same length as phraseWords across the
// transcript, and accepts a match if the average per-word edit distance is
// small relative to word length — this is what forgives "orthopedics" vs
// "orthopaedics" (distance 1) or the odd dropped/garbled letter from the
// speech recognizer, without accepting completely unrelated words.
function fuzzyPhraseInTranscript(transcriptWords, phraseWords) {
  if (phraseWords.length > transcriptWords.length) return false;

  for (let start = 0; start <= transcriptWords.length - phraseWords.length; start++) {
    let totalDistance = 0;
    let totalLength = 0;

    for (let i = 0; i < phraseWords.length; i++) {
      const tWord = transcriptWords[start + i];
      const pWord = phraseWords[i];
      totalDistance += levenshtein(tWord, pWord);
      totalLength += Math.max(tWord.length, pWord.length);
    }

    // Allow up to ~30% of characters to differ across the phrase.
    if (totalLength > 0 && totalDistance / totalLength <= 0.3) return true;
  }

  return false;
}

// Minimum keyword length before we allow prefix matching. Short aliases like
// "eye" or "ent" are too common as substrings of unrelated words (e.g. "ent"
// inside "appointment"), so prefix matching only kicks in for longer,
// distinctive keywords such as "ortho".
const MIN_PREFIX_LEN = 4;

// Catches things like "orthopedic", "orthoclinic", or any other word that
// starts with a distinctive department keyword, even if it doesn't match any
// alias exactly — e.g. any word starting with "ortho" should route to
// Orthopaedics.
function hasPrefixMatch(transcriptWords, candidateWord) {
  if (candidateWord.length < MIN_PREFIX_LEN) return false;
  return transcriptWords.some(
    (word) => word.length >= MIN_PREFIX_LEN && (word.startsWith(candidateWord) || candidateWord.startsWith(word))
  );
}

/**
 * Finds the department whose name or alias best matches the given transcript,
 * tolerating spelling variants (orthopaedics/orthopedics), minor
 * speech-recognition errors (a dropped or swapped letter), and words that
 * merely start with a distinctive department keyword (any "ortho..." word →
 * Orthopaedics). Returns null if nothing matches closely enough.
 */
export function matchDepartment(transcriptText, departments) {
  if (!transcriptText) return null;

  const transcriptWords = normalize(transcriptText).split(" ").filter(Boolean);
  if (!transcriptWords.length) return null;

  for (const dept of departments) {
    const candidates = [dept.name, ...(dept.aliases || [])];

    for (const candidate of candidates) {
      const candidateWords = normalize(candidate).split(" ").filter(Boolean);
      if (!candidateWords.length) continue;

      if (candidateWords.length === 1 && hasPrefixMatch(transcriptWords, candidateWords[0])) {
        return dept;
      }

      if (fuzzyPhraseInTranscript(transcriptWords, candidateWords)) {
        return dept;
      }
    }
  }

  return null;
}
