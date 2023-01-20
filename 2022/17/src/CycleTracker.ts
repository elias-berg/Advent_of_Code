// O(1) lookup of a move to all possible sequences it could start for
type CycleMap = {
  [key: string]: CycleSequenceMap // The key is a movement string
}

// Map of the entire sequence to the index it was first found at
type CycleSequenceMap = {
  [key: string]: number; // The key is an entire 5-move sequence string
}

// A mapping of the Index a possible sequence was detected at
type PossibleCycles = {
  [key: number]: PossibleCycle // The key is the AbsoluteSequence length to check for a cycle
}

// Data about a possible cycle:
// - the index it started at
// - the length of the cycle
type PossibleCycle = {
  Index: number,
  Length: number
};

// The data about a confirmed cycle!
// - The block movements, mainly important for the tower height increase
// - The number of blocks in the cycle, to jump to the end of the block count goal
// - The current height gained by the entire cycle (sum of all Move.Height values)
type Cycle = {
  Moves: Move[],
  Length: number,
  Height: number
}

// Data about an individual block being added to the tower
type Move = {
  Key: string;    // The movement key string
  Height: number; // The height the tower increased by this move
}

class CycleTracker {
  private static SeenSequences: CycleMap;
  private static CurSequence: string[]; // An array of size-5 arrays of possible start sequences to a cycle
  private static PossibleCycles: PossibleCycles;
  private static AbsoluteSequence: Move[];

  public static DetectedCycle: Cycle; // We know we have a cycle when this gets set

  static {
    this.Reset();
  }

  public static Reset() {
    this.SeenSequences = {};
    this.CurSequence = [];
    this.AbsoluteSequence = [];
    this.PossibleCycles = {};
    this.DetectedCycle = undefined; // I.e. null
  }

  /**
   * Helper function to prove a possible cycle is real.
   * I.e. runs through the entire cycle at it's original start and the subsequent
   * start and makes sure all corresponding movements are the same.
   * @param idx Index the alleged cycle started at.
   * @param len The length of the alleged cycle.
   * @returns True if the cycle is confirmed, false otherwise.
   */
  private static CheckSequence(idx: number, len: number): boolean {
    let heightGained = 0;
    for (let a = idx; a < idx + len; a++) {
      const b = a + len;
      if (this.AbsoluteSequence[a].Key !== this.AbsoluteSequence[b].Key) {
        return false;
      }
      heightGained += this.AbsoluteSequence[a].Height;
    }

    this.DetectedCycle = {
      Moves: this.AbsoluteSequence.slice(idx, idx + len),
      Length: len,
      Height: heightGained
    };
    return true;
  }

  /**
   * Public entry into the cycle detection; evaluates a single move and
   * whether or not it's indicative of a cycle so we can stop computing moves.
   * @param key Movement key string, containing data about the move.
   * @param height The height the tower increased from the move.
   * @returns True if we found a cycle, false otherwise.
   */
  public static Add(key: string, height: number): boolean {
    this.AbsoluteSequence.push({
      Key: key,
      Height: height
    });
    const curIdx = this.AbsoluteSequence.length;

    // If we're at an index where we may have a possible sequence, try it out
    if (this.PossibleCycles[curIdx]) {
      const possible = this.PossibleCycles[curIdx];
      if (this.CheckSequence(possible.Index, possible.Length)) {
        return true;
      }
      delete this.PossibleCycles[curIdx]; // Remove for memory's sake
    }

    // Otherwise, proceed with the checking for a start sequence.
    // Always start the check by making sure we at least have a 5-move sequence.
    if (this.CurSequence.push(key) < 5) {
      return false;
    }

    this.TrackSequence();

    // Now pop off the front before the next iteration
    this.CurSequence = this.CurSequence.slice(1);
    return false;
  }

  /**
   * Helper function to do the actual tracking of the current 5-move sequence
   * and determining if we've detected a possible cycle.
   * Adds to the PossibleCycles collection if we may be onto something.
   * 1) First convert the current 5-move sequence array into a long string (i.e. a character array)
   * 2) Then check and see if we've seen the first move in the sequence string before...
   * 2a) If we haven't seen it, map the move starting the sequence to the sequence string
   * 2b) If we have seen it before, then iterate through all of the
   */
  private static TrackSequence() {
    const curIdx = this.AbsoluteSequence.length;

    const curStart = this.CurSequence.join("");
    const entry = {
      Index: curIdx,
      Sequence: curStart
    };

    // Add the front of the collection to the dict
    const startKey = this.CurSequence[0];

    // If not seen this key before
    if (!this.SeenSequences[startKey] || !this.SeenSequences[startKey][curStart]) {
      this.SeenSequences[startKey] = {};
      this.SeenSequences[startKey][curStart] = curIdx; // Copy it
    } else {
      // We've seen this start move and entire start sequence before
      const sequenceIdx = this.SeenSequences[startKey][curStart];
      const sequenceLen = (curIdx - sequenceIdx)
      const possibleCycle = {
        Index: sequenceIdx,
        Length: sequenceLen
      };
      // Test the cycle out by the time we get another iteration to check it
      this.PossibleCycles[sequenceIdx + (sequenceLen * 2)] = possibleCycle;
    }
  }
}

export default CycleTracker;