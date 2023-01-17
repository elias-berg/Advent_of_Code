// This class holds all of the logic needed to solve the 2022 day 17 problems.

import Tower from "./Tower.js";
import { Block } from "./blocks";
import BlockFactory from "./BlockFactory.js";

class BlockSimulation {
  private static readonly BLOCK_GOAL = 2022;
  private static readonly ANIMATION_SPEED = 0; // Settable for debugging

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
  constructor(jetStr: string, towerRoot: JQuery<HTMLElement>) {
    this.JetString = jetStr;
    this.JetIndex = 0;
    this.JetModulo = jetStr.length;

    this.BlockCount = 0;

    this.Tower = new Tower(towerRoot);
  }

  public Reset() {
    if (this.Timer) {
      clearTimeout(this.Timer);
    }
    // We don't clear anything else since we'll create a new instance of
    // the tower object when the user selects an input file.
  }

  public MoveBlocks(fastMode: boolean): void {
    if (!fastMode) {
      // This should only happen the FIRST time the function is called
      if (!this.CurrentBlock) {
        this.CreateBlock();
      }
      if (this.BlockCount === BlockSimulation.BLOCK_GOAL && this.CurrentBlock.IsAddedToTower) {
        this.ShowFinalHeight();
      } else {
        this.StartSequence(); // Continue onwards
      }
    } else {
      while (this.BlockCount !== BlockSimulation.BLOCK_GOAL) {
        this.MoveSingleBlock();
      }
      this.ShowFinalHeight();
    }
  }

  /**
   * Simple wrapper around the end-state.
   */
  private ShowFinalHeight(): void {
    this.TowerHeightElement.text(this.Tower.TowerHeight);
    alert("The final tower height: " + this.Tower.TowerHeight);
  }

  /**
   * Step 1 of 3 in the sequence: create the block.
   */
  private StartSequence(): void {
    if (this.CurrentBlock.IsAddedToTower) {
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
}

export default BlockSimulation;