import { Block } from "./Block.js";
import Tower from "../Tower.js";

export class PlusBlock extends Block {
  constructor(tower: Tower) {
    super(tower);

    this.Height = 3;
    this.Width = 3;
    this.BlockKey = "P";

    this.Positions = [];
    // Bottom-middle
    let x = this.Left + 1;
    let y = this.Bottom;
    this.GetSetBlock(x, y, tower);
    // Middle row
    for (let i = 0; i < this.Width; i++) {
      x = this.Left + i;
      y = this.Bottom + 1;
      this.GetSetBlock(x, y, tower);
    }
    // Top-middle
    x = this.Left + 1;
    y = this.Bottom + 2;
    this.GetSetBlock(x, y, tower);
  }
}