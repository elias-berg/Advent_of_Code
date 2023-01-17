import { Block } from "./Block.js";
import Tower from "../Tower.js";

export class BackwardsLBlock extends Block {
  constructor(tower: Tower) {
    super(tower);

    this.Height = 3;
    this.Width = 3;

    this.Positions = [];
    // Bottom-left
    let x = this.Left;
    let y = this.Bottom;
    this.GetSetBlock(x, y, tower);
    // Bottom-middle
    x = this.Left + 1;
    y = this.Bottom;
    this.GetSetBlock(x, y, tower);
    // The shaft
    for (let i = 0; i < this.Height; i++) {
      x = this.Left + 2;
      y = this.Bottom + i;
      this.GetSetBlock(x, y, tower);
    }
  }
}