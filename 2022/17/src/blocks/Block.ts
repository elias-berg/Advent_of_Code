import Tower from "../Tower.js";
import CycleTracker from "../CycleTracker.js";

export abstract class Block {
  public IsAddedToTower = false; // End-state signaller

  protected Left = 2; // This should always be true

  protected Bottom: number; // The bottom-most position of the block
  protected Width: number; // How many positions wide the block is
  protected Height: number; // How many positions tall the block is

  // All of the positions of each piece of the block
  protected Positions: number[][];

  // Inheriting class defined block letter for cycle detection.
  protected BlockKey: string;
  // The directions the block is pushed left and right.
  // Used to create a cycle-detection key.
  private JetStreams: string;
  // The number of downward movements the block undergoes.
  // Used to create a cycle-detection key.
  private PositionsMoved: number;

  constructor(tower: Tower) {
    this.Bottom = tower.TowerHeight + 3;

    this.JetStreams = "";
    this.PositionsMoved = 0;
  }

  /**
   * Helper function to get a position within the tower and set it as
   * a piece of the current block.
   * @param x The X-coordinate of the current block piece position.
   * @param y The Y-coordinate of the current block piece position.
   * @param tower The tower we're adding the block to.
   */
  protected GetSetBlock(x: number, y: number, tower: Tower): void {
    if (y === tower.Top()) {
      tower.AppendTopRow();
    }

    const curBlock = tower.Get(x, y);
    curBlock.text("@");
    curBlock.attr("data-type", "block");
    this.Positions.push([x, y]);
  }

  /**
   * Handy function for all blocks to call the appropriate shift function.
   * @param dir The direction to shift, either "<" or ">".
   * @param tower The block tower we're shifting relative to.
   */
  public ShiftDirection(dir: string, tower: Tower): void {
    if (dir === "<") {
      this.ShiftLeft(tower);
    } else { // dir === ">"
      this.ShiftRight(tower);
    }
  }

  /**
   * Moves block one position down if nothing is blocking it.
   * If the floor or another block is blocking it, then it becomes
   * a part of the tower.
   * @param tower The tower we're moving the block within/adding to.
   */
  public MoveDown(tower: Tower): void {
    // If we've hit the floor
    if (this.Bottom === 0) {
      this.AddToTower(tower);
      return;
    }

    // Need to see if we can even move down first
    let canMove = true;
    for (const curPosition of this.Positions) {
      const x = curPosition[0];
      const y = curPosition[1];
      const nextBlock = tower.Get(x, y - 1);
      // Only evaluate the next position if it's not a part of the current block
      if (nextBlock.attr("data-type") !== "block") {
        canMove = canMove && (nextBlock.text() === "-");
      }
    }

    if (canMove) {
      this.PositionsMoved++; // For cycle detection
      this.MovePositionsDown(tower);
    } else {
      this.AddToTower(tower);
    }
  }

  /**
   * Shifts the block one position to the left if nothing is blocking it.
   * @param tower The tower we're shifting the block within.
   */
  private ShiftLeft(tower: Tower): void {
    // Can't shift left
    if (this.Left === 0) {
      this.JetStreams += "!<";
      return;
    }

    let canMove = true;
    for (const curPosition of this.Positions) {
      const x = curPosition[0];
      const y = curPosition[1];
      const nextBlock = tower.Get(x - 1, y);
      // Only evaluate the next position if it's not a part of the current block
      if (nextBlock.attr("data-type") !== "block") {
        canMove = canMove && (nextBlock.text() === "-");
      }
    }

    if (canMove) {
      this.JetStreams += "<"; // For cycle detection
      this.ShiftPositionsLeft(tower);
    } else {
      this.JetStreams += "!<";
    }
  }

  /**
   * Shifts the block one position to the right if nothing is blocking it.
   * @param tower The tower we're shifting the block within.
   */
  private ShiftRight(tower: Tower): void {
    // Can't shift right
    if (this.Left + this.Width === Tower.TOWER_WIDTH) {
      this.JetStreams += "!>";
      return;
    }

    let canMove = true;
    for (const curPosition of this.Positions) {
      const x = curPosition[0];
      const y = curPosition[1];
      const nextBlock = tower.Get(x + 1, y);
      // Only evaluate the next position if it's not a part of the current block
      if (nextBlock.attr("data-type") !== "block") {
        canMove = canMove && (nextBlock.text() === "-");
      }
    }

    if (canMove) {
      this.JetStreams += ">";
      this.ShiftPositionsRight(tower);
    } else {
      this.JetStreams += "!>";
    }
  }

  /**
   * Generic function for all blocks to move all of the block pieces
   * down in unison.
   * @param tower The block tower we're moving relative to.
   */
  protected MovePositionsDown(tower: Tower) {
    for (let i = 0; i < this.Positions.length; i++) {
      const curPosition = this.Positions[i];
      const curBlock = tower.Get(curPosition[0], curPosition[1]);
      const nextBlock = tower.Get(curPosition[0], curPosition[1] - 1);
      nextBlock.text("@");
      nextBlock.attr("data-type", "block");
      curBlock.text("-");
      curBlock.removeAttr("data-type");
      this.Positions[i] = [curPosition[0], curPosition[1] - 1];
    }
    this.Bottom--;
  }

  /**
   * Generic function for all blocks to shift all of the block pieces
   * left in unison.
   * @param tower The block tower we're moving relative to.
   */
  protected ShiftPositionsLeft(tower: Tower) {
    for (let i = 0; i < this.Positions.length; i++) {
      const curPosition = this.Positions[i];
      const curBlock = tower.Get(curPosition[0], curPosition[1]);
      const nextBlock = tower.Get(curPosition[0] - 1, curPosition[1]);
      nextBlock.text("@");
      nextBlock.attr("data-type", "block");
      curBlock.text("-");
      curBlock.removeAttr("data-type");
      this.Positions[i] = [curPosition[0] - 1, curPosition[1]];
    }
    this.Left--;
  }

  /**
   * Generic function for all blocks to shift all of the block pieces
   * right in unison.
   * @param tower The block tower we're moving relative to.
   */
  protected ShiftPositionsRight(tower: Tower) {
    for (let i = this.Positions.length - 1; i >= 0; i--) {
      const curPosition = this.Positions[i];
      const curBlock = tower.Get(curPosition[0], curPosition[1]);
      const nextBlock = tower.Get(curPosition[0] + 1, curPosition[1]);
      nextBlock.text("@");
      nextBlock.attr("data-type", "block");
      curBlock.text("-");
      curBlock.removeAttr("data-type");
      this.Positions[i] = [curPosition[0] + 1, curPosition[1]];
    }
    this.Left++;
  }

  /**
   * Once the block can't move any further, call this function.
   * "One of us. One of us."
   * @param tower The block tower we're adding the block to.
   */
  public AddToTower(tower: Tower) {
    this.Positions.map((position: number[]) => {
      const curBlock = tower.Get(position[0], position[1]);
      curBlock.attr("data-type", "tower");
    });

    // Update the tower height
    let heightDiff = 0;
    const blockHeight = this.Bottom + this.Height;
    if (blockHeight > tower.TowerHeight) {
      heightDiff = blockHeight - tower.TowerHeight;
      tower.TowerHeight = blockHeight;
    }

    this.IsAddedToTower = true;

    // Once we've added to the tower, we can check and see if we've moved this
    // block the same directions and distance before to see if we have a cycle!
    const key = this.BlockKey + this.JetStreams + this.PositionsMoved;
    CycleTracker.Add(key, heightDiff);
  }
}