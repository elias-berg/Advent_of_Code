// This class holds all of the logic needed to solve the 2022 day 17 problems.

import Tower from "./Tower.js";
import { Block } from "./blocks";
import BlockFactory from "./BlockFactory.js";
import CycleTracker from "./CycleTracker.js";

class BlockSimulation {
  private static readonly ANIMATION_SPEED = 0; // Settable for debugging

  private IsPartOne: boolean;
  private BlockGoal: number;

  // Main pieces at play
  private Tower: Tower;
  private CurrentBlock: Block;
  private BlockCount: number;

  // For determining the current jet movement
  private JetString: string;
  private JetIndex: number;
  private JetModulo: number;

  // The simulation is responsible for incrementing/updating these
  public BlockCountElement: JQuery<HTMLElement>;
  public TowerHeightElement: JQuery<HTMLElement>;

  private Timer: NodeJS.Timeout | null;

  // Construct the tower and backing array
  constructor(jetStr: string, towerRoot: JQuery<HTMLElement>, partOne: boolean) {
    this.JetString = jetStr;
    this.JetIndex = 0;
    this.JetModulo = jetStr.length;

    this.BlockCount = 0;

    this.IsPartOne = partOne;
    if (this.IsPartOne) {
      this.BlockGoal = 2022;
    } else {
      this.BlockGoal = 1_000_000_000_000; // Oof! 1 Trillion
    }

    this.Tower = new Tower(towerRoot);
  }

  public Reset() {
    if (this.Timer) {
      clearTimeout(this.Timer);
    }
    // We don't clear anything else since we'll create a new instance of
    // the tower object when the user selects an input file.
    CycleTracker.Reset();
  }

  public MoveBlocks(fastMode: boolean): void {
    if (!fastMode) {
      // This should only happen the FIRST time the function is called
      if (!this.CurrentBlock) {
        this.CreateBlock();
      }
      if (this.BlockCount === this.BlockGoal && this.CurrentBlock.IsAddedToTower) {
        this.ShowFinalHeight();
      } else {
        this.StartSequence(); // Continue onwards
      }
    } else {
      while (this.BlockCount !== this.BlockGoal) {
        this.MoveSingleBlock();
        // If Part 2, then skip to the end!
        if (!this.IsPartOne && CycleTracker.DetectedCycle) {
          this.SkipToTrillionBlockCount();
          return;
        }
      }
      this.ShowFinalHeight();
    }
  }

  /**
   * Simple wrapper around the end-state.
   */
  private ShowFinalHeight(): void {
    const towerHeight = this.Tower.TowerHeight;
    this.TowerHeightElement.text(towerHeight);
    alert("The final tower height: " + towerHeight);
  }

  /**
   * Step 1 of 3 in the sequence: create the block.
   */
  private StartSequence(): void {
    if (this.CurrentBlock.IsAddedToTower) {
      // First see if we detected a cycle
      if (!this.IsPartOne && CycleTracker.DetectedCycle) {
        this.SkipToTrillionBlockCount();
        return;
      }

      this.TowerHeightElement.text(this.Tower.TowerHeight); // Update the latest height
      this.CreateBlock();
    }
    this.Timer = setTimeout(() => this.ApplyJet(), BlockSimulation.ANIMATION_SPEED);
  }

  /**
   * Step 2 of 3 in the sequence: let the jet move the block.
   */
  private ApplyJet(): void {
    // Jet of gas pushes block
    const direction = this.JetString.charAt(this.JetIndex % this.JetModulo);
    this.CurrentBlock.ShiftDirection(direction, this.Tower);
    this.JetIndex++;
    this.Timer = setTimeout(() => this.MoveBlock(), BlockSimulation.ANIMATION_SPEED);
  }

  /**
   * Step 3 of 3 in the sequence: move the block or add it to the tower.
   */
  private MoveBlock(): void {
    // Rock falls one unit
    this.CurrentBlock.MoveDown(this.Tower);
    this.Timer = setTimeout(() => this.MoveBlocks(false), BlockSimulation.ANIMATION_SPEED);
  }

  /**
   * All block movements in a single sequence.
   */
  private MoveSingleBlock(): void {
    this.CreateBlock();
    while (!this.CurrentBlock.IsAddedToTower) {
      // Jet of gas pushes block
      const direction = this.JetString.charAt(this.JetIndex % this.JetModulo);
      this.CurrentBlock.ShiftDirection(direction, this.Tower);
      this.JetIndex++;

      // Rock falls one unit
      this.CurrentBlock.MoveDown(this.Tower);
    }

    this.TowerHeightElement.text(this.Tower.TowerHeight);
  }

  /**
   * Handy wrapper to create a block and increment the counter.
   */
  private CreateBlock(): void {
    const blockType = this.BlockCount % 5; // 5 types of blocks
    this.CurrentBlock = BlockFactory.CreateBlock(blockType, this.Tower);
    this.BlockCount++;

    this.BlockCountElement.text(this.BlockCount);
  }

  private SkipToTrillionBlockCount(): void {
    const cycle = CycleTracker.DetectedCycle;
    const heightPerCycle = cycle.Height;

    const blocksLeft = this.BlockGoal - this.BlockCount;
    const cycleRemainder = blocksLeft % cycle.Length;
    const cyclesLeft = (blocksLeft - cycleRemainder) / cycle.Length;

    this.Tower.TowerHeight += (heightPerCycle * cyclesLeft);

    // Play out the remainder
    for (let i = 0; i < cycleRemainder; i++) {
      this.Tower.TowerHeight += cycle.Moves[i].Height;
    }

    this.BlockCount = this.BlockGoal;
    this.BlockCountElement.text(this.BlockCount);
    this.ShowFinalHeight();
  }
}

export default BlockSimulation;