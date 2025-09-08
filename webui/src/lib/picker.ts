/**
 * Client-side deterministic shot picker
 * 
 * Implements the same logic as cli/picker.py to ensure consistency
 * between CLI and UI filtering.
 */

/**
 * Pick k unique indices from range [0, n_total) using deterministic hashing.
 * 
 * @param nTotal Total number of shots available
 * @param mmdd Birth date in MMDD format (e.g., "0802")
 * @param k Number of shots to pick (default 3)
 * @returns Array of k unique indices
 */
export function pickIndices(nTotal: number, mmdd: string, k: number = 3): number[] {
  if (nTotal === 0) {
    return [];
  }
  
  if (k >= nTotal) {
    // If we want more shots than available, return all indices
    return Array.from({ length: nTotal }, (_, i) => i);
  }
  
  // Create deterministic seed from birth date using Web Crypto API
  const encoder = new TextEncoder();
  const data = encoder.encode(mmdd);
  
  // Use a simple hash function since Web Crypto API doesn't have SHA256 in all environments
  let hash = 0;
  for (let i = 0; i < data.length; i++) {
    const char = data[i];
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  
  // Use the hash as seed for Math.random
  const seed = Math.abs(hash);
  
  // Simple seeded random number generator
  function seededRandom(seed: number): () => number {
    let current = seed;
    return () => {
      current = (current * 9301 + 49297) % 233280;
      return current / 233280;
    };
  }
  
  const rng = seededRandom(seed);
  
  // Generate k unique indices
  const indices: number[] = [];
  const available = Array.from({ length: nTotal }, (_, i) => i);
  
  for (let i = 0; i < k; i++) {
    const randomIndex = Math.floor(rng() * available.length);
    indices.push(available.splice(randomIndex, 1)[0]);
  }
  
  return indices.sort((a, b) => a - b);
}

/**
 * Filter cards based on birth date using the same picker logic.
 * 
 * @param cards Array of all available cards
 * @param mmdd Birth date in MMDD format
 * @param k Number of cards to select (default 3)
 * @returns Array of selected cards
 */
export function filterCardsByBirthDate<T>(cards: T[], mmdd: string, k: number = 3): T[] {
  const indices = pickIndices(cards.length, mmdd, k);
  return indices.map(index => cards[index]);
}
