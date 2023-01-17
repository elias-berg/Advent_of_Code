import Tower from "../Tower.js";

export abstract class Block {
  public IsAddedToTower = false; // End-state signaller

  protected Left = 2; // This should always be true

  protected Bottom: number; // The bottom-most position of the block
  protected Width: number; // How many positions wide the block is
  protected Height: number; // How many positions tall the block is

  // Here we have an index-sensitive list of positions. It needs to be organized
  // in a way that we can move all pieces down and left by iterating from the
  // start to the end, or move all right by iterating from the end to the start.
  protected Positions: number[][];

  constructor(tower: Tower) {
    this.Bottom = tower.TowerHeight + 3;
  }

  protected GetSetBlock(x: number, y: number, tower: Tower): void {
    if (y === tower.Top()) {
      tower.AppendTopRow();
    }

    const curBlock = tower.Get(x, y);
    curBlock.text("@");
    curBlock.attr("data-type", "block");
    this.Positions.push([x, y]);
  }

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
      this.MovePositionsDown(tower);
    } else {
      this.AddToTower(tower);
    }
  }

  private ShiftLeft(tower: Tower): void {
    // Can't shift left
    if (this.Left === 0) {
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
      this.ShiftPositionsLeft(tower);
    }
  }

  private ShiftRight(tower: Tower): void {
    // Can't shift right
    if (this.Left + this.Width === Tower.TOWER_WIDTH) {
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
      this.ShiftPositionsRight(tower);
    }
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
    const blockHeight = this.Bottom + this.Height;
    if (blockHeight > tower.TowerHeight) {
      tower.TowerHeight = blockHeight;
    }

    this.IsAddedToTower = true;
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
}